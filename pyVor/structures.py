#!/usr/bin/env python3



# class Poset(object):
#     """A collection of faces of various dimensions, all convex.

#     This is used to represent triangulations and Voronoi diagrams.
#     """

#     class Face:

#         parents = None
        

#     def __init__(self, dimension, points=None, facets=None):
#         """I honestly am not sure we need to build one of these from scratch.

#         Dimension is number of dimensions.
#         """
#         self.vertices = 

from pyVor.primitives import Point
from pyVor.predicates import ccw

class GeneralPositionError(Exception):
    """For when the input isn't in general position.

    Obviously it's better to handle the input properly. This is a stand-in.
    """
    def __init__(self, *args):
        super().__init__("Points not in general position", *args)

class SimplicialComplex:
    """A d-dimensional set of faces. Essentially a triangulation."""

    # vertices = []  # The order of these never changes
    # faces = []

## Process: Input = set of vertices, set of faces (to be closed under subset)
## Establish total order on vertices. DONE
## Make faces with tuples of vertices (hashable; in total order)
## For pairs of faces, if they should share a facet, make it. (Do this by DFS)
## (Facets will store directional information, i.e. which side each face is on.) DONE
## Iterable: both points and Vertices

    class Face:
        """A d-dimensional face. Has d+1 vertices and facets."""
        # vertices = []  # To be sorted in ascending order
        # facets = {}  # Will map lists of vertices to faces

        # def _common_vertices(self, other):
        #     """What vertices do I have in common with this other face? List."""
        #     # Not useful. See _generate_facet instead
        #     raise NotImplementedError

        def __init__(self, vertices):
            """Constructs the face, but doesn't add any facets.

            (This is because of course it is not aware of anything but its own
            vertices.)
            """
            vertices.sort()
            self.vertices = tuple(vertices)
            self.facets = {}

        def add_facet(self, facet, vertex):
            """Add a facet, vertex pair.

            The facet stores which directions are inside and outside,
            so we don't worry about that here.
            """
            self.facets[vertex] = facet


        def _generate_facet(self, other, add_to_faces=True):
            """Construct the common facet, if it exists.

            If it exists, add it to both faces (if add_to_faces=True)
            and then return it. (Else return None.)

            If a facet exists already, nothing is returned or created,
            even if the current facet "ought" to be changed. This method
            is not for changing facets. Really it should only
            be used by the SimplicialComplex constructor.
            """
            if (len(self.vertices) == len(self.facets) or
                len(other.vertices) == len(other.facets)):
                # We don't need more facets.
                return None
            # The vertices of each will be in order, so we can
            # find the relative complements in linear time.
            # (If something's confusing, consider that I optimized this
            #  reasonably well but not completely.)
            i_self = 0  # Some indices.
            i_other = 0
            v_self = None  # The vertices not in both self and other
            v_other = None
            while (i_self < len(self.vertices)
                   and i_other < len(other.vertices)):
                if self.vertices[i_self] == other.vertices[i_other]:
                    i_self += 1
                    i_other += 1
                elif (v_self is None and
                      self.vertices[i_self] < other.vertices[i_other]):
                    # self.vertices[i_self] is not in other
                    v_self = self.vertices[i_self]
                    i_self += 1
                elif (v_other is None and
                      self.vertices[i_self] > other.vertices[i_other]):
                    # other.vertices[i_other] is not in self
                    v_other = other.vertices[i_other]
                    i_other += 1
                else:
                    # The two faces do not share a facet
                    # (I.e. they don't have d-1 vertices in common)
                    return None
            if v_self in self.facets:
                # Don't change anything or return anything. A facet
                # exists already.
                return None
            if (v_self is None) or (v_other is None):
                # This should never happen but is happening
                # print("{}, {}".format(self, other))  # TODO get rid of this
                # print(len(self.vertices))
                # print(len(other.vertices))
                # print(len(other.vertices[0].point))
                return None
            facet = SimplicialComplex.Facet([self, other], [v_self, v_other])
            if add_to_faces:
                self.facets[v_self] = facet
                other.facets[v_other] = facet
            return facet

        def shared_facet(self, other_face):
            """If self is adjacent to other_face, return the shared facet.

            Else return None.
            """
            for vert in vertices:
                if vert not in other_face:
                    facet = self.facets[vert]
                    if other_face in facet.faces:
                        return facet
                    else:
                        return None
            # This should be unreachable unless the SimplicialComplex
            # is half-built somehow:
            return None

        def iter_vertices(self):
            """Iterate through vertices in order.

            Currently equivalent to accessing self.vertices.
            """
            return self.vertices

        def iter_facets(self):
            """Iterate through facets, ordered like iter_vertices."""
            return [self.facets[key] for key in self.iter_vertices()]

        def iter_points(self):
            """Iterate through points, ordered like iter_vertices."""
            return [vert.point for vert in self.iter_vertices()]

        def contains(self, point, **kwargs):
            """Is the query point inside this simplex?
            
            (You can pass **kwargs for predicates.ccw.)
            """
            for facet in self.iter_facets():
                if facet.lineside(point, **kwargs) != self:
                    return False
            return True

    class Vertex:
        """Vertices of the simplicial complex, with an order imposed.

        Incidence is not implemented at this time. I doubt it will be.

        Never reassign the point attribute, since you'll change the hash.
        """
        def __init__(self, point):
            self.point = point

        def __gt__(self, other):
            return hash(self) > hash(other)

        def __lt__(self, other):  # Used exclusively by sort builtin.
            return hash(self) < hash(other)

        def __le__(self, other):
            return hash(self) <= hash(other)

        def __ge__(self, other):
            return hash(self) >= hash(other)

        # def __eq__(self, other):  # I'd prefer pointer comparison
        #     return self.point == other.point

        def __hash__(self):
            return hash(self.point)

    class Facet:
        """A d-1 dimensional face. Has d vertices."""

        # faces = (None, None)  # public
        # _vertices = (None, None)
        # _sides = (0, 0)

        def __init__(self, faces, vertices):
            """faces is a pair of faces and vertices is a pair of vertices.
            This facet will be incident to both faces.

            The input should satisfy
            (vertices[0] in faces[0] and vertices[0] not in faces[1])
            and similar for vertices[1].

            Incorrect inputs could lead to migraines, so be careful.

            (Facets should typically be constructed by Face._generate_facet)
            """
            # Let's sort our two _vertices in case that matters somehow
            if vertices[0] > vertices[1]:
                # Reverse things
                vertices = vertices[::-1]
                faces = faces[::-1]
            self.faces = tuple(faces)
            self._vertices = tuple(vertices)
            if ccw(*[vert.point for vert in faces[0].iter_vertices()
                     if vert not in self._vertices],
                   vertices[0].point) == 1:
                # Catastrophic if either vertex is in this facet
                self._sides = (1, -1,)
            else:
                self._sides = (-1, 1,)

        def face(self, number):
            """Argument is the result of ccw(*self, point) for a point in the
            returned face.
            """
            if number not in self._sides:
                raise ValueError("Argument must be 1 or -1")
            else:
                return self.faces[self._sides.index(number)]

        def lineside(self, point, **kwargs):
            """Takes a point, not a vertex. Returns a face.

            **kwargs are passed directly to predicates.ccw.
            """
            answer = ccw(*self.iter_points(), point, **kwargs)  # -1, 0, or 1
            if answer != 0:
                return self.face(answer)
            else:
                # The point is co-planar with this face. Shucks.
                raise GeneralPositionError


    def __init__(self, points, face_sets):
        """Constructor for SimplicialComplex

        Pass a set of points and a list of "faces", which are
        simply subsets of the points (of size d+1, where d is
        the dimension of the points).
        """
        self.vertices = sorted([self.Vertex(pt) for pt in points])
        # We have to make a bunch of faces, now. They won't have facets yet.
        # Convert all the faces to vertices:
        points_to_verts = {vert.point: vert for vert in self.vertices}
        face_sets = [[*map(lambda p: points_to_verts[p], fs)] for fs in face_sets]
        self.faces = []
        for fs in face_sets:
            self.faces.append(self.Face(fs))  # Face does its own sorting
        # Now to make Facets between Faces:
        # Let's do this the naive, quadratic way.
        # (Quadratic _generate_facet calls in len(faces).)
        # If we see huge enough point sets in low dimensions,
        # there could maybe be a better way, though it would be
        # rather complicated.
        for i in range(len(self.faces)):
            for j in range(i + 1, len(self.faces)):
                self.faces[i]._generate_facet(self.faces[j],
                                              add_to_faces=True)
        
