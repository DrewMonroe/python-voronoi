#!/usr/bin/env python3

"""This should be the main command line interface to our project."""

import argparse
import sys
import re

from pyVor.structures import DelaunayTriangulation as DelT
from pyVor.primitives import Point


def line_to_point(line):
    """Convert a line of user input to a point.

    Homogeneous coordinates are not added, on the grounds that this part of
    the code really oughtn't to do any math.
    """
    line = line.strip("() \t\n")
    return Point(*(float(x) for x in line.split()))


def main():
    """See argument parser or output of --help"""
    parser = argparse.ArgumentParser(
        description="Triangulate a set of points in any number of dimensions."
        " The result is a Delaunay triangulation with respect to the usual "
        "Euclidian getup. If you want something weirder you'll have "
        "to change the code.")
    parser.add_argument("-g", "--homogeneous", action='store_true',
                        help="Set this flag if the input has homogeneous "
                        "coordinates already.")
    args = parser.parse_args()
    # I'm happy with no arguments for now. Let's just do sys.stdin.
    not_empty = re.compile(r'.*\d+.*')
    points = []
    for line in sys.stdin:
        if not_empty.match(line):
            points.append(line_to_point(line))
    del_tri = DelT(points, homogeneous=args.homogeneous)
    if not del_tri.test_is_delaunay():
        print("It might not have worked. Oh, well!")
    print("Done!")  # I'm so mean. TODO output something reasonable here.
    exit(1337)

if __name__ == '__main__':
    main()
