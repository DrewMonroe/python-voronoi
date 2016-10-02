import numpy as np


class point:
    """This class stores imformation about a point in R^n"""
    def __init__(self, *components):
        """Store componements in a numpy array under the hood"""
        self._components = np.array(components)

    def __repr__(self):
        """The string "point(x)" where x is the components of the point"""
        return "point(" + ", ".join(str(x) for x in self._components) + ")"

    def __str__(self):
        """Returns the string of the tuple of the components"""
        return str(tuple(x for x in self._components))

    def __len__(self):
        """Returns the number of components"""
        return len(self._components)

    def __getitem__(self, val):
        """This allows for slicing of a point, which may or may not actually
        be a useful thing. We should probably talk about how this should be
        implemented, maybe we want to return a point? Maybe we want to return
        a numpy array?
        """
        # if the user has specified a slice, then return a tuple of the slicing
        if type(val) == slice:
            return tuple(x for x in self._components[val])
        # otherwise, return the value at the given index
        return self._components[val]

    def __iter__(self):
        """So that we can iterate over the components of a point"""
        for i in self._components:
            yield i

    def __eq__(self, p):
        """Equality if points have the same components in the same order"""
        return len(p) == len(self) and\
               all([p[i] == self[i] for i in range(len(p))])

    def __sub__(self, p):
        """TODO: We need to implement this once we have a vector class"""
        pass
