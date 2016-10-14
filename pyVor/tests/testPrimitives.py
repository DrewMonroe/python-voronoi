"""Unit tests for the classes defined in the primitives package"""

import unittest
import random  # only used where I didn't feel like picking arbitrary numbers

from pyVor.primitives import Point, Vector


class PrimitivesTestCase(unittest.TestCase):
    """Unit tests for the Vector class."""

    def setUp(self):
        """Make some 10-dimensional vectors to play with."""
        # Some vectors, for when the particular values don't matter.
        # Note that if v1, v2, or v3 is the zero vector, tests will
        # fail despite correct behavior.
        # But that's pretty remarkably improbable unless random.random
        # is the absolute worst.
        self.v1 = Vector(*[(random.random() - 0.5) * 10 for i in range(10)])
        self.v2 = Vector(*[(random.random() - 0.5) * 10 for i in range(10)])
        self.zero_v = Vector(*([0] * 10))  # 10-dimensional 0 vector

    def test_vector_equal(self):
        """Tests comparison of vectors for equality"""
        # Same values --> equal
        self.assertTrue(Vector(0, -9, 11.2) == Vector(0, -9, 11.2))
        self.assertFalse(Vector(0, -9, 1600002) == Vector(0, -8, 1600002))
        # Different values should not be equal
        self.assertFalse(Vector(1, 4) == Vector(1, 4, 5))

    def test_weird_edge_cases(self):
        """Tests stuff that is just plain weird but might matter.

        Yeah, I know, this is non-standard. Avoid adding to it.
        """
        # I've never heard the phrase "the empty vector"
        # before, and in fact I never expect to make one on purpose.
        # So I want to know if I make one by accident.
        with self.assertRaises(ValueError):
            Vector()

    def test_vector_arithmetic(self):
        """Tests if vector addition works properly."""

        # Result of addition is a vector
        self.assertIsInstance(self.v1 + self.v2, Vector)

        # Just a sanity-check example.
        self.assertEqual(Vector(1, 4, 5, 6) + Vector(4, 10, -3, 0),
                         Vector(5, 14, 2, 6))

        # Make sure this doesn't modify the vectors somehow
        self.assertNotEqual(self.v1 + self.v2, self.v1)

        # Test symmetry
        self.assertEqual(self.v1 + self.v2, self.v2 + self.v1)

        self.assertEqual(self.v1 + self.zero_v, self.v1)

        # Adding vectors from different vector spaces should raise errors
        # Big + small:
        self.assertRaises(ValueError, Vector(1, 2, 3).__add__, Vector(1, 2))
        # small + Big:
        self.assertRaises(ValueError, Vector(1, 2).__add__, Vector(1, 2, 3))

        # Adding totally weird stuff to a vector should also raise errors
        # It doesn't matter what error, really.
        self.assertRaises(Exception, Vector(1, 2, 3).__add__, None)

    def test_vector_subtraction(self):
        """Tests if subtraction works properly"""

        # Result of subtraction is a vector
        self.assertIsInstance(self.v1 - self.v2, Vector)

        # A few simple cases that should pass
        self.assertEqual(Vector(1, 3) - Vector(0, 3), Vector(1, 0))
        self.assertEqual(Vector(500) - Vector(400), Vector(100))

        # Should only work on vectors of like sizes
        # big - small
        self.assertRaises(ValueError, Vector(1, 2, 3).__sub__, Vector(1, 2))
        # small - big
        self.assertRaises(ValueError, Vector(1, 2).__sub__, Vector(1, 2, 3))

        # A few things could go horribly, horribly wrong such
        # that the following test fails:
        # Unfortunately it seems to be failing just because of floating
        # point arithmetic.
        self.assertEqual(self.v2 - self.v1 + self.v1,
                         self.v1 - self.v1 + self.v2)

    def test_scalar_multiplication(self):
        """There should be some way to multiply vectors by scalars."""

        self.assertEqual(1 * self.v1, self.v1 * 1)
        self.assertEqual(0 * self.v1, self.zero_v)
        self.assertIsInstance(5 * self.v1, Vector)

    def test_dot_products(self):
        """Tests vector dot products"""

        v1 = self.v1  # The code looks so much better with these short
        v2 = self.v2
        zero_v = self.zero_v

        # Symmetric
        self.assertEqual(v1.dot(v2), v2.dot(v1))

        # Associative with scalar multiplication
        self.assertEqual(v1.dot(v2 * 5),
                         v1.dot(v2) * 5)

        # Norm >= 0
        self.assertTrue(v1.dot(v1) >= 0)
        self.assertTrue(v2.dot(v2) >= 0)

        # zero is orthogonal to everything
        self.assertEqual(v1.dot(zero_v), 0)
        self.assertEqual(zero_v.dot(v1), 0)

        # Other things that should be orthogonal are so.
        self.assertEqual(Vector(1, 0).dot(Vector(0, 1)), 0)

    def test_iteration(self):
        """We wanted to be able to iterate over vectors"""

        # Make sure you get the elements in order.
        # Note that v1 was made by iterating over the elements of
        # a list.
        self.assertEqual(Vector(*[i for i in self.v1]), self.v1)

    def test_indexing(self):
        """Make sure accessing by index works"""
        my_vector = Vector(1, 2, 3, 4, 5)
        self.assertEqual(my_vector[0], 1)
        self.assertEqual(my_vector[-1], 5)


class PointTestCase(unittest.TestCase):
    """Unit tests for the Point class."""

    def setUp(self):
        """Make some objects that are useful for most tests."""
        self.a = Point(0, 0)
        self.b = Point(1, 2)
        self.c = Point(1, 2, 3)

    def test_point_equal(self):
        """Tests if comparison of points for equality works"""
        self.assertTrue(Point(0, -9, 11.2) == Point(0, -9, 11.2))
        self.assertFalse(Point(0, -9, 1600002) == Point(0, -8, 1600002))
        # Different location
        self.assertFalse(Point(1, 4) == Point(1, 4, 5))

        # Drew's tests:
        self.assertFalse(self.a == self.b)
        self.assertTrue(self.b == self.b)
        self.assertTrue(self.c == Point(1, 2, 3))
        self.assertFalse(self.b == self.c)
        self.assertFalse(self.b == (1, 2))

    def test_misc_niceties(self):
        """I don't want  the empty point to be a thing. You may disagree."""
        with self.assertRaises(ValueError):
            Point()  # Try to make an empty point.

        # Make sure that we can evaluate a point to True
        self.assertTrue(self.a)

    def test_lift(self):
        """Make sure lifting works nicely. TODO"""
        pass

    def test_length(self):
        """Test to see if length of a point makes sense"""
        self.assertTrue(len(self.c) == 3)
        self.assertTrue(len(Point(1, 2, 3, 4)) == 4)
        self.assertFalse(len(self.b) == 3)

    def test_indexing(self):
        """Make sure that we can access elements of a point by index"""
        self.assertTrue(self.a[0] == 0)
        self.assertTrue(self.c[2] == 3)
        self.assertFalse(self.b[-1] == 10)

        with self.assertRaises(Exception):
            # I want a warning when I accidentally try to set values:
            self.b[-1] = 10

    def test_subtraction(self):
        """Test point subtraction"""
        self.assertTrue(self.b - self.b == Vector(0, 0))
        self.assertTrue(self.b - self.a == Vector(1, 2))

    def test_to_vector(self):
        """Test turning points into vectors"""
        self.assertEqual(self.c.to_vector(), Vector(1, 2, 3))
        self.assertEqual(self.a.to_vector(), Vector(0, 0))
        self.assertEqual(self.b.to_vector(), Vector(1, 2))
        self.assertNotEqual(self.b.to_vector(), Vector(1, 2, 0))

if __name__ == "__main__":
    unittest.main()