import pyVor.primitives
import pyVor.utils

import graphics as g
import math


def main():
    """This is a basic test to draw three points on a screen and then calculate
    the circumcircle of these points
    """
    win = g.GraphWin()  # Make a new graphics window
    points = []  # This will store the pyVor.Points that have been clicked

    # Get three points from the mouse click and draw them
    for i in range(0, 3):
        click = win.getMouse()  # get one click
        # create a black circle (which is more visible than a single pixel)
        # around the point that the user clicked on
        p = g.Circle(click, 2)
        p.setFill("black")
        p.draw(win)  # draw that click
        # Add the pyVor.point to a list
        points.append(pyVor.primitives.Point(click.x, click.y))

    # Computer the circumcenter of the points
    center = pyVor.utils.circumcenter(*points, homogeneous=False)
    # Create a graphics.Point that represents the center
    gCenter = g.Point(center[0], center[1])
    # Create a circle around gCenter which has a radius that is the distance
    # to any one of the points
    circle = g.Circle(gCenter, math.sqrt((center[0] - points[0][0]) ** 2 +
                                         (center[1] - points[0][1]) ** 2))
    # Draw the circle
    circle.draw(win)

    # Exit on the next mouse click
    win.getMouse()

if __name__ == "__main__":
    main()
