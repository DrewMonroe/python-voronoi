#!/usr/bin/env python3

"""This is a collection of linear predicate implementations.

It also has basic stuff like 'lift' and 'norm', and also a thing
to make vectors / document how we should make vectors.
"""

# from scipy import linalg # supposedly faster, but doesn't have everything
from pyVor.primitives import Matrix, Vector, Point


def ccw(*points, homogeneous=True):
    """tests if triangle a, b, c is oriented counterclockwise.

    Returns 1 if ccw, 0 if colinear, -1 if cw.

    Also does the scary analogous n-dimensional test, which
    essentially tests if, from the perspective of the last point,
    the other points appear to be well-oriented according
    to the (n-1)-dimensional test.
    """
    if not homogeneous:
        mtrx = Matrix(*[pt.lift(lambda v: 1).to_vector() for pt in points])
    else:
        mtrx = Matrix(*[pt.to_vector() for pt in points])
    return mtrx.sign_det()


def incircle(*points, homogeneous=True):
    """In R^2, is the last argument inside the circle defined by the
    previous arguments?
    1 if inside, -1 if outside, and 0 if all cocircular.

    The points are interpreted as having extended homogenious
    coordinates unless homogeneous=False is passed.
    """
    # if debug and homogeneous:
    #     # Checking for human error. Eventually we can turn debug off.
    #     if not sum([p[-1] == 1 or p[-1] == 0 for p in points]):
    #         raise ValueError("These points are not homogeneous!")

    if homogeneous:
        # The points already have homogeneous coordinates
        vectors = [pt - Point(*([0] * len(pt))) for pt in points]
    else:
        # We'll give each point a homogeneous coordinate of 1
        vectors = [(pt - Point(*([0] * len(pt)))).lift() for pt in points]

    vectors = [vector.lift(lambda v: v[:-1].norm_squared())
               for vector in vectors]
    # At this point we could switch the last two elements of each
    # vector to get the matrix we want to test. But we can
    # also just use the fact that if you swap 2 rows of a
    # matrix, the sign of the determinant is flipped. So:
    return - Matrix(*vectors).sign_det()
