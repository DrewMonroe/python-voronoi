import pyVor.primitives
import pyVor.utils
import pyVor.structures

import graphics as g
import math


def main():
    """This is a basic test to draw three points on a screen and then calculate
    the circumcircle of these points
    """
    win = g.GraphWin("Triangulation", 400, 400)  # Make a new graphics window
    d = None

    while True:
        click = win.getMouse()  # get one click
        if d is None:
            d = pyVor.structures.DelaunayTriangulation((pyVor.primitives.Point(click.x, click.y), ), randomize=False, homogeneous=False)
        else:
            d.delaunay_add(pyVor.primitives.Point(click.x, click.y), homogeneous=False)
        # create a black circle (which is more visible than a single pixel)
        # around the point that the user clicked on
        p = g.Circle(click, 2)
        p.setFill("black")
        p.draw(win)  # draw that click

    # Exit on the next mouse click
    win.getMouse()

if __name__ == "__main__":
    main()
