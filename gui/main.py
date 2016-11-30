import pyVor.primitives
import pyVor.utils
import pyVor.structures
import time
from tkinter import Tk, Canvas, Frame, BOTH


class Triangulation_GUI(Frame):
    """Class used for representing a triangulation"""

    def __init__(self, parent):
        """Constructor which takes in parent (the main window)"""
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.d = None
        self.working = False

    def draw_point_locate(self, face):
        """Show the point location for a given face"""
        self.canvas.delete("locate")  # Delete the highlighted triangle
        face_points = []
        for vert in face.vertices:
            if vert.point[2] == 0:
                # Inifinity points must be reallllllllly far away
                face_points.append(vert.point[0] * 1000000000)
                face_points.append(vert.point[1] * 1000000000)
            else:
                face_points.append(vert.point[0])
                face_points.append(vert.point[1])
        # Make the polygon
        self.canvas.create_polygon(*face_points, fill="gray",
                                   outline="black", tag="locate")
        self.canvas.update()
        # Sleep so that the user can actually see what's happening
        time.sleep(.5)

    def click(self, event):
        """Event for when the user clicks on the screen"""
        # working is used so that the user cannot add points while the
        # algorithm is running. If we don't have this, we would have a weird
        # error sometimes that would cause points not to be added
        if self.working:
            return

        self.working = True
        self.canvas.delete("circle")  # the circumcircle may not be valid
        self.addPoint(pyVor.primitives.Point(event.x, event.y))
        # if the triangulation exists, add the point to the triangulation,
        # otherwise, make a new triangulation
        if self.d:
            self.d.delaunay_add(pyVor.primitives.Point(event.x, event.y),
                                homogeneous=False)
        else:
            self.d = pyVor.structures.DelaunayTriangulation(
                (pyVor.primitives.Point(event.x, event.y),),
                randomize=False,
                homogeneous=False,
                function=self.draw_point_locate)
        self.canvas.delete("locate")
        self.drawTriangulation()
        self.working = False

    def showCircle(self, event):
        """Shows a circumcircle for a tirnagle if the user wants to see it"""
        face = self.d.locate(pyVor.primitives.Point(event.x, event.y, 1))
        center = pyVor.utils.circumcenter(
            *[vert.point for vert in face.vertices])
        face_point = next(iter(face.vertices)).point
        distance = ((face_point[0] - center[0]) ** 2 +
                    (face_point[1] - center[1]) ** 2) ** .5
        self.canvas.create_oval(center[0] - distance, center[1] - distance,
                                center[0] + distance, center[1] + distance,
                                outline="black", dash=(5,), tag="circle")

    def clear(self, event):
        """Removes all circles"""
        self.canvas.delete("circle")

    def modify_function(self, event):
        """Switch visualization on and off"""
        if self.d.function is None:
            self.d.set_function(self.draw_point_locate)
        else:
            self.d.set_function(None)

    def initUI(self):
        """Initialize the window"""
        self.parent.title("Delaunay Triangulation")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<Button-3>", self.showCircle)
        self.canvas.bind("c", self.clear)
        self.canvas.bind("s", self.modify_function)
        self.canvas.focus_set()
        self.canvas.pack(fill=BOTH, expand=1)

    def addPoint(self, point):
        """Add a point to the screen"""
        self.canvas.create_oval(point[0] - 5, point[1] - 5, point[0] + 5,
                                point[1] + 5, outline="black", fill="black")

    def drawTriangulation(self):
        """Actually draw the triangulation"""
        self.canvas.delete("triangle")
        faces = self.d.face_point_sets(homogeneous=False)
        for face in faces:
            face_points = []
            for point in face:
                face_points.append(point[0])
                face_points.append(point[1])
            self.canvas.create_polygon(*face_points, fill="", outline="black",
                                       tag="triangle")


def main():
    root = Tk()
    dt = Triangulation_GUI(root)
    root.geometry("500x500")
    root.mainloop()

if __name__ == '__main__':
    main()
