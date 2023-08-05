from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from .pyapi.http_request import HttpRequest
from .pyapi.user import User

if TYPE_CHECKING:
    from .session import Session

    CallbackEndpoint = Callable[[HttpRequest, User, Session], str]


@dataclass
class PyApiEndpoint:
    """Session endpoint using a Python callback."""

    callback: CallbackEndpoint
    session: Session
    name: str = "Python.PyApiEnpoint"

    def performRequest(  # pylint: disable=invalid-name
        self, url: str, body: str, user_name: str, roles: str
    ) -> str:
        """Call when the associated route is requested.

        Args:
            url: The URL the user used for the query.
            body: String containing the request body, Only JSON is supported.
            user_name: Name of the user doing the query.
            roles: Roles of the user doing the query (string representing a set).
        """
        return self.callback(
            HttpRequest(url, json.loads(body)),
            User(user_name, roles[1 : len(roles) - 1].split(", ")),
            self.session,
        )

    def toString(self) -> str:  # pylint: disable=invalid-name
        """To string."""
        return self.name

    class Java:
        """Code needed for Py4J callbacks."""

        implements = ["com.activeviam.chouket.pyapi.PyApiEndpoint"]
