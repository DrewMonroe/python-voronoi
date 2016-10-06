import numpy as np


class Point:
    """This class stores imformation about a point in R^n"""
    def __init__(self, *components):
        """Store componements in a numpy array under the hood"""
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
        """TODO: We need to implement this once we have a vector class"""
        pass

    def to_array(self):
        """Return a numpy array of the components
        This will be useful for if we need to build up additional data
        structures from a point
        """
        return self._components

    def to_vector(self):
        """Turn the point into a vector from the origin"""
        return self - Point(*[0 for x in self])
