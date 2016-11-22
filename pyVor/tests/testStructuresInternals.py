#!/usr/bin/env python3

"""Tests for the data structures that are not independent of implementation.

This is only useful because I keep writing bugs into the implementation of the
data structures. These bugs are easier to test if you access "non-public" parts
of the data structure API.
"""

import unittest
from pyVor.primitives import Point
from pyVor.structures import SimplicialComplex as SC
#from pyVor.strucures.SimplicialComplex import Vertex, Facet, Face

class SimplicialComplexInternalsTestCase(unittest.TestCase):
    """See module docstring"""

    def test_face_generate_facet(self):
        """Test face._generate_facet(...)"""

        # Test in one dimension (+ homogeneous coordinates as always)
        vertices = [SC.Vertex(Point(*tup)) for tup in [
            (-5, 1), (-3, 1), (-1, 1), (1, 1)]]
        assert vertices == sorted(vertices)  # Else the test is useless
        left_face = SC.Face(vertices[0:2])
        right_face = SC.Face(vertices[1:3])

        result = left_face._generate_facet(right_face, add_to_faces=True)
        self.assertIsInstance(result, SC.Facet)

        # Make sure we associated the facet with the proper vertices
        # (and added it to the faces at all)
        self.assertIn(vertices[0], left_face.facets)
        self.assertIn(vertices[2], right_face.facets)
        # Make sure it's the same facet for both
        self.assertIs(left_face.facets[vertices[0]],
                      right_face.facets[vertices[2]])
        # Make sure we only added it in one place
        self.assertEqual(len(left_face.facets), 1)
        self.assertEqual(len(right_face.facets), 1)

    def test_vertex_equality(self):
        vertex = SC.Vertex(Point(3, 1))
        other = vertex
        self.assertEqual(vertex, other)
        self.assertFalse(vertex < other)

if __name__ == '__main__':
    unittest.main()
