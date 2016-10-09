#!/usr/bin/env python3

import numpy as np

class Vector:
    """This class stores imformation about a Vector in R^n"""
    def __init__(self, *components):
        """Store componements in a numpy array under the hood"""
        self._components = np.array(components)

    def __repr__(self):
        """Return the string of the list of the components"""
        return str(list(x for x in self._components))

    def __str__(self):
        """Returns the string of the list of the components"""
        return str(list(x for x in self._components))

    def __len__(self):
        """Returns the number of components"""
        return len(self._components)

    def __getitem__(self, val):
        """Be able to access an individual component of a vector"""
        return self._components[val]

    def __iter__(self):
        """So that we can iterate over the components of a vector"""
        for i in self._components:
            yield i

    def __eq__(self, v):
        """Equality if vectors have the same components in the same order"""
        return type(self) == type(v) and\
            len(v) == len(self) and\
            all([v[i] == self[i] for i in range(len(v))])

    def __sub__(self, v):
        """Pointwise vector subtraction"""
        if type(self) == type(v) and len(self) == len(v):
            return Vector(*np.subtract(self._components, v))
        else:
            return NotImplemented

    def __add__(self, v):
        """Pointwise vector addition"""
        if type(self) == type(v) and len(self) == len(v):
            return Vector(*np.add(self._components, v))
        else:
            return NotImplemented

    def __mul__(self, s):
        """Scalar multiplication"""
        if isinstance(s, (int, float)):
            return Vector(*np.multiply(self._components, s))
        elif type(self) == type(s) and len(self) == len(s):
            return self.dot(s)
        else:
            return NotImplemented

    __rmul__ = __mul__

    def to_array(self):
        """Return a numpy array of the components
        This will be useful for if we need to build up additional data
        structures from a vector
        """
        return self._components

    def dot(self, v):
        """"Returns the dot product with another vector"""
        return np.dot(self._components, v)

    def norm_squared(self):
        """Returns the norm of itself squared"""
        return self.dot(self)

    def lift(self, function=(lambda *args: 1)):
        """Lifts the vector up to a dimension based off the given function"""
        return Vector(*np.append(self._components, Vector(function()), axis=0))
