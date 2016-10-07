import numpy as np
from vector import Vector


class Matrix:
    """This class represents a column matrix"""
    def __init__(self, *vectors):
        """Store vectors of matrix in numpy array"""
        self._columns = np.array([row.to_array() for row in vectors]).T

    def __repr__(self):
        """Return numpy array's str."""
        return str(self._columns)

    def __str__(self):
        """Return numpy array's str."""
        return str(self._columns)

    def width(self):
        """Returns the width of the matrix"""
        return len(self._columns[0])

    def height(self):
        """Returns the height of the matrix"""
        return len(self._columns[:, 0])

    def __getitem__(self, val):
        """Access individual vector of matrix"""
        return Vector(*self._columns[:, val])

    def __iter__(self):
        """Iterate over the vectors of the matrix"""
        for i in self._columns.T:
            yield Vector(*i)

    def to_array(self):
        """Return numpy array of matrix"""
        return self._columns

    def __mul__(self, other):
        """Multiply this matrix with another matrix"""
        if isinstance(other, (int, float)):
            return Matrix(*[Vector(*i) for i in
                            np.multiply(self._columns, other)])
        elif type(self) == type(other):
            return Matrix(*[Vector(*i) for i in
                            self._columns.dot(other.to_array()).T])

    __rmul__ = __mul__

    def det(self):
        """Return determinant of matrix"""
        return np.linalg.det(self._columns)

    def __add__(self, other):
        """Add this matrix with another matrix"""
        return Matrix(*[Vector(*i) for i in
                        (self._columns + other.to_array()).T])

    def __sub__(self, other):
        """Subtract this matrix with another matrix"""
        return Matrix(*[Vector(*i) for i in
                        (self._columns - other.to_array()).T])

    def __eq__(self, other):
        """Checks if two matrices are equal"""
        return np.array_equal(self._columns, other.to_array())

    def transpose(self):
        """Returns the transpose of the matrix"""
        return Matrix(*[Vector(*i) for i in self._columns])

    def power(self, p):
        """Returns a matrix to the power p"""
        return Matrix(*[Vector(*i) for i in
                        np.linalg.matrix_power(self._columns, p).T])
