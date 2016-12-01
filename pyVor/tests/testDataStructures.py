#!/usr/bin/env python3
"""
Unit tests for triangulation class
"""

import unittest
import csv
import os
from pyVor.primitives import Point
from pyVor.structures import DelaunayTriangulation as DelT
from pyVor.structures import Voronoi


class DelaunayTriangulationTestCase(unittest.TestCase):
    """Tests for the triangulation data structure."""

    def test_vertex_compare(self):
        """Make sure vertices have an order that's reasonable."""
        verts = []
        for i in range(-5, 5):
            for j in range(-5, 5):
                verts.append(DelT.Vertex(Point(i, j, 1)))
        self.assertEqual(sorted(verts), sorted(verts[::-1]))  # consistency
        self.assertEqual(sorted(verts), sorted(verts))
        self.assertLess(sorted(verts)[0], sorted(verts)[1])
        self.assertNotEqual(verts[0], verts[1])
        self.assertEqual(verts[0], verts[0])

    def test_locally_delaunay(self):
        """Make sure that the locally delaunay test works."""

        def quick_delaunay_test(*points, expectation=True):
            """Tests that the faces defined by points[:-1] and points[1:] share
            an edge that is locally delaunay iff we expect it to be so.
            """
            vertices = [DelT.Vertex(point) for point in points]
            face_1 = DelT.Face(vertices[:-1])
            face_2 = DelT.Face(vertices[1:])
            facet_1 = face_1.half_facets[vertices[0]]
            facet_2 = face_2.half_facets[vertices[-1]]
            facet_1.twin = facet_2
            facet_2.twin = facet_1

            self.assertEqual(facet_1.lineside(facet_1.opposite.point),
                             1)
            self.assertEqual(facet_1.lineside(facet_1.opposite.point),
                             1)

            self.assertEqual(facet_1.locally_delaunay(),
                             expectation)
            self.assertEqual(facet_1.locally_delaunay(),
                             facet_2.locally_delaunay())

        # Test for one dimension first.
        quick_delaunay_test(Point(-1, 1), Point(2, 1), Point(3, 1),
                            expectation=True)
        # points_1 = [Point(-1, 1), Point(2, 1), Point(3, 1)]
        # vertices_1 = [DelT.Vertex(point) for point in points_1]
        # half_facet_1 = DelT.HalfFacet(vertices_1[0], vertices_1[1:2],
        #                              None)
        # Basic cases in 2 dimensions
        quick_delaunay_test(Point(0, 2, 1), Point(-1, 0, 1), Point(1, 0, 1),
                            Point(0, -1, 1), expectation=True)
        quick_delaunay_test(Point(0, 2, 1), Point(-1, 0, 1), Point(1, 0, 1),
                            Point(0, -0.3, 1), expectation=False)
        # Similar basic 3D cases
        unit_circle_pts_3d = [Point(0, 0, -1, 1), Point(0, 1, 0, 1),
                              Point(0, -1, 0, 1), Point(1, 0, 0, 1)]
        quick_delaunay_test(*unit_circle_pts_3d, Point(0, 0, 1.5, 1),
                            expectation=True)
        quick_delaunay_test(*unit_circle_pts_3d, Point(0, 0, 0.5, 1),
                            expectation=False)

        # Cases with infinite points in the plane:
        quick_delaunay_test(Point(0, 1, 0), Point(0.5, -400, 1),
                            Point(0, 0, 1), Point(-1, -1, 0),
                            expectation=True)

        quick_delaunay_test(Point(-2, 0, 1), Point(-0.6, 3.2, 1),
                            Point(3.2, 2.1, 1), Point(1, 0, 0),
                            expectation=True)

    def test_easy_peasy_case(self):
        """Test with one point and see if the structure makes sense."""
        point = Point(-3, 2, 1)
        deltri = DelT([point])
        self.assertEqual(len(deltri.faces), 3)
        for face in deltri.faces:
            self.assertIn(point, face.points())
            for hafacet in face.half_facets.values():
                self.assertNotIn(hafacet.opposite,
                                 hafacet.points())
        null_twin_count = 0
        for face in deltri.faces:
            self.assertEqual(len(face.vertices), 3)
            for halffacet in face.half_facets.values():
                if halffacet.twin is None:
                    null_twin_count += 1
                else:
                    self.assertIs(halffacet.twin.twin,
                                  halffacet)
        self.assertEqual(null_twin_count, 3)
        self.assertTrue(deltri.test_is_delaunay())

    def test_in_general_position(self):
        """Test rigorously, but only for nice inputs"""

        points = [Point(0.5, -400, 1), Point(10, 21, 1),
                  Point(-5, 0, 1), Point(1, 2, 1), Point(2, 1, 1)]
        deltri = DelT(points, randomize=False)
        self.assertTrue(deltri.test_is_delaunay())

    def test_2d_case(self):
        """Test the output for a 2D case transfered from a notebook"""

        # First just make sure face equality works like I hope:
        self.assertEqual(set(frozenset([Point(0, 3.7)])),
                         set(frozenset([Point(0, 3.7)])))

        del_tri = DelT([Point(-0.6, 3.2), Point(3.2, 2.1),
                        Point(-2, 0), Point(1, -0.2), Point(3.6, -0.3),
                        Point(-1.4, -2.1), Point(2.5, -1.7)],
                       homogeneous=False,
                       randomize=False)
        self.assertTrue(del_tri.test_is_delaunay())
        face_sets = set([
            frozenset(face) for face in
            del_tri.face_point_sets(homogeneous=False)])
        expected_face_sets = set([
            frozenset([Point(-2, 0), Point(-0.6, 3.2), Point(1, -0.2)]),
            frozenset([Point(3.2, 2.1), Point(-0.6, 3.2), Point(1, -0.2)]),
            frozenset([Point(3.2, 2.1), Point(3.6, -0.3), Point(1, -0.2)]),
            frozenset([Point(2.5, -1.7), Point(3.6, -0.3), Point(1, -0.2)]),
            frozenset([Point(2.5, -1.7), Point(-1.4, -2.1), Point(1, -0.2)]),
            frozenset([Point(-1.4, -2.1), Point(-2, 0), Point(1, -0.2)])])
        # Note that equality of faces works exactly like you'd want.  The test
        # even nicely tells you the differences between the sets, if it fails.
        for face_set in face_sets:
            self.assertEqual(len(face_set), 3)  # triangles have 3 vertices
        self.assertEqual(face_sets, expected_face_sets)

    def test_3d_case(self):
        fn = os.path.join(os.path.dirname(__file__), 'data/points.csv')
        f = open(fn)
        points = csv.reader(f)
        points = list(points)
        points = [[float(y) for y in x] for x in points]
        point_array = [Point(*point) for point in points]
        del_tri = DelT(point_array,
                       homogeneous=False,
                       randomize=False)
        self.assertTrue(del_tri.test_is_delaunay())
        face_sets = set([
            frozenset(face)
            for face in del_tri.face_point_sets(homogeneous=False)])
        fn = os.path.join(os.path.dirname(__file__), 'data/dt.csv')
        with open(fn, 'r') as f:
            triangles = list(csv.reader(f))
            triangles = [[int(y) for y in x] for x in triangles]
            expected_face_sets = set(
                [frozenset([point_array[y - 1] for y in x])
                    for x in triangles])
            for face_set in face_sets:
                self.assertEqual(len(face_set), 4)
        self.assertEqual(face_sets, expected_face_sets)

        #     def test_flip(self):
#         thingy = Triangulation(
#             points=[Point(0, 0, 1), Point(1, 0, 1), Point(0, 1, 1)])
# #         We do not flip! Nevermind!


class VoronoiTestCase(unittest.TestCase):
    """Tests for the voronoi data structure."""
    def test_2d_case(self):
        """Test the output for a super simple 2D case"""

        del_tri = DelT([Point(3, 4), Point(-3, 4),
                        Point(0, -5)],
                       homogeneous=False,
                       randomize=False)
        vor = Voronoi(del_tri)
        expected_center = Point(0.0, 0.0, 1.0)

        self.assertTrue(expected_center in vor.points)
        self.assertTrue(len(vor.points) == 1)
        self.assertTrue(len(vor.edges) == 3)

if __name__ == '__main__':
    unittest.main()
