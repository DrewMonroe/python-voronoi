"""Unittests for the predicates"""
import unittest

#import numpy as np
from predicates import mkvector
from predicates import ccw
from predicates import incircle

class PredicatesTestCase(unittest.TestCase):
    """Unit tests for the predicates and related objects."""

    def setUp(self):
        """Make some objects that are useful for most tests."""
        # Used to test incircle and foo
        self.r2north = mkvector(0, 1)
        self.r2east = mkvector(1, 0)
        self.r2south = mkvector(0, -1)
        self.r2west = mkvector(-1, 0)
        self.r2orig = mkvector(0, 0)


    @unittest.skip("No tests for mkvector")
    def test_mkvector(self):
        """Test our standard function for making column vectors"""
        raise NotImplementedError

    def test_ccw(self):
        """Right now this only tests ccw for 1 and 2 dimensions."""

        # one-dimensional test.

        one_dim_high = mkvector(1)
        one_dim_low = mkvector(0)
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

        r2far_east = mkvector(50, -0.5)

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
