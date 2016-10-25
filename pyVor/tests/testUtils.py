"""Unittests for the functions in utils."""

import unittest

from pyVor.primitives import Point, Vector, Matrix
from pyVor.utils import circumcenter


class UtilsTestCase(unittest.TestCase):

    def testCircumCenter(self):
        """ Tests for corect circumcenter """
        a = Point(1, 0)
        b = Point(0, 1)
        c = Point(0, -1)
        zero = Point(0.0, 0.0)
        center1 = circumcenter(a, b, c)
        self.assertTrue(type(center1) is Point)
        self.assertTrue(center1 == zero)
        d = Point(0, 0, 1)
        center2 = circumcenter(a.lift(lambda v: 0),
                               b.lift(lambda v: 0), c.lift(lambda v: 0), d)
        self.assertTrue(center2 == zero.lift(lambda v: 0.0))
        a = Point(1, 2)
        b = Point(2, 1)
        c = Point(1, 0)
        center3 = circumcenter(a, b, c)
        self.assertTrue(center3 == Point(1.0, 1.0))

if __name__ == "__main__":
    unittest.main()
