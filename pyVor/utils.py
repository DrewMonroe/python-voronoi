"""
Utilities for pyVor.

These are different from predicates in that they are,
well, not linear predicates.
"""

from pyVor.primitives import Point, Vector, Matrix


def circumcenter(*points, homogeneous=True):
    """Computes a circumcenter for a set of n+1 points in n dimensions,
    ignoring the extended homogeneous coordinates.

    Unless you pass homogeneous=False, the last coordinate of each
    point will be lopped off. Behavior may not be defined if
    any of the homogeneous coordinates is not 1.
    """

    if homogeneous:
        if [pt[-1] for pt in points] != [1] * len(points):
            tmp = []
            for v in [p.to_vector() for p in points]:
                if v[-1] == 0:
                    # print(v)
                    v *= 1000000000
                tmp.append(v)
            # Just strip off the homogeneous coordinates.
            tmp = [v[:-1] for v in tmp]
            points = [Point(*v.to_array()) for v in tmp]
        else:
            points = [pt[:-1] for pt in points]

    vectors = [p - points[0] for p in points[1:]]
    A = Matrix(*vectors).transpose()
    p0_squared = points[0].to_vector().norm_squared()
    b = Vector(*[0.5 * (p.to_vector().norm_squared() - p0_squared)
                 for p in points[1:]])
    x = A.inverse() * b
    # If the arguments had homogeneous coordinates, we want to tack the extra
    # coordinate back on:
    return Point(*x, *([1] if homogeneous else []))
