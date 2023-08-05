import numpy as np

from .area import area
from ..core import jitted

__all__ = ["iou"]


@jitted
def _intersection_bb_size(bb_0: np.ndarray, bb_1: np.ndarray) -> np.ndarray:
    """Computes the size of the intersection between two bboxes
    :param bb_0: 1-dimensional np.ndarray of shape (4,) representing the first bbox
    :param bb_1: 1-dimensional np.ndarray of shape (4,) representing the second bbox
    :return: 1-dimensional np.ndarray of shape (2,) representing the [width, height] of the
    intersection between bb_0 and bb_1
    """

    left = max(bb_0[0], bb_1[0])
    right = min(bb_0[0] + bb_0[2], bb_1[0] + bb_1[2])

    width = max(0, right - left)

    top = max(bb_0[1], bb_1[1])
    bottom = min(bb_0[1] + bb_0[3], bb_1[1] + bb_1[3])

    height = max(0, bottom - top)

    return np.array([width, height])


@jitted
def iou(bb_0: np.ndarray, bb_1: np.ndarray) -> float:
    """Computes the IOU between the two bboxes passed as argument
    :param bb_0: 1-dimensional np.ndarray of shaoe (4,) representing the first bbox
    :param bb_1: 1-dimensional np.ndarray of shape (4,) representing the second bbox
    :return: The intersection of union (IOU) between the two bounding bb_1 passed as argument
    """

    # Compute the coordinates of the intersecting rectangle
    w_in, h_in = _intersection_bb_size(bb_0, bb_1)
    intersection_area = w_in * h_in

    # Compute the areas of the individual bboxes
    area_0 = area(bb_0)
    area_1 = area(bb_1)

    return intersection_area / (area_0 + area_1 - intersection_area)
