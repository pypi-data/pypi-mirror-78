from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class QueryMeasure:
    """Query measure.

    Attributes:
        name: Measure name.
        visible: Whether the measure is visible or not.
        folder: Measure folder.
        formatter: Measure formatter.
    """

    name: str
    visible: bool
    folder: Optional[str]
    formatter: Optional[str]
