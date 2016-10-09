"""Unittests for the predicates. Some of these are relics from an older design."""
import unittest

# import numpy as np
from primitives import Point


class PredicatesTestCase(unittest.TestCase):
    """Unit tests for the predicates and related objects."""

    def setUp(self):
        """Make some objects that are useful for most tests."""
        self.a = Point(0, 0)
        self.b = Point(1, 2)
        self.c = Point(1, 2, 3)

    def test_point(self):
        # Make sure that we can evaluate a point to True
        self.assertTrue(self.a)

        # Test to see if length of a point makes sense
        self.assertTrue(len(self.c) == 3)
        self.assertTrue(len(Point(1, 2, 3, 4)) == 4)
        self.assertFalse(len(self.b) == 3)

        # Make sure that we can access elements of a point by index
        self.assertTrue(self.a[0] == 0)
        self.assertTrue(self.c[2] == 3)
        self.assertFalse(self.b[-1] == 10)

        # Test point equality
        self.assertFalse(self.a == self.b)
        self.assertTrue(self.b == self.b)
        self.assertTrue(self.c == Point(1, 2, 3))
        self.assertFalse(self.b == self.c)
        self.assertFalse(self.b == (1, 2))

        # Test point subtraction
        self.assertTrue(self.b - self.b == Vector(0, 0))
        self.assertTrue(self.b - self.a == Vector(1, 2))

        # Test turning points into vectors
        self.assertTrue(self.c.to_vector() == Vector(1, 2, 3))
        self.assertTrue(self.a.to_vector() == Vector(0, 0))
        self.assertTrue(self.b.to_vector() == Vector(1, 2))
        self.assertFalse(self.b.to_vector() == Vector(1, 2, 0))
    '''
    I hate giant commented sections of code too. Don't worry, when we merge
    this to master with actual tests it will be fixed
    def test_as_columns(self):
        """Test the thing that joins column vectors into a matrix."""
        target = matrix([1, 2, 3],
                        [4, 5, 6],
                        [7, 8, 9])
        col1 = vector(1, 4, 7)
        col2 = vector(2, 5, 8)
        col3 = vector(3, 6, 9)
        self.assertTrue(equal(target, as_columns(col1, col2, col3)))

    def test_vector(self):
        """Test our standard function for making column vectors"""
        self.assertEqual(len(vector(0, 1, 2)), 3)
        self.assertTrue(vector(0, 1, 2))  # might fail. numpy is a pain.
        # self.assertTrue(vector(0, 1, 2).any()) # feels like admitting defeat
        # depends how we want to use it:
        # self.assertTrue(vector(0, 0, 0).any())

    def test_ccw(self):
        """Right now this only tests ccw for 1 and 2 dimensions."""
        # one-dimensional test.

        one_dim_high = vector(1)
        one_dim_low = vector(0)
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

    def test_incircle(self):
        """Test the incircle predicate (currently in the plane only)"""

        r2far_east = vector(50, -0.5)

        # circle of radius 0... ought to be 0 (co-circular)
        self.assertEqual(incircle(self.r2east, self.r2east, self.r2east,
                                  self.r2east), 0)

        self.assertEqual(incircle(self.r2east, self.r2west, self.r2north,
                                  self.r2orig), 1)

        # Shouldn't depend on orientation of circle
        self.assertEqual(incircle(self.r2east, self.r2west, self.r2north,
                                  self.r2orig),
                         incircle(self.r2west, self.r2east, self.r2north,
                                  self.r2orig))
        self.assertEqual(incircle(self.r2east, self.r2north, self.r2west,
                                  self.r2orig),
                         incircle(self.r2west, self.r2east, self.r2north,
                                  self.r2orig))

        # faraway pt not in circle
        self.assertEqual(incircle(self.r2north, self.r2west, self.r2east,
                                  r2far_east), -1)

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
        vector_test = vector(*list_test)
        matrix_test = matrix(list_test)
        self.assertTrue(equal(target, lift_matrix(base, list_test)))
        self.assertTrue(equal(target, lift_matrix(base, vector_test)))
        self.assertTrue(equal(target, lift_matrix(base, matrix_test)))
    '''
if __name__ == "__main__":
    unittest.main()
