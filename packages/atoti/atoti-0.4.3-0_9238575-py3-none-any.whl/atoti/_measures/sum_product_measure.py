from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Sequence

from ..column import Column
from ..measure import Measure
from .calculated_measure import AggregatedMeasure
from .utils import get_measure_name

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..cube import Cube


@dataclass(eq=False)
class SumProductFieldsMeasure(Measure):
    """Sum of the product of factors for store fields."""

    _factors: Sequence[Column]

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        # Checks fields are in the selection, otherwise use the other sum product implementation because UDAF needs
        # fields in the selection.
        selection_fields = java_api.get_selection_fields(cube)
        if all([factor.name in selection_fields for factor in self._factors]):
            return java_api.sum_product_udaf(cube, measure_name, self._factors)
        return AggregatedMeasure(  # pylint: disable=protected-access
            SumProductEncapsulationMeasure(
                [
                    (
                        factor._to_measure("SUM")
                        if factor.name in selection_fields
                        else factor._to_measure()
                    )
                    for factor in self._factors
                ]
            ),
            "SUM_PRODUCT",
            None,
        )._do_distil(java_api, cube, measure_name)


@dataclass(eq=False)
class SumProductEncapsulationMeasure(Measure):
    """Create an intermetdiate measure needing to be aggregated with the key "SUM_PRODUCT"."""

    _factors: Sequence[Measure]

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:

        return java_api.sum_product_encapsulation(
            cube, [get_measure_name(java_api, factor, cube) for factor in self._factors]
        )
