#!/usr/bin/env python3

import numpy as np
from pyVor.primitives.vector import Vector


class Point:
    """This class stores imformation about a point in R^n"""
    def __init__(self, *components):
        """Store componements in a numpy array under the hood"""
        if not components:
            raise ValueError("Empty Point")
        self._components = np.array(components)

    def __repr__(self):
        """Return the string of the tuple of the components"""
        return str(tuple(x for x in self._components))

    def __str__(self):
        """Returns the string of the tuple of the components"""
        return str(tuple(x for x in self._components))

    def __len__(self):
        """Returns the number of components"""
        return len(self._components)

    def __getitem__(self, val):
        """Be able to access an individual component of a point"""
        return self._components[val]

    def __iter__(self):
        """So that we can iterate over the components of a point"""
        for i in self._components:
            yield i

    def __eq__(self, p):
        """Equality if points have the same components in the same order"""
        return type(self) == type(p) and\
            len(p) == len(self) and\
            all([p[i] == self[i] for i in range(len(p))])

    def __sub__(self, p):
        """We need to implement this once we have a vector class"""
        if len(self) != len(p):
            raise ValueError('Dimension mismatch')
        return Vector(*[x - y for x, y in zip(self, p)])

    def to_vector(self):
        """Turn the point into a vector from the origin"""
        return self - Point(*[0 for x in self])

    def lift(self, function=lambda *args: 1):
        """Lifts a point up to a dimension based on the given function"""
        return Point(*np.append(self._components, Point(function(self)),
                     axis=0))
