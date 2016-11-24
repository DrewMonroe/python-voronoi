"""Unittests for the predicates.

Some of these are relics from an older design.
"""

import unittest

from pyVor.primitives import Point
from pyVor.predicates import incircle, ccw


class PredicatesTestCase(unittest.TestCase):
    """Unit tests for the predicates and related objects."""

    def setUp(self):
        """Make some objects that are useful for most tests."""
        # Make points on the unit circle in the plane
        # North, East, South, and West shouldn't bend your brain
        self.r2north = Point(0, 1)
        self.r2south = Point(0, -1)
        self.r2east = Point(1, 0)
        self.r2west = Point(-1, 0)
        self.r2orig = Point(0, 0)
        # Now the homogeneous version of the same thing (We use the plane z=1
        # to represent the plane R^2 but with a boundary (homeomorphic to a
        # circle). Points with z=0 are essentially infinitely far away. The
        # same idea works in higher dimensions.
        self.homo_north = Point(0, 1, 1)
        self.homo_south = Point(0, -1, 1)
        self.homo_east = Point(1, 0, 1)
        self.homo_west = Point(-1, 0, 1)
        self.homo_orig = Point(0, 0, 1)

    def test_incircle_euclidean(self):
        """Test the incircle predicate in the plane."""

        a = Point(1, 0)
        b = Point(0, 1)
        c = Point(-1, 0)
        d = Point(0, 0)
        self.assertTrue(incircle(a, b, c, d, homogeneous=False) == 1)
        self.assertTrue(incircle(a, b, d, c, homogeneous=False) == -1)
        self.assertTrue(incircle(a, b, c, c, homogeneous=False) == 0)

        r2far_east = Point(50, -0.5)

        # circle of radius 0... ought to be 0 (co-circular)
        self.assertEqual(incircle(self.r2east, self.r2east, self.r2east,
                                  self.r2east, homogeneous=False), 0)

        # The origin is in fact inside the (counterclockwise) unit circle
        self.assertEqual(incircle(self.r2east, self.r2north, self.r2west,
                                  self.r2orig, homogeneous=False), 1)

        # SHOULD depend on orientation of circle, so we can
        # have stuff like inside-out circles
        self.assertNotEqual(incircle(self.r2east, self.r2west, self.r2north,
                                     self.r2orig, homogeneous=False),
                            incircle(self.r2west, self.r2east, self.r2north,
                                     self.r2orig, homogeneous=False))
        self.assertNotEqual(incircle(self.r2east, self.r2north, self.r2west,
                                     self.r2orig, homogeneous=False),
                            incircle(self.r2north, self.r2east, self.r2west,
                                     self.r2orig, homogeneous=False))

        # Finitely faraway pt not in (counterclockwise) unit circle
        self.assertEqual(incircle(self.r2north, self.r2west, self.r2east,
                                  r2far_east, homogeneous=False), -1)
        # Finitely faraway pt is in the clockwise (inside-out) unit circle
        self.assertEqual(incircle(self.r2west, self.r2north, self.r2east,
                                  r2far_east, homogeneous=False), 1)

    def test_incircle_homogeneous(self):
        """Tests incircle on points with homogeneous coordinates
        (representing points in R^d but with a boundary)
        """
        far_east_finite = Point(50, 0, 1)
        far_east_infinite = Point(1, 0, 0)

        # Counterclockwise circle around origin contains origin:
        self.assertEqual(incircle(self.homo_east, self.homo_north,
                                  self.homo_south, self.homo_orig), 1)
        # But it shouldn't contain any faraway point:
        self.assertEqual(incircle(self.homo_east, self.homo_north,
                                  self.homo_south, far_east_finite), -1)
        self.assertEqual(incircle(self.homo_east, self.homo_north,
                                  self.homo_south, far_east_infinite), -1)
        # And of course, another point on the unit circle should be cocircular:
        self.assertEqual(incircle(self.homo_east, self.homo_north,
                                  self.homo_south, self.homo_west), 0)

        # Clockwise circle around origin does not contain origin:
        self.assertEqual(incircle(self.homo_north, self.homo_east,
                                  self.homo_south, self.homo_orig), -1)
        # But it SHOULD contain faraway points:
        self.assertEqual(incircle(self.homo_north, self.homo_east,
                                  self.homo_south, far_east_finite), 1)
        self.assertEqual(incircle(self.homo_north, self.homo_east,
                                  self.homo_south, far_east_infinite), 1)
        # Cocircular stuff should still be cocircular:
        self.assertEqual(incircle(self.homo_north, self.homo_east,
                                  self.homo_south, self.homo_west), 0)

        # Check for subtle arithmetic errors:
        self.assertEqual(incircle(Point(0, -10, 1),
                                  Point(0, 0, 1),
                                  Point(-0.001, 10, 1),
                                  Point(-0.0005, 10, 1)),
                         -1)

        # Counterclockwise infinite triangle contains everything
        inf_triangle = [Point(1, 0, 0), Point(-1, 1, 0), Point(-1, -1, 0)]

        self.assertEqual(incircle(*inf_triangle, Point(12, -14, 1)),
                         1)
        self.assertEqual(incircle(*inf_triangle, Point(-1, 1, 1)),
                         1)

        # Clockwise infinite triangle contains nothing
        self.assertEqual(incircle(*inf_triangle[::-1], Point(12, -14, 1)),
                         -1)
        self.assertEqual(incircle(*inf_triangle[::-1], Point(-1, 1, 1)),
                         -1)

        # Tricky cases:
        self.assertEqual(incircle(
            Point(-1, -1, 0), Point(-3, 2, 1), Point(1, 0, 0), Point(0, 1, 0)),
                         1)
        self.assertEqual(incircle(
            Point(-3, 2, 1), Point(-1, -1, 0), Point(1, 0, 0), Point(0, 1, 0)),
                         -1)

        # The following tests are based on pencil-and-paper drawings
        # as well as hours spent debugging the DelaunayTriangulation.

        self.assertEqual(incircle(
            Point(1, 0, 0), Point(-0.6, 3.2, 1), Point(3.2, 2.1, 1),
            Point(-2, 0, 1)),
                         -1)

        self.assertEqual(incircle(
            Point(-2, 0), Point(-0.6, 3.2), Point(0, 1, 0), Point(1, 0, 0)),
                         -1)

    def test_ccw_euclidean(self):
        """Right now this only tests ccw for 1 and 2 dimensions."""
        # one-dimensional test.

        one_dim_high = Point(1)
        one_dim_low = Point(0)
        # I don't much care which way is negative, but one had better be
        # positive and the other negative. And they'd better be ints. (Of
        # course, ccw in 1D is equivalent to numeric comparison.)
        self.assertEqual((ccw(one_dim_high, one_dim_low, homogeneous=False) *
                          ccw(one_dim_low, one_dim_high, homogeneous=False)),
                         -1)
        self.assertIsInstance((ccw(one_dim_high, one_dim_low,
                                   homogeneous=False) *
                               ccw(one_dim_low, one_dim_high,
                                   homogeneous=False)),
                              int)

        # co-hyperplanar --> 0
        self.assertEqual(ccw(one_dim_high, one_dim_high, homogeneous=False), 0)

        # Now for 2D stuff:

        # Invariance under rotation of args
        self.assertEqual(ccw(self.r2north, self.r2east, self.r2south,
                             homogeneous=False),
                         ccw(self.r2south, self.r2north, self.r2east,
                             homogeneous=False))

        self.assertEqual(ccw(self.r2north, self.r2east, self.r2south,
                             homogeneous=False), -1)
        self.assertEqual(ccw(self.r2east, self.r2south, self.r2west,
                             homogeneous=False), -1)
        self.assertEqual(ccw(self.r2south, self.r2north, self.r2orig,
                             homogeneous=False), 0)
        self.assertEqual(ccw(self.r2east, self.r2orig, self.r2east,
                             homogeneous=False), 0)
        self.assertEqual(ccw(self.r2west, self.r2east, self.r2south,
                             homogeneous=False), -1)
        self.assertEqual(ccw(self.r2west, self.r2south, self.r2north,
                             homogeneous=False), 1)

        # Swapping two args flips the sign
        self.assertEqual(ccw(self.r2west, self.r2south, self.r2north,
                             homogeneous=False),
                         -ccw(self.r2south, self.r2west, self.r2north,
                              homogeneous=False))
        self.assertEqual(ccw(self.r2west, self.r2east, self.r2orig,
                             homogeneous=False),
                         -ccw(self.r2east, self.r2west, self.r2orig,
                              homogeneous=False))
        # Warn us when we make non-square matrices
        self.assertRaises(Exception, ccw, self.r2west, self.r2south,
                          self.r2north, self.r2east, homogeneous=False)
        self.assertRaises(Exception, ccw, self.r2orig, self.r2south,
                          homogeneous=False)

    def test_ccw_homogeneous(self):
        """Tests ccw with extended homogeneous coordinates"""
        # One dimensional case:

        # Basic, hair-not-on-fire requirement
        self.assertNotEqual(ccw(Point(0, 1), Point(1, 1)), 0)
        self.assertEqual(ccw(Point(0, 1), Point(1, 1)),
                         ccw(Point(0), Point(1), homogeneous=False))

        # With one homogeneous coordinate
        self.assertEqual(ccw(Point(0, 1), Point(1, 1)),
                         ccw(Point(-1, 0), Point(2, 1)))

        # With two homogeneous coordinates
        self.assertEqual(ccw(Point(0, 1), Point(1, 1)),
                         ccw(Point(-10, 0), Point(5, 0)))

        # Make sure simple stuff works
        # Should be counterclockwise:
        self.assertEqual(ccw(self.homo_north, self.homo_south, self.homo_east),
                         1)
        # Should be colinear:
        self.assertEqual(ccw(Point(1, 0, 1), Point(0, 0, 1), Point(-1, 0, 1)),
                         0)
        # Should be clockwise:
        self.assertEqual(ccw(self.homo_north, self.homo_east, self.homo_south),
                         -1)

        # Now try some weird stuff

        # Tests involving one infinitely distance point:
        self.assertEqual(ccw(Point(1, 0, 1), Point(0, 0, 1), Point(0, 1, 0)),
                         -1)

        # Tests involving two infinitely distance points:
        self.assertEqual(ccw(Point(1, 0, 0), Point(0, 0, 1), Point(0, 1, 0)),
                         -1)
        self.assertEqual(ccw(Point(0, 1, 0), Point(0, 0, 1), Point(1, 0, 0)),
                         1)

        # Test with three points on the "boundary of the plane"
        self.assertEqual(ccw(Point(0, 1, 0), Point(-1, 0, 0), Point(0, -1, 0)),
                         1)
        self.assertEqual(ccw(Point(0, 1, 0), Point(1, 0, 0), Point(0, -1, 0)),
                         -1)
        # Same but with weirder points
        self.assertEqual(ccw(Point(1.8, 19, 0),
                             Point(309.7, 1, 0),
                             Point(-0.05, -10, 0)),
                         -1)

        # ANY finite point must satisfy this:
        queries = [Point(0, 0, 1), Point(1232, 4, 1),
                   Point(-320, -0.0, 1), Point(-1, -1, 1),
                   Point(1, 0, 1), Point(0, 1, 1)]
        for query in queries:
            self.assertEqual(ccw(Point(0, 1, 0), Point(-1, -1, 0), query), 1)
            self.assertEqual(ccw(Point(1, 0, 0), Point(0, 1, 0), query), 1)

if __name__ == "__main__":
    unittest.main()
