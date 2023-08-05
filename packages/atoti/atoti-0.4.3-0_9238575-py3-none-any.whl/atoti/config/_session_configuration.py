from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Collection, Mapping, Optional, Union

from .._deprecation import deprecated
from .._serialization_utils import FromDict
from ..sampling import DEFAULT_SAMPLING_MODE, SamplingMode
from ._auth import Auth
from ._auth_utils import merge_auth, parse_auth
from ._role import Role
from ._utils import Mergeable
from .parsing import ConfigParsingError

DEFAULT_URL_PATTERN = "http://localhost:{port}"


@dataclass(frozen=True)
class SessionConfiguration(FromDict, Mergeable):
    """Configuration of the session."""

    inherit: bool
    port: Optional[int]
    url_pattern: Optional[str]
    metadata_db: Optional[str]
    roles: Optional[Collection[Role]]
    authentication: Optional[Auth]
    sampling_mode: Optional[SamplingMode]
    max_memory: Optional[str]
    java_args: Optional[Collection[str]]
    i18n_directory: Optional[Union[Path, str]]
    default_locale: Optional[str]

    @deprecated(
        "Constructing SessionConfiguration is deprecated, use atoti.config.create_config instead.",
        unless_called_from={
            "create_config",
            "_complete_with_default",
            "_from_dict",
            "_do_merge",
        },
    )
    def __post_init__(self):
        """Raise a deprecation warning if needed."""

    @classmethod
    def _from_dict(cls, data: Mapping[str, Any]):  # noqa
        if "roles" in data:
            if not isinstance(data["roles"], Collection):
                raise ConfigParsingError("roles must be a collection.")
            roles = [Role._from_dict(role) for role in data["roles"]]
        else:
            roles = None
        auth = parse_auth(data["authentication"]) if "authentication" in data else None
        sampling_mode = (
            SamplingMode._from_dict(data["sampling_mode"])
            if "sampling_mode" in data
            else None
        )
        path = data.get("i18n_directory")
        return SessionConfiguration(
            inherit=data.get("inherit", True),
            port=data.get("port"),
            url_pattern=data.get("url_pattern"),
            metadata_db=data.get("metadata_db"),
            roles=roles,
            authentication=auth,
            sampling_mode=sampling_mode,
            max_memory=data.get("max_memory"),
            java_args=data.get("java_args"),
            i18n_directory=Path(path) if path is not None else None,
            default_locale=data.get("default_locale"),
        )

    @classmethod
    def _do_merge(
        cls, instance1: SessionConfiguration, instance2: SessionConfiguration
    ) -> SessionConfiguration:
        """Merge two instances of the class. Second overrides the first one."""
        if instance1.roles is None:
            roles = instance2.roles
        elif instance2.roles is None:
            roles = instance1.roles
        else:
            role_names2 = [role.name for role in instance2.roles]
            roles = list(instance2.roles) + [
                i for i in instance1.roles if i.name not in role_names2
            ]

        return SessionConfiguration(
            inherit=instance1.inherit and instance2.inherit,
            port=instance2.port or instance1.port,
            url_pattern=instance2.url_pattern or instance1.url_pattern,
            metadata_db=instance2.metadata_db or instance1.metadata_db,
            roles=roles,
            authentication=merge_auth(
                instance1.authentication, instance2.authentication
            ),
            sampling_mode=instance2.sampling_mode or instance1.sampling_mode,
            max_memory=instance2.max_memory or instance1.max_memory,
            java_args=instance2.java_args or instance1.java_args,
            i18n_directory=instance2.i18n_directory or instance1.i18n_directory,
            default_locale=instance2.default_locale or instance1.default_locale,
        )

    def _complete_with_default(self) -> SessionConfiguration:
        """Copy the config into a new one with the default values.

        These values should only be set if None is provided.
        They are not set when creating the configuration to able clean merging.
        """
        return SessionConfiguration(
            inherit=self.inherit,
            port=self.port,
            url_pattern=self.url_pattern or DEFAULT_URL_PATTERN,
            metadata_db=self.metadata_db,
            roles=self.roles,
            authentication=self.authentication,
            sampling_mode=self.sampling_mode or DEFAULT_SAMPLING_MODE,
            max_memory=self.max_memory,
            java_args=self.java_args,
            i18n_directory=self.i18n_directory,
            default_locale=self.default_locale,
        )


def create_config(
    *,
    inherit: bool = True,
    port: Optional[int] = None,
    url_pattern: Optional[str] = None,
    metadata_db: Optional[str] = None,
    roles: Optional[Collection[Role]] = None,
    authentication: Optional[Auth] = None,
    sampling_mode: Optional[SamplingMode] = None,
    max_memory: Optional[str] = None,
    java_args: Optional[Collection[str]] = None,
    i18n_directory: Optional[Union[Path, str]] = None,
    default_locale: Optional[str] = None,
) -> SessionConfiguration:
    """Create a configuration.

    Args:
        inherit: Whether this config should be merged with the default config if it exists.
        port: The port on which the session will be exposed. Defaults to a random available port.
        url_pattern: The pattern of the public URL of the session.
            The ``{host}`` and ``{port}`` placeholders will be replaced with, respectively,
            the actual host address and port number.
            If ``None``, defaults to ``http://localhost:{port}``.
        metadata_db: The description of the database where the session's metadata will be stored.
            It is the path to a file, which will be created if needed.
        roles: The roles and their restrictions.
        authentication: The authentication used by the server.
        sampling_mode: The sampling mode describing how files are loaded into the stores.
            It's faster to build the data model when only part of the data is loaded.

            Modes are available in :mod:`atoti.sampling`.

            If :data:`atoti.sampling.FULL` isn't passed, call :meth:`load_all_data`
            to load everything once the model definition is done.
        max_memory: Max memory allocated to each session.
            Actually sets the ``-Xmx`` JVM parameter.
            The format is a string containing a number followed by a unit among ``G``, ``M`` and ``K``.
            For instance: ``64G``.
            Defaults to the JVM default memory which is 25% of the machine memory.
        java_args: Collection of additional arguments to pass to the Java process.
            For instance: ``["-verbose:gc", "-Xms1g", "-XX:+UseG1GC"]``.
        i18n_directory: The directory from which translation files will be loaded.
            It should contain a list of files (one per locale) named after the locale they contain
            translations for (i.e. ``en-US.json`` for US translations). The application will behave
            differently depending on how the metadata_db is configured:

            * If a local metadata_db, backed by a file, has been configured:

              - If a value is specified for ``i18n_directory`` those files will be uploaded to the
                local metadata_db, overriding any previously defined translations.
              - If no value is specified for ``i18n_directory`` the default translations for atoti
                will be uploaded to the local metadata_db

            * If a remote metadata_db has been configured:

              - If a value is specified for ``i18n_directory`` this data will be pushed to the
                remote metadata_db, overriding any previously existing values
              - If no value has been specified for ``i18n_directory`` and translations exist in the
                remote metadata_db, those values will be loaded into the session
              - If no value has been specified for ``i18n_directory`` and no translations exist in
                the remote metodata_db, the default translations for atoti will be uploaded
                to the remote metadata_db

        default_locale: The default locale to use for internationalizing the session.
    """
    return SessionConfiguration(
        inherit=inherit,
        port=port,
        url_pattern=url_pattern,
        metadata_db=metadata_db,
        roles=roles,
        authentication=authentication,
        sampling_mode=sampling_mode,
        max_memory=max_memory,
        java_args=java_args,
        i18n_directory=i18n_directory,
        default_locale=default_locale,
    )
