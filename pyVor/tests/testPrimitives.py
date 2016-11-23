"""Unit tests for the classes defined in the primitives package"""

import unittest

from pyVor.primitives import Point, Vector, Matrix


class VectorTestCase(unittest.TestCase):
    """Unit tests for the Vector class."""

    def setUp(self):
        """Make some 10-dimensional vectors to play with."""
        # Some vectors, for when the particular values don't matter.
        # Note that if v1, v2, or v3 is the zero vector, tests will
        # fail despite correct behavior.
        # But that's pretty remarkably improbable unless random.random
        # is the absolute worst.
        self.v1 = Vector(*[1.25 * i for i in range(10)])
        self.v2 = Vector(*[-0.125 * i for i in range(10)])
        self.zero_v = Vector(*([0] * 10))  # 10-dimensional 0 vector

    def test_vector_length(self):
        """Tests to make sure we can take the length of vectors"""
        self.assertTrue(len(self.v1) == 10)
        self.assertTrue(len(Vector(0, 1, 2)) == 3)
        self.assertFalse(len(self.v1) == len(Vector(0)))

    def test_vector_equal(self):
        """Tests comparison of vectors for equality"""
        # Same values --> equal
        self.assertTrue(Vector(0, -9, 11.2) == Vector(0, -9, 11.2))
        self.assertFalse(Vector(0, -9, 1600002) == Vector(0, -8, 1600002))
        # Different values should not be equal
        self.assertFalse(Vector(1, 4) == Vector(1, 4, 5))
        # Make sure that vectors of different lengths aren't equal
        self.assertFalse(Vector(1, 2, 3) == Vector(1, 2))

    def test_weird_edge_cases(self):
        """Tests stuff that is just plain weird but might matter.

        Yeah, I know, this is non-standard. Avoid adding to it.
        """
        # I've never heard the phrase "the empty vector"
        # before, and in fact I never expect to make one on purpose.
        # So I want to know if I make one by accident.
        with self.assertRaises(ValueError):
            Vector()

        # For now, I'm going to say we shouldn't be able to set components of
        # a vector like this
        with self.assertRaises(Exception):
            Vector(0, 1, 2)[0] = 10

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
        with self.assertRaises(ValueError):
            Vector(1, 2, 3) + Vector(1, 2)
        # small + Big:
        with self.assertRaises(ValueError):
            Vector(1, 2) + Vector(1, 2, 3)

        # Adding totally weird stuff to a vector should also raise errors
        # It doesn't matter what error, really.
        with self.assertRaises(Exception):
            Vector(1, 2, 3) + None

    def test_vector_subtraction(self):
        """Tests if subtraction works properly"""

        # Result of subtraction is a vector
        self.assertIsInstance(self.v1 - self.v2, Vector)

        # A few simple cases that should pass
        self.assertEqual(Vector(1, 3) - Vector(0, 3), Vector(1, 0))
        self.assertEqual(Vector(500) - Vector(400), Vector(100))

        # Should only work on vectors of like sizes
        # big - small
        with self.assertRaises(ValueError):
            Vector(1, 2, 3) - Vector(1, 2)
        # small - big
        with self.assertRaises(ValueError):
            Vector(1, 2) - Vector(1, 2, 3)

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

        # Make sure the side that the multiplication is done on doesn't matter
        self.assertTrue(self.v1 * 3 == 3 * self.v1)
        # Make sure that multiplying by 0 yields the 0 vector
        self.assertTrue(Vector(1, 1, 5, 0) * 0 == Vector(0, 0, 0, 0))

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
        with self.assertRaises(IndexError):
            my_vector[len(my_vector)]

        self.assertIsInstance(my_vector[:-1], Vector)

    def test_norm_squared(self):
        """Make sure that the norm_squared is right"""
        zero_v = self.zero_v
        # The norm of the zero vector should be 0
        self.assertTrue(zero_v.norm_squared() == 0)
        # If a vector is a unit vector, the norm should be 1
        self.assertTrue(Vector(1, 0, 0).norm_squared() == 1)
        self.assertTrue(Vector(0, 1, 0).norm_squared() == 1)
        self.assertTrue(Vector(0, 0, 1).norm_squared() == 1)
        # The order of the components shouldn't matter
        self.assertTrue(Vector(2, 3, 1, 5).norm_squared() ==
                        Vector(5, 2, 3, 1).norm_squared())
        # The norm quared of anything must be greater than or equal to 0
        self.assertFalse(Vector(-1, -1, -1).norm_squared() < 0)
        self.assertFalse(Vector(-1000, 0, 0, 0, -10).norm_squared() < 0)

        # Do some actual tests with vectors
        self.assertTrue(Vector(2, 2).norm_squared() == 8)
        self.assertTrue(Vector(3, 3, 3).norm_squared() == 27)
        # If you remove a multiplicitive constant, then the norm squared is
        # the the old norm squared divided by the square of the constant
        self.assertTrue(Vector(1, 1, 1).norm_squared() == 27 / 9)
        self.assertTrue(Vector(-1, -1, -1).norm_squared() ==
                        Vector(1, 1, 1).norm_squared())

    def test_vector_lift(self):
        """Test to make sure that we can lift a Vector"""
        # Make sure that lifting a vector results in a Vector
        self.assertIsInstance(Vector(1, 1, 1).lift(), Vector)

        # Define a function to test lifting with
        def f(x):
            return x[0] * 2

        self.assertTrue(Vector(2, 2).lift(f) == Vector(2, 2, 4))
        self.assertTrue(Vector(2, 2, 8).lift(f) == Vector(2, 2, 8, 4))


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
        self.assertTrue(Point(1, 2, 3) == Point(1, 2, 3))
        self.assertFalse(self.b == self.c)
        self.assertFalse(self.b == (1, 2))

    def test_misc_niceties(self):
        """I don't want  the empty point to be a thing. You may disagree."""
        with self.assertRaises(ValueError):
            Point()  # Try to make an empty point.

        # Make sure that we can evaluate a point to True
        self.assertTrue(self.a)

    def test_lift(self):
        """Make sure lifting works nicely."""

        # Define a function to use for testing
        def f(x):
            return x[0] * 2
        self.assertTrue(self.b.lift(f) == Point(1, 2, 2))
        self.assertFalse(self.c.lift(f) == Point(1, 2, 3, 4))
        self.assertFalse(self.c.lift(f) == Point(1, 2, 3))

        # Make sure that lifting a Point returns a Point
        self.assertIsInstance(self.b.lift(f), Point)

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

        self.assertIsInstance(self.a[:-1], Point)

    def test_subtraction(self):
        """Test point subtraction"""
        self.assertIsInstance(self.b - self.a, Vector)
        self.assertTrue(self.b - self.b == Vector(0, 0))
        self.assertTrue(self.b - self.a == Vector(1, 2))
        self.assertFalse(self.b - self.b == Point(0, 0))

    def test_to_vector(self):
        """Test turning points into vectors"""
        self.assertEqual(self.c.to_vector(), Vector(1, 2, 3))
        self.assertEqual(self.a.to_vector(), Vector(0, 0))
        self.assertEqual(self.b.to_vector(), Vector(1, 2))
        self.assertNotEqual(self.b.to_vector(), Vector(1, 2, 0))

    def test_hashing(self):
        """Make sure point hashing works and does not cause collisions"""
        # Add 400 points' hashes to a set and make sure 400 things are in the
        # set
        some_hashes = set()
        for x in range(-10, 10):
            for y in range(-10, 10):
                some_hashes.add(hash(Point(x, y, 1)))
        self.assertEqual(len(some_hashes), 400)

        self.assertEqual(hash(Point(0, 1, 2)),
                         hash(Point(0, 1, 2)))


class MatrixTestCase(unittest.TestCase):
    """Unit tests for the Matrix class"""

    def setUp(self):
        """Set up some Vectors and Matrices"""
        self.v1 = Vector(1, 2, 3)
        self.v2 = Vector(1, 1, 1)
        self.v3 = Vector(9, 9)
        self.v4 = Vector(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        self.zero = Vector(0, 0, 0)
        self.v5 = Vector(1, 2)
        self.v6 = Vector(3, 4)
        self.v7 = Vector(5, 6)
        self.v8 = Vector(7, 8)
        self.v9 = Vector(4, 5, 6)
        self.m1 = Matrix(self.v1, self.v2, self.zero)
        self.m2 = Matrix(self.v1, self.v2)
        self.m3 = Matrix(self.v3, self.v3)
        self.m4 = Matrix(self.v5, self.v6)
        self.m5 = Matrix(self.v7, self.v8)
        self.m6 = Matrix(self.v1, self.v9, self.v2)
        self.I = Matrix(Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1))

    def test_matrix_init(self):
        """Make sure we cannot initialize matrices that don't make sense"""
        # Make sure the empty matrix can't exist
        with self.assertRaises(ValueError):
            Matrix()

        # Ensure failure if the vectors have different dimensions
        with self.assertRaises(ValueError):
            Matrix(self.v1, self.v2, self.v4)
        with self.assertRaises(ValueError):
            Matrix(self.v4, self.zero)
        with self.assertRaises(ValueError):
            Matrix(self.v1, self.v4, self.zero)

    def test_matrix_width(self):
        """Tests for matrix width"""
        self.assertTrue(self.m1.width() == 3)
        self.assertTrue(self.m2.width() == 2)

    def test_matrix_height(self):
        """Tests for matrix height"""
        self.assertTrue(self.m1.height() == 3)
        self.assertTrue(self.m2.height() == 3)
        self.assertTrue(self.m3.height() == 2)

    def test_matrix_get(self):
        """Test for getting vectors of a matrix"""
        self.assertTrue(self.m1[0] == self.v1)
        self.assertTrue(self.m1[1] == self.v2)
        self.assertTrue(self.m1[2] == self.zero)

    def test_matrix_iteration(self):
        """Test iteration of a matrix"""
        orig_list = [self.v1, self.v2, self.zero]
        other_list = [vector for vector in self.m1]
        self.assertTrue(orig_list == other_list)

    def test_matrix_multiplication(self):
        """Tests for matrix multiplication"""
        result1 = Matrix(Vector(23, 34), Vector(31, 46))
        self.assertTrue(self.m4 * self.m5 == result1)
        result2 = Matrix(Vector(3, 4, 5), Vector(9, 13, 17), Vector(2, 3, 4))
        self.assertTrue(self.m1 * self.m6 == result2)

    def test_vector_multiplication(self):
        """Tests for matrix, vector multiplication"""
        self.assertTrue(self.I*self.v1 == self.v1)
        result1 = Vector(7, 10)
        self.assertTrue(self.m4 * self.v5 == result1)

    def test_scalar_multiplication(self):
        """Tests for multiplication of a matrix and a scalar"""
        result1 = Matrix(Vector(2, 4, 6), Vector(2, 2, 2), Vector(0, 0, 0))
        self.assertTrue(2 * self.m1 == result1)
        self.assertTrue(2 * self.m1 == self.m1 * 2)

    def test_determinant(self):
        """Tests for calculating determinant of matrix"""
        self.assertTrue(self.m1.det() == 0)
        self.assertAlmostEqual(self.m5.det(), -2.0)
        # almostEqual to account for floating point

    def test_add_matrix(self):
        """Tests for addition of two matrices"""
        result1 = Matrix(Vector(2, 4, 6), Vector(5, 6, 7), Vector(1, 1, 1))
        self.assertTrue(self.m1 + self.m6 == result1)

    def test_subtract_matrix(self):
        """Tests for subtraction of two matrices"""
        result1 = Matrix(Vector(0, 0, 0),
                         Vector(-3, -4, -5),
                         Vector(-1, -1, -1))
        zero_matrix = Matrix(Vector(0, 0, 0), Vector(0, 0, 0), Vector(0, 0, 0))
        self.assertTrue(self.m1 - self.m6 == result1)
        self.assertTrue(self.m1 - self.m1 == zero_matrix)

    def test_equal(self):
        """Tests for equality of matrices"""
        self.assertTrue(self.m1 == self.m1)
        self.assertFalse(self.m1 == self.m6)
        self.assertFalse(self.m1 == self.m2)

    def test_transpose(self):
        """Tests for transpose of a matrix"""
        result1 = Matrix(Vector(1, 1, 0), Vector(2, 1, 0), Vector(3, 1, 0))
        result2 = Matrix(Vector(1, 4, 1), Vector(2, 5, 1), Vector(3, 6, 1))
        self.assertTrue(self.m1.transpose() == result1)
        self.assertTrue(self.m6.transpose() == result2)

    def test_matrix_power(self):
        """Tests for matrices to a power"""
        result1 = Matrix(Vector(3, 4, 5), Vector(2, 3, 4), Vector(0, 0, 0))
        self.assertTrue(self.m1 ** 2 == result1)
        self.assertTrue(self.m1 * self.m1 * self.m1 == self.m1 ** 3)

    def test_matrix_inversion(self):
        """Tests to see if matrix inversion works as expected"""
        inv1 = Matrix(Vector(-2, 1), Vector(1.5, -0.5))
        self.assertTrue(Matrix(self.v5, self.v6).inverse() == inv1)
        with self.assertRaises(ValueError):
            Matrix(self.zero, self.v1, self.v2).inverse()
        t1 = Vector(-1, 1, 2)
        t2 = Vector(-1, 3, 2)
        t3 = Vector(-1, 1, 3)
        inv2 = Matrix(Vector(-3.5, 0.5, 2),
                      Vector(-0.5, 0.5, 0),
                      Vector(-1, 0, 1))
        self.assertTrue(inv2 == Matrix(t1, t2, t3).inverse())
        inv3 = Matrix(Vector(-3.5, 2, 0.5),
                      Vector(-0.5, 0, 0.5),
                      Vector(-1, 1, 0))
        self.assertTrue(Matrix(t1, t3, t2).inverse() == inv3)

        self.assertEqual(Matrix(t1, t2, t3).inverse() * Matrix(t1, t2, t3),
                         Matrix(Vector(1, 0, 0),
                                Vector(0, 1, 0),
                                Vector(0, 0, 1)))

    def test_matrix_sign_det(self):
        """Tests that sign_det returns the sign of the determinant.

        (Rather, sign_det should return an integer with the same sign as the
        determinant.)
        """
        ident_3 = Matrix(Vector(1, 0, 0),
                         Vector(0, 1, 0),
                         Vector(0, 0, 1))
        # The following are just some cases where it's easy
        # to do the math in your head.
        self.assertEqual(ident_3.sign_det(),
                         1)
        self.assertEqual((ident_3 - ident_3).sign_det(),
                         0)
        # (A lower-triangular matrix. And don't forget it.)
        self.assertEqual(Matrix(Vector(1, 2, 3),
                                Vector(0, -12, 5),
                                Vector(0, 0, 0.001)).sign_det(),
                         -1)

        self.assertIsInstance(Matrix(Vector(1, 2),
                                     Vector(3, 4)).sign_det(),
                              int)

if __name__ == "__main__":
    unittest.main()
