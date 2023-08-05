"""Tests for `cartesio.bbox` subpackage and modules."""

import unittest

import numpy as np

import cartesio as cs


class TestCartesioBBox(unittest.TestCase):
    """Tests for `cartesio.bbox` subpackage and modules."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_area(self):
        bb = np.array([0, 0, 0, 0])
        self.assertEqual(cs.bbox.area(bb), 0)

        bb = np.array([0, 0, 0, 1])
        self.assertEqual(cs.bbox.area(bb), 0)

        bb = np.array([0, 0, 1, 0])
        self.assertEqual(cs.bbox.area(bb), 0)

        bb = np.array([0, 0, 1, 1])
        self.assertEqual(cs.bbox.area(bb), 1)

        bb = np.array([1, 1, 2, 2])
        self.assertEqual(cs.bbox.area(bb), 1)

        bb = np.array([1.5, 1.5, 2.0, 3.5])
        self.assertEqual(cs.bbox.area(bb), 1)

    def test_iou(self):
        bb_0 = np.array([0, 0, 1, 1])
        bb_1 = np.array([0, 0, 1, 1])
        self.assertEqual(cs.bbox.iou(bb_0, bb_1), 1)

        bb_0 = np.array([0, 0, 1, 1])
        bb_1 = np.array([0, 0, 2, 2])
        self.assertEqual(cs.bbox.iou(bb_0, bb_1), 1 / 4)

        bb_0 = np.array([1, 1, 2, 2])
        bb_1 = np.array([0, 0, 2, 2])
        self.assertEqual(cs.bbox.iou(bb_0, bb_1), 1 / 4)

        bb_0 = np.array([1.5, 1.5, 2.5, 2.5])
        bb_1 = np.array([0, 0, 2, 2])
        self.assertEqual(cs.bbox.iou(bb_0, bb_1), 0.5 ** 2 / (5 - 0.5 ** 2))
