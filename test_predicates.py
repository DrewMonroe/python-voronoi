"""Unittests for the predicates"""
import unittest

#import numpy as np
# from predicates import as_columns
# from predicates import ccw
# from predicates import equal
# from predicates import incircle
# from predicates import lift_matrix
# from predicates import matrix
# from predicates import vector
from point import Point # fix these imports, of course
from vector import Vector

class PredicatesTestCase(unittest.TestCase):
    """Unit tests for the predicates and related objects."""

    def setUp(self):
        """Make some objects that are useful for most tests."""
        # Used to test incircle and foo
        self.r2north = Vector(0, 1)
        self.r2east = Vector(1, 0)
        self.r2south = Vector(0, -1)
        self.r2west = Vector(-1, 0)
        self.r2orig = Vector(0, 0)

    def test_equal(self):
        """Tests the predicate for equality of vectors/matrices."""
        self.assertTrue(equal(Vector(0, -9, 1600002),
                              Vector(0, -9, 1600002)))
        self.assertTrue(equal(matrix([0, 1], [-1, -2]),
                              matrix([0, 1], [-1, -2])))
        self.assertFalse(equal(matrix([0, 1], [-1, -2]),
                               matrix([0, 1], [-1, -5])))
        # shouldn't throw errors if things are different sizes
        self.assertFalse(equal(matrix([0, 1], [-1, -2]),
                               matrix([0, 1, 2],
                                      [-1, -2, 10],
                                      [48, 20, 1])))
        self.assertFalse(equal(matrix([0, 1], [-1, -2]),
                               matrix([0, 1, -1], # paranoia seems wise
                                      [-2, 0, 0],
                                      [0, 0, 0])))
        self.assertFalse(equal(Vector(0, 1, 2), Vector(1, 2)))


    # def test_as_columns(self):
    #     """Test the thing that joins column vectors into a matrix."""
    #     target = matrix([1, 2, 3],
    #                     [4, 5, 6],
    #                     [7, 8, 9])
    #     col1 = Vector(1, 4, 7)
    #     col2 = Vector(2, 5, 8)
    #     col3 = Vector(3, 6, 9)
    #     self.assertTrue(equal(target, as_columns(col1, col2, col3)))


    def test_Vector(self):
        """Test our standard function for making column vectors"""
        self.assertEqual(len(Vector(0, 1, 2)), 3)
        self.assertTrue(Vector(0, 1, 2)) # might fail. numpy is a pain.
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
        self.assertEqual((ccw(one_dim_high, one_dim_low)
                          * ccw(one_dim_low, one_dim_high)),
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

        # Warn us when we make non-square matrices
        self.assertRaises(Exception, ccw, self.r2west, self.r2south,
                          self.r2north, self.r2east)
        self.assertRaises(Exception, ccw, self.r2orig, self.r2south)

    def test_incircle(self):
        """Test the incircle predicate (currently in the plane only)"""

        r2far_east = Vector(50, -0.5)

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
        vector_test = Vector(*list_test)
        matrix_test = matrix(list_test)
        self.assertTrue(equal(target, lift_matrix(base, list_test)))
        self.assertTrue(equal(target, lift_matrix(base, vector_test)))
        self.assertTrue(equal(target, lift_matrix(base, matrix_test)))

