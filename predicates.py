#!/usr/bin/env python3

"""This is a collection of linear predicate implementations.

It also has basic stuff like 'lift' and 'norm', and also a thing
to make vectors / document how we should make vectors.
"""

import numpy as np
#from scipy import linalg # supposedly faster, but doesn't have everything
from numpy import linalg # for accurate sign of det, hopefully

def mkvector(*args):
    """This is honestly just supposed to document our convention
    for what a column vector is.
    I don't know if it's a good idea to use it.
    """
    return np.array([[x] for x in args])


def lift(vector, function=(lambda *args: 1)):
    """Takes a column vector (np.ndarray) and lifts it using function.

    Check out this sweet syntax!
    """
    # both commented with value returned by timeit.timeit(...)
    # timeit.timeit(setup='''import numpy as np
    # column = np.array([[i] for i in range(10)])''',
    # stmt='np.array([*column, [7]])')
    # or stmt='np.append(column, np.array(7, axis=0

    # return np.array([*vector, function(vector)]) # 11.9s
    return np.append(vector, np.array([[function(vector)]]),
                     axis=0) # 8.7s

def sign_det(matrix):
    """Return just the sign (-1, 0, 1) of the determinant of matrix.

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
    # return sign(linalg.det(matrix))
    return linalg.slogdet(matrix)[0]

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
    previous arguments? (TODO test this.)
    1 if inside, -1 if outside, and 0 if all cocircular.
    """

    return ccw(*[lift(v, norm_squared) for v in vectors])


def not_enough_tests():
    # This is some test code. It's not enough test code.
    # We should write more.
    a = np.array([[1], [1]])
    b = np.array([[0], [0]])
    c = np.array([[0], [1]])
    d = np.array([[-1], [-1]])
    print(d.T.dot(d))
    assert np.equal(lift(a), np.array([[1], [1], [1]])).all()
    assert ccw(c, b, a) == 1
    assert ccw(c, b, d) == -1
    assert ccw(b, a, d) == 0
    print(incircle(d, a, c, b))

    w = np.array([[1], [2], [3]])
    x = np.array([[4], [5], [6]])
    y = np.array([[7], [8], [9]])
    z = np.array([[10], [11], [12]])
    print(ccw(w, x, y, z)) # 0. Hopefully that's right.


if __name__ == '__main__':
    not_enough_tests()
