from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Collection, Mapping, Optional

from .._deprecation import deprecated
from ._auth import Auth
from ._utils import Mergeable
from .parsing import ConfigParsingError

OIDC_AUTH_TYPE = "oidc"


@dataclass(frozen=True)
class OidcAuthentication(Auth, Mergeable):
    """OpenID connect authentication."""

    provider_id: Optional[str]
    issuer_url: Optional[str]
    client_id: Optional[str]
    client_secret: Optional[str]
    name_attribute: Optional[str]
    paths_to_authorities: Optional[Collection[str]]
    scopes: Optional[Collection[str]]
    role_mapping: Optional[Mapping[str, Collection[str]]]

    @deprecated(
        "Constructing OidcAuthentication is deprecated, use atoti.config.create_oidc_authentication instead.",
        unless_called_from={"create_oidc_authentication", "_do_merge", "_from_dict"},
    )
    def __post_init__(self):
        """Raise a deprecation warning if needed."""

    @property
    def _type(self):
        return OIDC_AUTH_TYPE

    @classmethod
    def _from_dict(cls, data: Mapping[str, Any]):
        provider_id = data.get("provider_id")
        issuer_url = data.get("issuer_url")
        client_id = data.get("client_id")
        client_secret = data.get("client_secret")
        name_attribute = data.get("name_attribute")
        paths_to_authorities = data.get("paths_to_authorities")
        scopes = data.get("scopes")
        role_mapping = data.get("role_mapping")
        if role_mapping is None:
            role_mapping = {}
        if role_mapping is not None and not isinstance(role_mapping, dict):
            raise ConfigParsingError(
                "The OpenID Connect role mappings must be a dict", role_mapping
            )

        return OidcAuthentication(
            provider_id,
            issuer_url,
            client_id,
            client_secret,
            name_attribute,
            paths_to_authorities,
            scopes,
            role_mapping,
        )

    @classmethod
    def _do_merge(
        cls, instance1: OidcAuthentication, instance2: OidcAuthentication
    ) -> OidcAuthentication:
        """Merge the OpenID Connect authentications."""
        # pylint: disable=too-many-branches
        if instance2.provider_id is None:
            provider_id = instance1.provider_id
        elif instance1.provider_id is None:
            provider_id = instance2.provider_id
        elif instance1.provider_id != instance2.provider_id:
            raise ValueError("Cannot merge configurations for two different providers")
        else:
            provider_id = instance1.provider_id
        issuer_url = (
            instance2.issuer_url
            if instance2.issuer_url is not None
            else instance1.issuer_url
        )
        client_id = (
            instance2.client_id
            if instance2.client_id is not None
            else instance1.client_id
        )
        client_secret = (
            instance2.client_secret
            if instance2.client_secret is not None
            else instance1.client_secret
        )
        name_attribute = (
            instance2.name_attribute
            if instance2.name_attribute is not None
            else instance1.name_attribute
        )
        if instance1.paths_to_authorities is None:
            paths_to_authorities = instance2.paths_to_authorities
        elif instance2.paths_to_authorities is None:
            paths_to_authorities = instance1.paths_to_authorities
        else:
            paths_to_authorities = [
                *instance1.paths_to_authorities,
                *instance2.paths_to_authorities,
            ]
        if instance1.scopes is None:
            scopes = instance2.scopes
        elif instance2.scopes is None:
            scopes = instance1.scopes
        else:
            scopes = [
                *instance1.scopes,
                *instance2.scopes,
            ]
        if instance1.role_mapping is None:
            roles = instance2.role_mapping
        elif instance2.role_mapping is None:
            roles = instance1.role_mapping
        else:
            roles = {**instance1.role_mapping, **instance2.role_mapping}
        return OidcAuthentication(
            provider_id,
            issuer_url,
            client_id,
            client_secret,
            name_attribute,
            paths_to_authorities,
            scopes,
            roles,
        )
        # pylint: enable=too-many-branches


def create_oidc_authentication(
    *,
    provider_id: Optional[str] = None,
    issuer_url: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    name_attribute: Optional[str] = None,
    paths_to_authorities: Optional[Collection[str]] = None,
    scopes: Optional[Collection[str]] = None,
    role_mapping: Optional[Mapping[str, Collection[str]]] = None
) -> OidcAuthentication:
    """Create an OpenID connect authentication.

    Args:
        provider_id: The name of your provider. This string is used to build the redirectUrl
            using this template ``{baseUrl}:{port}/login/oauth2/code/{providerId}`` .
        issuer_url: The issuer URL parameter from your provider's OpenID connect configuration
            endpoint.
        client_id: Your app's clientId, obtained from your authentication provider.
        client_secret: Your app's clientSecret, obtained from your authentication provider.
        name_attribute: The key in the ``IdToken`` of the parameter to display as the username in
            the application.
        paths_to_authorities: The location of the authoritios to use for atoti in the returned
            access token or id token.
        scopes: The scopes to request from the authentication provider (e.g. : email, username,
            etc.).
        role_mapping: The mapping between the roles returned by the authentication provider and
            the corresponding roles to use in atoti.
    """
    return OidcAuthentication(
        provider_id,
        issuer_url,
        client_id,
        client_secret,
        name_attribute,
        paths_to_authorities,
        scopes,
        role_mapping if role_mapping is not None else {},
    )
