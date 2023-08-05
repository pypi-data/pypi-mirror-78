from .._measures.calculated_measure import CalculatedMeasure, Operator
from ..measure import Measure, MeasureLike, _convert_to_measure


def erf(measure: MeasureLike) -> Measure:
    """Return the error function of the input measure.

    This can be used to compute traditional statistical measures such as the cumulative standard normal distribution.

    For more information read:

      * :func:`math.erf` in Python math module
      * `scipy.special.erf <https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.erf.html>`_
      * `The Wikipedia page <https://en.wikipedia.org/wiki/Error_function#Numerical_approximations>`_
    """
    return CalculatedMeasure(Operator("erf", [_convert_to_measure(measure)]))


def erfc(measure: MeasureLike) -> Measure:
    """Return the complementary error function of the input measure.

    This is the complementary of :func:`atoti.math.erf`.
    It is defined as ``1.0 - erf``.
    It can be used for large values of x where a subtraction from one would cause a loss of significance.
    """
    return CalculatedMeasure(Operator("erfc", [_convert_to_measure(measure)]))
