import unittest


from point import Point
from vector import Vector

import random # only used where I didn't feel like picking arbitrary numbers

class PrimitivesTestCase(unittest.TestCase):
    """Unit tests for the Vector class."""

    def setUp(self):
        """Make some 10-dimensional vectors to play with."""
        # Some vectors, for when the particular values don't matter.
        # Note that if v1, v2, or v3 is the zero vector, tests will
        # fail despite correct behavior.
        # But that's pretty remarkably improbable unless random.random
        # is the absolute worst.
        self.v1 = vector(*[(random.random() - 0.5) * 10 for i in range(10)])
        self.v2 = vector(*[(random.random() - 0.5) * 10 for i in range(10)])
        self.v3 = vector(*[(random.random() - 0.5) * 10 for i in range(10)])
        self.zero_v = vector(*([0] * 10)) # 10-dimensional 0 vector

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
            Vector() # make an empty vector
        

    def test_vector_arithmetic(self):
        """Tests if vector addition works properly."""

        # Some vectors, for when the particular values don't matter.
        # Note that if v1, v2, or self.v3 is the zero vector, tests will
        # fail despite correct behavior.
        # But that's pretty remarkably improbable unless random.random
        # is the absolute worst.
        v1 = vector(*[(random.random() - 0.5) * 10 for i in range(10)])
        v2 = vector(*[(random.random() - 0.5) * 10 for i in range(10)])
        self.v3 = vector(*[(random.random() - 0.5) * 10 for i in range(10)])
        zero_v = vector(*([0] * 10))

        # Test addition

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
        with self.assertRaises(ValueError):
            Vector(1, 2, 3) + Vector(1, 2)

        # Adding totally weird stuff to a vector should also raise errors
        with self.assertRaises(Exception):
            # I'm happy as long as this raises something at all
            Vector(1, 2, 3) + None

    def test_vector_subtraction(self):
        """Tests if subtraction works properly"""

        # Result of subtraction is a vector
        self.assertIsInstance(self.v1 - self.v2, Vector)

        # A few simple cases that should pass
        self.assertEqual(Vector(1, 3) - Vector(0, 3), Vector(1, 0))
        self.assertEqual(Vector(500) - Vector(400), Vector(300))

        # A few things could go horribly, horribly wrong such
        # that the following test fails:
        self.assertEqual(self.v2 - self.v1 + self.v1, self.v1 - self.v1 + self.v2)

        # Should only work on vectors of like sizes
        with self.assertRaises(ValueError):
            Vector(1, 2, 3) - Vector(1, 2) # big - small

        with self.assertRaises(ValueError):
            Vector(1, 2)  - Vector(1, 2, 3) # small - big

    # def test_scalar_multiplication(self):
    #     """There should be some way to multiply vectors by scalars."""

    def test_dot_products(self):
        """Tests vector dot products"""

        v1 = self.v1 # The code looks so much better with these short
        v2 = self.v2
        v3 = self.v3
        zero_v = self.zero_v

        # Symmetric
        self.assertEqual(v1.dot(v2), v2.dot(v1))

        # # Associative
        # self.assertEqual(v1.dot(v2.scale(5)),
        #                  v1.dot(v2).scale(5))
        # TODO - figure out our canonical way to
        # multiply a vector by a scalar here.

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
        """Make sure getting/setting by index works"""

        # Make sure OOP still works properly
        original = Vector(1, 2, 3)
        same_object = original
        original[0] = 4
        self.assertEqual(original, same_object)
        # Honestly... I don't know if we want a set-item.

class PointTestCase(unittest.TestCase):
    """Unit tests for the Point class."""

    def test_point_equal(self):
        """Tests if comparison of points for equality works"""
        self.assertTrue(Point(0, -9, 11.2) == Point(0, -9, 11.2))
        self.assertFalse(Point(0, -9, 1600002) == Point(0, -8, 1600002))
        # Different location
        self.assertFalse(Point(1, 4) == Point(1, 4, 5))


    def test_weird_edge_cases(self):
        """I don't want  the empty point to be a thing. Sue me."""
        with self.assertRaises(ValueError):
            Point() # Try to make an empty point. 

    def test_lift(self):
        """Make sure lifting works nicely. TODO"""
        pass
