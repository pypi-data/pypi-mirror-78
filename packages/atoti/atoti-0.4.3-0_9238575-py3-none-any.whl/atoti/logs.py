from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Logs:
    """Lines of logs.

    Attributes:
        lines: List of logs' lines.
    """

    lines: List[str]

    def _repr_html_(self) -> str:
        return f"<pre>{str(self)}</pre>"

    def __str__(self) -> str:
        """Return the string representation."""
        return "".join(self.lines)
