#!/usr/bin/env python3
"""
Unit tests for triangulation class
"""

from pyVor.primitives import Point, Vector
import unittest

class SimplexTestCase(unittest.TestCase):


class SimplicialComplexTestCase(unittest.TestCase):
    """Tests for simplicial complexes.

    Abstractly, a simplicial complex is a collection of simplices that,
    when you view each simplex as a set of vertices that define it,
    is closed under subset. Geometrically / topologically, a
    k-simplex is the convex closure the k+1 vertices that define it.

    In R^d, I'm calling the d-simplices "faces", the [d-1]-simplices
    "edges", and the 0-simplices "vertices".

    This... can't be used to represent Voronoi cells because all the
    faces have to have d vertices. Shucks. Time to make a polytope instead.
    """

    def setUp(self):
        """Setup for other tests.

        Implicitly specifies behavior for the constructor.

        It should be safe to write tests that will fail if the structures made
        here are altered, e.g. by adding more vertices to them. So don't alter
        these things.
        """
        # All points are specified with homogeneous coordinates as usual
        # All faces are specified manually for the constructor.
        self.one_d_sim_pts = [Point(-1, 0), Point(-5, 1), Point(-1, 1),
                              Point(0, 1), Point(4, 1), Point(5, 1),
                              Point(1, 0)]
        self.one_d_sim = SimplicialComplex(
            vertices=self.one_d_sim_pts,  # Faces in R^1 are intervals
            faces=[self.one_d_sim_pts[i:i+1]
                   for i in range(len(self.one_d_sim_pts) - 1)])
        # There's a subtlety here in that I only passed one instance
        # representing each distinct point to the constructor above.
        # So two points passed to the constructor were equal
        # iff they were the same instance. I will not do the same for 2-D,
        # so we can test other behavior.

        self.two_d_sim_pts = [Point(0, -1, 0), Point(1, 1, 0),
                              Point(-1, 1, 0),  # points at infinity
                              Point(0, 0, 1)]  # Keep it simple.
        self.two_d_sim = SimplicialComplex(
            vertices=self.two_d_sim_pts,
            # vertices of faces must be specified in CCW order.
            # Check: They should be [S, NE, 0], [NE, 0, NW],  [NW, S, 0]
            # (Also notice if you consider their centers, the faces are
            #  also passed in CCW order in a sense.)
            faces=[[Point(0, -1, 0), Point(1, 1, 0), Point(0, 0, 1)],
                   [Point(1, 1, 0), Point(0, 0, 1), Point(-1, 1, 0)],
                   [Point(-1, 1, 0), Point(0, -1, 0), Point(0, 0, 1)]])
        # TODO make higher dimensional ones of these.

    def test_iterate_simplices(self):
        """Must be able to iterate all simplices of each dimension.

        (This is because the output we ultimately want is a list of
        simplices, in some special format.)

        Also, to draw a triangulation on the screen, we can simply
        draw its 1-skeleton (all its edges and vertices). This will
        be handy for that also.
        """

        # The simplices of dimension 0 should be the vertices (though I don't
        # currently care about their type (could be Point but probably
        # shouldn't be)
        self.assertEqual(len(self.one_d_sim_pts),
                         len([*self.one_d_sim.simplices(0)]))
        self.assertEqual(len(self.one_d_sim_pts) - 1,
                         len([*self.one_d_sim.simplices(1)]))

    def test_iterate_simplex_points(self):
        """Should be able to iterate over the Points in a simplex."""
        self.two_d_sim

    def test_point_location(self):
        """Tests point location.

        Given an arbitrary query point, return the face containing that point.
        """
        # Test for the 1-D case:
        # (-2, 1) should be in the face defined by (-5, 1) and (-1, 1).
        for point in self.one_d_sim.locate(Point(-2, 1)).points():
            self.assertIn(point, [Point(-5, 1), Point(-1, 1)])


        # If the query is in a lower-dimensional simplex, that simplex could be
        # returned instead of a face, for topological correctness or whatever.
        # When you do your hyperplane-side tests, make sure that it's not
        # strictly outside the simplex. But if some of the tests return 0, then
        # the query point is in the intersection of those hyperplanes.  (If one
        # returns 0, the query is in the relevant sub-simplex.)

        # Honesly I think the behavior I just described would be super annoying.
        # I'd rather always return a face.
        # Rant, rant, rant.

    def test_simplex_split(self):
        """Test splitting a d-dimensional face into d+1 new faces."""
        # I could totally be wrong about d+1, but it's correct for
        # d in [1, 2, 3]. ... I hand-wavy proof follows:

        # Add query point q to some k-simplex:
        # k-simplex has k+1 vertices therefore also k+1 [k-1]-simplices.
        # Each [k-1]-simplex has k [k-2]-simplices. Call those S[0], .. S[k-1].
        # Then for i in range(k), we define a new [k-1] simplex T[i]
        # by T[i] := S[i] \cup q
        # There, plus the original face, define a new [k-1]-simplex.
        # The resulting k [k-1]-simplices, along with the original [k-1]-simplex
        # over whose [k-2]-simplices we just iterated, define a new
        # k-simplex.
        # If you repeat this process you'll get exactly one new
        # k-simplex for each [k-1]-simplex incident to the original k-simplex.
        # So yes, the number of new faces is k+1 in general.

        # (Notice the proof wasn't rigorous because I didn't prove that
        # the new simplices would be well-formed, that their intersections
        # were either empty or lower-dimensional simplices,
        # or that their union covers the original k-simplex we were
        # splitting up. But hey, those things make sense for k < 4,
        # so I'm no worse than when I started.)

        pass  # TODO obviously

class PolytopalComplex(unittest.TestCase):
    """This is like a simplicial complex, but instead of simplices it has
    arbitrary convex polytopes as faces. (So, d-dimensional components
    need not be defined by d+1 vertices. Although they should have
    at least d+1 vertices. Also facets aren't closed unter subset.)

    All my tests for SimplicialComplex so far could ALMOST
    be copied and pasted over here. I could cry.
    """

    def setUp(self):
        """Implicitly also tests the constructor. Whatever."""
        pass  # TODO make some fancy voronoi-diagram looking things

    def test_point_location(self):
        """Be able to return the face containing a query point."""
        # Point location by walking (per homework 2 q4) should work
        # But I wouldn't trust visibility walk in particular.
        pass  # TODO

    def test_facet_iteration(self):
        """Enumerate all facets of a given dimension.

        Useful for drawing (e.g. draw the 1-skeleton).

        Very tired, see the corresponding test for SimplicialComplex.
        """
        pass  # TODO


class TriangulationTestCase(unittest.TestCase):
    """Tests for the triangulation data structure."""

    def setUp(self):
        pass

#     def test_flip(self):
#         thingy = Triangulation(
#             points=[Point(0, 0, 1), Point(1, 0, 1), Point(0, 1, 1)])
# #         TODO
