from typing import Optional

from .auth import Auth
from .basic_auth import BasicAuthentication, create_basic_authentication
from .session import QuerySession


def open_query_session(
    url: str, name: Optional[str] = None, *, auth: Optional[Auth] = None
) -> QuerySession:
    """Open an existing session to query it.

    This can be used to connect to:

      * Other sessions built with another atoti process
      * ActivePivot cubes built with a classic Java project, if version >= 5.7.0

    Args:
        url: The server base URL, if ``{url}`` is given, ``{url}/versions/rest`` is expected to exist.
        name: The name to give to the session.
            Defaults to the passed ``url``.
        auth: The authentication to use.

    Returns:
        The query session.
    """
    return QuerySession(url, auth or (lambda url: None), name or url)
