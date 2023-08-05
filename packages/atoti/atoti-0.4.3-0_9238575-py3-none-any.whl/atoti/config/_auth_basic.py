from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Collection, Mapping, Optional

from .._deprecation import deprecated
from .._serialization_utils import FromDict
from ._auth import Auth
from ._utils import Mergeable
from .parsing import ConfigParsingError

BASIC_AUTH_TYPE = "basic"


@dataclass(frozen=True)
class BasicUser(FromDict):
    """Basic user with roles."""

    name: str
    password: str
    roles: Collection[str] = field(default_factory=list)

    @deprecated(
        "Constructing BasicUser is deprecated, use atoti.config.create_basic_user instead.",
        unless_called_from={"create_basic_user", "_from_dict"},
    )
    def __post_init__(self):
        """Raise a deprecation warning if needed."""

    @classmethod
    def _from_dict(cls, data: Mapping[str, Any]):
        if "name" not in data:
            raise ConfigParsingError("Missing name for user.", data)
        name = data["name"]
        if "password" not in data:
            raise ConfigParsingError(f"Missing password for user {name}.", data)
        password = data["password"]
        if "roles" in data:
            if not isinstance(data["roles"], Collection):
                raise ConfigParsingError(
                    f"Roles of user {name} must be a collection.", data
                )
            roles = data["roles"]
        else:
            roles = []
        return BasicUser(name, password, roles)


def create_basic_user(
    name: str, password: str, *, roles: Optional[Collection[str]] = None
) -> BasicUser:
    """Create a basic user with roles.

    Args:
        name: User name.
        password: User password.
        roles: User roles.
    """
    return BasicUser(name, password, roles or {})


@dataclass(frozen=True)
class BasicAuthentication(Auth, Mergeable):
    """Basic authentication."""

    users: Collection[BasicUser]
    realm: Optional[str] = None

    @deprecated(
        "Constructing BasicAuthentication is deprecated, use atoti.config.create_basic_authentication instead.",
        unless_called_from={"create_basic_authentication", "_do_merge", "_from_dict"},
    )
    def __post_init__(self):
        """Raise a deprecation warning if needed."""

    @property
    def _type(self):
        return BASIC_AUTH_TYPE

    @classmethod
    def _from_dict(cls, data: Mapping[str, Any]) -> BasicAuthentication:
        """Create the authentication from dictionary."""
        if "users" not in data:
            raise ConfigParsingError("Basic authentication must specify users")
        users_data = data["users"]
        if not isinstance(users_data, Collection):
            raise ConfigParsingError("Basic authentication users must be a collection.")
        users = [BasicUser._from_dict(user) for user in users_data]
        return BasicAuthentication(users, data.get("realm"))

    @classmethod
    def _do_merge(
        cls, instance1: BasicAuthentication, instance2: BasicAuthentication
    ) -> BasicAuthentication:
        """Merge the basic authentications."""
        user_names2 = [user.name for user in instance2.users]
        users = list(instance2.users) + [
            user for user in instance1.users if user.name not in user_names2
        ]
        realm = instance2.realm if instance2.realm is not None else instance1.realm
        return BasicAuthentication(users, realm)


def create_basic_authentication(
    users: Collection[BasicUser], *, realm: Optional[str] = None
) -> BasicAuthentication:
    """Create a basic authentication.

    Args:
        users: The list of users that can authenticate against the session.
        realm: The realm describing the protected area.
            Different realms can be used to isolate sessions running on the same domain
            (regardless of the port).
            The realm will also be displayed by the browser when prompting for credentials.
            Defaults to ``f"{session_name} atoti session at {session_id}"``.

    """
    return BasicAuthentication(users, realm)
