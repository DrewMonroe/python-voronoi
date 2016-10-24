"""Unittests for the predicates.

Some of these are relics from an older design.
"""

import unittest

from pyVor.primitives import Point, Vector, Matrix
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
        # Now the homogeneous version of the same thing
        # (We use the plane z=1 to represent the projective
        # plane in a roundabout way. Points with z=0 are
        # essentially infinitely far away. Cool, right?)
        self.homo_north = Point(0, 1, 1)
        self.homo_south = Point(0, -1, 1)
        self.homo_east = Point(1, 0, 1)
        self.homo_west = Point(-1, 0, 1)
        self.homo_orig = Point(0, 0, 1)

    def test_incircle_plane(self):
        """Test the incircle predicate in the plane."""
        # TODO - Add tests with extended homogeneous coordinates

        # Not sure if I like this part, but I don't have time to make
        # this make sense.
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

    def test_incircle_projective(self):
        """Tests incircle on points with homogeneous coordinates
        (representing points in the projective plane)
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

        # Points at infinity should be colinear and thus also cocircular
        self.assertEqual(incircle(Point(1, 0, 0),
                                  Point(-1, 1, 0),
                                  Point(1, 1, 0),
                                  Point(2, 1, 0)),
                         0)


    def test_ccw(self):
        """Right now this only tests ccw for 1 and 2 dimensions."""
        # one-dimensional test.

        one_dim_high = Vector(1)
        one_dim_low = Vector(0)
        # I don't much care which way is negative, but one had better
        # be positive and the other negative. And they'd better be
        # ints.
        self.assertEqual((ccw(one_dim_high, one_dim_low) *
                          ccw(one_dim_low, one_dim_high)),
                         -1)
        # co-hyperplanar --> 0
        self.assertEqual(ccw(one_dim_high, one_dim_high), 0)

        # Now for 2D stuff:

        # Invariance under rotation of args
        self.assertEqual(ccw(self.r2north, self.r2east, self.r2south),
                         ccw(self.r2south, self.r2north, self.r2east))

        self.assertEqual(ccw(self.r2north, self.r2east, self.r2south), -1)
        self.assertEqual(ccw(self.r2east, self.r2south, self.r2west), -1)
        self.assertEqual(ccw(self.r2south, self.r2north, self.r2orig), 0)
        self.assertEqual(ccw(self.r2east, self.r2orig, self.r2east), 0)
        self.assertEqual(ccw(self.r2west, self.r2east, self.r2south), -1)
        self.assertEqual(ccw(self.r2west, self.r2south, self.r2north), 1)

        # Swapping two args flips the sign
        self.assertEqual(ccw(self.r2west, self.r2south, self.r2north),
                         -ccw(self.r2south, self.r2west, self.r2north))
        self.assertEqual(ccw(self.r2west, self.r2east, self.r2orig),
                         -ccw(self.r2east, self.r2west, self.r2orig))
        # Warn us when we make non-square matrices
        self.assertRaises(Exception, ccw, self.r2west, self.r2south,
                          self.r2north, self.r2east)
        self.assertRaises(Exception, ccw, self.r2orig, self.r2south)


if __name__ == "__main__":
    unittest.main()
