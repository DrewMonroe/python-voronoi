#!/usr/bin/env python3

"""This is a collection of linear predicate implementations."""

from pyVor.primitives import Matrix, Point, Vector


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
        mtrx = None
        for pt in points:
            if pt[-1] == 1:
                # We need at list one non-infinite point
                # for this to work normally
                mtrx = Matrix(*[pt.to_vector() for pt in points])
                break
    if mtrx is not None:
        return mtrx.sign_det()
    # If all points have 0 for extended homogeneous coordinate,
    # win by using the ccw test for one dimension higher:
    return ccw(*points,
               Point(*(0 for i in range(len(points[0]) - 1)), -1),
               homogeneous=False)


def incircle(*points, homogeneous=True):
    """Returns 1 if the last point is inside the circle defined by the other
    three, -1 if outside, and 0 if all cocircular.

    The points are interpreted as having extended homogenious
    coordinates unless homogeneous=False is passed.

    If multiple points are at infinity, incircle isn't necessarily
    well-defined, so we had to make something up. Essentially we only consider
    one point at a time to be at infinity, and we see if all the resulting
    tests agree with each other. Mostly this means we return 0. In 2
    dimensions, with two infinite points, this results in an X shaped partition
    of the plane, where two faces are 0s, one is 1, and one is -1.
    """

    if homogeneous:
        # The points already have homogeneous coordinates
        vectors = [pt.to_vector() for pt in points]
    else:
        # We'll give each point a homogeneous coordinate of 1
        vectors = [(pt.to_vector()).lift() for pt in points]

    vectors = [vect.lift(lambda v: v[:-1].norm_squared()) for vect in vectors]

    infinite_count = 0
    for vect in vectors:
        if vect[-2] == 0:  # this is the homogeneous coordinate
            infinite_count += 1

    if infinite_count is 0:
        return - Matrix(*vectors).sign_det()  # the easy case

    else:
        # I'll probably need to make a matrix of finite points equivalent
        # to the infinite ones, although I'm testing the easy way first.
        # That part should/will go right here.
        # Wow, never mind, the tests pass.
        results = set()
        for i in range(len(vectors)):
            if vectors[i][-2] == 0:
                new = [*vectors[:i],
                       # notice the negative coord here to cancel
                       # the rows having been swapped
                       Vector(*([0] * (len(vectors) - 1)), -1),
                       *vectors[i+1:]]
                results.add(Matrix(*new).sign_det())

        return sum(results)  # will be -1, 0, or 1
