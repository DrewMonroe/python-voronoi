"""Unit tests for the functions in utils."""

import unittest

from pyVor.primitives import Point, Vector, Matrix
from pyVor.utils import circumcenter


class UtilsTestCase(unittest.TestCase):

    def testCircumCenter(self):
        """Tests for the circumcenter utility"""

        # Make sure the unit circle is centered at the origin
        center1 = circumcenter(Point(1, 0), Point(0, 1), Point(0, -1),
                               homogeneous=False)
        self.assertIsInstance(center1, Point)
        self.assertEqual(center1, Point(0, 0))

        # Do the same but with the unit sphere in R^3
        center2 = circumcenter(Point(1, 0, 0), Point(0, 1, 0), Point(0, -1, 0),
                               Point(0, 0, 1), homogeneous=False)
        self.assertIsInstance(center2, Point)
        self.assertEqual(center2, Point(0, 0, 0))

        # Make sure it isn't just returning zero all the time
        center3 = circumcenter(Point(1, 2), Point(2, 1), Point(1, 0),
                               homogeneous=False)
        self.assertEqual(center3, Point(1.0, 1.0))

        # Now let's see how it deals with homogeneous coordinates

        # Since we haven't yet decided how/whether to deal with
        # *extended* homogeneous coordinates in particular
        # (i.e. Point(*values, 0)), we throw an exception.
        # If we decide what to do, we should replace the following
        # test with something more useful:
        self.assertRaises(NotImplementedError, circumcenter,
                          Point(1, 0, 1), Point(0, 1, 0), Point(0, -1, 1))

        # Now make sure homogeneous coordinates are properly ignored
        # if they are all 1. (But the point returned should be
        # of the same dimension as the input.)
        self.assertEqual(circumcenter(Point(2, 3, 1), Point(3, 2, 1),
                                      Point(2, 1, 1)),
                         Point(2, 2, 1))

        # We'll want this to pass once we get things fully working.
        # TODO: We'll probably want to rewrite this test once we get everything
        # figured out
        self.assertEqual(circumcenter(Point(0, 0, 1), Point(0, 1, 1),
                                      Point(2, 2, 0))[-1],
                         0)

if __name__ == "__main__":
    unittest.main()
