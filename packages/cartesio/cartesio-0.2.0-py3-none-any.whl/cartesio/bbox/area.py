import numpy as np

from ..core import jitted

__all__ = ["area"]


@jitted
def area(bb: np.ndarray) -> float:
    """Computes the area of the bbox passed as argument
    :param bb: 1-dimensional np.ndarray of shape (4,) representing the bbox for which to compute
    the aread
    :return: the area of the bbox passed as argument
    """

    width = bb[2] - bb[0]
    height = bb[3] - bb[1]

    return width * height
