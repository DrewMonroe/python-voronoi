#!/usr/bin/env python3

"""This is a collection of linear predicate implementations.

It also has basic stuff like 'lift' and 'norm', and also a thing
to make vectors / document how we should make vectors.
"""

import numpy as np
# from scipy import linalg # supposedly faster, but doesn't have everything
from numpy import linalg  # for accurate sign of det, hopefully
from matrix import Matrix
from vector import Vector


def ccw(*vectors):
    """tests if triangle a, b, c is oriented counterclockwise.

    Returns 1 if ccw, 0 if colinear, -1 if cw.

    Also does the scary analogous n-dimensional test.
    """
    m = Matrix(*[vector.lift() for vector in vectors])
    return int(np.sign(m.det()))


def incircle(*vectors):  # a, b, c, d):
    """In R^2, is the last argument inside the circle defined by the
    previous arguments?
    1 if inside, -1 if outside, and 0 if all cocircular.
    """

    return ccw(*[v.lift(v.norm_squared) for v in vectors]) * ccw(*vectors[:-1])
