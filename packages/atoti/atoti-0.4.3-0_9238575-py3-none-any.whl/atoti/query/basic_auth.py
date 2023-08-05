from base64 import b64encode
from dataclasses import dataclass

from .._deprecation import deprecated
from .auth import Auth


def create_basic_authentication(username: str, password: str) -> Auth:
    """Create a basic authentication.

    It can be used on ActivePivots's sandbox for instance.
    """
    plain_credentials = f"{username}:{password}"
    encoded_credentials = str(b64encode(plain_credentials.encode("ascii")), "utf8")
    htt_headers = {"Authorization": f"Basic {encoded_credentials}"}
    return lambda url: htt_headers


@dataclass(frozen=True)
class BasicAuthentication:
    """Basic Authentication."""

    username: str
    password: str

    @deprecated(
        "Constructing BasicAuthentication is deprecated, use atoti.query.create_basic_authentication instead.",
    )
    def __post_init__(self):
        """Raise a deprecation warning."""

    def __call__(self, url: str):
        """Return the authentication headers for the passed URL."""
        return create_basic_authentication(self.username, self.password)(url)
