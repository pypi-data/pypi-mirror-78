from dataclasses import dataclass
from typing import Collection


@dataclass(frozen=True)
class User:
    """Info of a user calling a custom HTTP endpoint.

    Attributes:
        name: Name of the user calling the endpoint.
        roles: Roles of the user calling the endpoint.
    """

    name: str
    roles: Collection[str]
