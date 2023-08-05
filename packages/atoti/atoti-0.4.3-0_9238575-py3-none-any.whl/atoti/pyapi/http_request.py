from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class HttpRequest:
    """Info of an HTTP request.

    Attributes:
        url: URL the client used to make the request.
        body: Parsed JSON body of the request.
    """

    url: str
    body: Any
