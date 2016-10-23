from pyVor.primitives import Point, Vector, Matrix


def circumcenter(*points):
    vectors = [p-points[0] for p in points]
    del vectors[0]
    A = Matrix(*vectors)
    p0Squared = points[0].to_vector().norm_squared()
    b = Vector(*[0.5*(p.to_vector().norm_squared()-p0Squared)
                 for p in points[1:]])
    x = A.inverse() * b
    return Point(*x)
