"""Unittests for the functions in utils."""

import unittest

from pyVor.primitives import Point, Vector, Matrix
from pyVor.utils import circumcenter


class UtilsTestCase(unittest.TestCase):

    def testCircumCenter(self):
        """ Tests for corect circumcenter """
        a = Point(0, 1)
        b = Point(1, 0)
        c = Point(0, -1)
        zero = Point(0.0, 0.0)
        center = circumcenter(a, b, c)
        self.assertTrue(type(center) is Point)
        self.assertTrue(center == zero)

if __name__ == "__main__":
    unittest.main()
