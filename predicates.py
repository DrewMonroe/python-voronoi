#!/usr/bin/env python3

"""This is a collection of linear predicate implementations.

It also has basic stuff like 'lift' and 'norm', and also a thing
to make vectors / document how we should make vectors.
"""

import numpy as np
#from scipy import linalg # supposedly faster, but doesn't have everything
from numpy import linalg # for accurate sign of det, hopefully

def vector(*values):
    """Make a column vector (secretly a numpy array)"""
    return np.array([[v] for v in values])

def matrix(*rows):
    """Make a matrix with the given rows."""
    return np.array(rows)

def equal(matrix0, matrix1):
    """Test matrices/vectors for equality.

    This matters because numpy doesn't let you use == because of
    ambiguity.
    """
    return (matrix0.shape == matrix1.shape and
            np.equal(matrix0, matrix1).all())

def as_columns(*vectors):
    """Return a matrix with those vectors as columns.

    Non-distructive - copies everything.
    """
    return np.concatenate(vectors, axis=1)


def lift(vect, function=(lambda *args: 1)):
    """Takes a column vector vect (np.ndarray) and lifts it using function.

    Check out this sweet syntax!
    """
    # both commented with value returned by timeit.timeit(...)
    # timeit.timeit(setup='''import numpy as np
    # column = np.array([[i] for i in range(10)])''',
    # stmt='np.array([*column, [7]])')
    # or stmt='np.append(column, np.array(7, axis=0

    # return np.array([*vector, function(vector)]) # 11.9s
    return np.append(vect, np.array([[function(vect)]]),
                     axis=0) # 8.7s

def sign_det(mtrx):
    """Return just the sign (-1, 0, 1) of the determinant of matrix mtrx.

    Hopefully this can be optimized to be faster than a full computation
    of the determinant. (TODO)
    https://math.stackexchange.com/questions/693948/simple-
    way-to-find-the-sign-of-a-determinant-given-a-singular-
    value-decompositio
    """
    # def sign(x): # This version should be faster by 15%
    #     if abs(x) < 0.000000001: # arbitrary, might break things
    #         return 0
    #     elif x < 0:
    #         return -1
    #     else:
    #         return 1
    # return sign(linalg.det(mtrx))
    return linalg.slogdet(mtrx)[0]

def ccw(*vectors):
    """tests if triangle a, b, c is oriented counterclockwise.

    Returns 1 if ccw, 0 if colinear, -1 if cw.

    Also does the scary analogous n-dimensional test.
    """
    #print([lift(x, lambda *args: 1) for x in [a, b, c]])
    return sign_det(np.concatenate(
        [lift(x, lambda arg: 1) for x in vectors],
        axis=1))

def norm_squared(column):
    """The dot-product norm on R^d. Used by incircle."""
    # This one might not be good/useful, but is handy for reference.
    return column.T.dot(column)[0][0]

def incircle(*vectors):#a, b, c, d):
    """In R^2, is the last argument inside the circle defined by the
    previous arguments?
    1 if inside, -1 if outside, and 0 if all cocircular.
    """

    return (ccw(*[lift(v, norm_squared) for v in vectors]) *
            ccw(*vectors[:-1])) # eliminate dependence on orienation of circle


def lift_matrix(base_matrix, last_row):
    """Append a given row to the bottom of a matrix.

    The row will be flattened, which is convenient only when you weren't
    making a 3-D matrix. (I hope it never comes to that anyway.)
    """
    return np.append(base_matrix, last_row, axis=0) # fails the test

# def not_enough_tests():
#     # This is some test code. It's not enough test code.
#     # We should write more.
#     a = np.array([[1], [1]])
#     b = np.array([[0], [0]])
#     c = np.array([[0], [1]])
#     d = np.array([[-1], [-1]])
#     print(d.T.dot(d))
#     assert np.equal(lift(a), np.array([[1], [1], [1]])).all()
#     assert ccw(c, b, a) == 1
#     assert ccw(c, b, d) == -1
#     assert ccw(b, a, d) == 0
#     print(incircle(d, a, c, b))

#     w = np.array([[1], [2], [3]])
#     x = np.array([[4], [5], [6]])
#     y = np.array([[7], [8], [9]])
#     z = np.array([[10], [11], [12]])
#     print(ccw(w, x, y, z)) # 0. Hopefully that's right.

# if __name__ == '__main__':
#     not_enough_tests()
