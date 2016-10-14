"""Unittests for the predicates.

Some of these are relics from an older design.
"""

import unittest

from pyVor.primitives import Point, Vector, Matrix
from pyVor.predicates import incircle


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

    def test_incircle(self):
        """Test the incircle predicate."""
        # TODO - Add tests with extended homogeneous coordinates

        # Not sure if I like this part, but I don't have time to make
        # this make sense.
        a = Point(1, 0)
        b = Point(0, 1)
        c = Point(-1, 0)
        d = Point(0, 0)
        self.assertTrue(incircle(a, b, c, d) == 1)
        self.assertTrue(incircle(a, b, d, c) == -1)
        self.assertTrue(incircle(a, b, c, c) == 0)

        r2far_east = Point(50, -0.5)

        # circle of radius 0... ought to be 0 (co-circular)
        self.assertEqual(incircle(self.r2east, self.r2east, self.r2east,
                                  self.r2east), 0)

        # The origin is in fact inside the (counterclockwise) unit circle
        self.assertEqual(incircle(self.r2east, self.r2north, self.r2west,
                                  self.r2orig), 1)

        # SHOULD depend on orientation of circle, so we can
        # have stuff like inside-out circles
        self.assertNotEqual(incircle(self.r2east, self.r2west, self.r2north,
                                     self.r2orig),
                            incircle(self.r2west, self.r2east, self.r2north,
                                     self.r2orig))
        self.assertNotEqual(incircle(self.r2east, self.r2north, self.r2west,
                                     self.r2orig),
                            incircle(self.r2west, self.r2east, self.r2north,
                                     self.r2orig))

        # Finitely faraway pt not in (counterclockwise) unit circle
        self.assertEqual(incircle(self.r2north, self.r2west, self.r2east,
                                  r2far_east), -1)
        # Finitely faraway pt is in the clockwise (inside-out) unit circle
        self.assertEqual(incircle(self.r2west, self.r2north, self.r2east,
                                  r2far_east), 1)

    '''
    I hate giant commented sections of code too. Don't worry, when we merge
    this to master with actual tests it will be fixed

    def test_as_columns(self):
        """Test the thing that joins column Vectors into a matrix."""
        target = matrix([1, 2, 3],
                        [4, 5, 6],
                        [7, 8, 9])
        col1 = Vector(1, 4, 7)
        col2 = Vector(2, 5, 8)
        col3 = Vector(3, 6, 9)
        self.assertTrue(equal(target, as_columns(col1, col2, col3)))

    def test_Vector(self):
        """Test our standard function for making column Vectors"""
        self.assertEqual(len(Vector(0, 1, 2)), 3)
        self.assertTrue(Vector(0, 1, 2))  # might fail. numpy is a pain.
        # self.assertTrue(Vector(0, 1, 2).any()) # feels like admitting defeat
        # depends how we want to use it:
        # self.assertTrue(Vector(0, 0, 0).any())

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


    def test_lift_matrix(self):
        """Tests the lift_matrix function."""
        target = matrix([0, 1, 2],
                        [3, 4, 5],
                        [6, 7, 8])
        base = matrix([0, 1, 2],
                      [3, 4, 5])
        # It will be nice if we can just throw whatever data type makes
        # sense into this function, so let's make sure that happens.
        list_test = [6, 7, 8]
        Vector_test = Vector(*list_test)
        matrix_test = matrix(list_test)
        self.assertTrue(equal(target, lift_matrix(base, list_test)))
        self.assertTrue(equal(target, lift_matrix(base, Vector_test)))
        self.assertTrue(equal(target, lift_matrix(base, matrix_test)))
'''

if __name__ == "__main__":
    unittest.main()
