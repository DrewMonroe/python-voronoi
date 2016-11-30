import pyVor.primitives
import pyVor.utils
import pyVor.structures

from tkinter import Tk, Canvas, Frame, BOTH


class Triangulation_GUI(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.d = None

    def click(self, event):
        if self.d:
            self.d.delaunay_add(pyVor.primitives.Point(event.x, event.y),
                                homogeneous=False)
        else:
            self.d = pyVor.structures.DelaunayTriangulation(
                (pyVor.primitives.Point(event.x, event.y),),
                randomize=False,
                homogeneous=False)
        self.addPoint(pyVor.primitives.Point(event.x, event.y))
        self.drawTriangulation()
        print("clicked at", event.x, event.y)

    def initUI(self):
        self.parent.title("Delaunay Triangulation")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.pack(fill=BOTH, expand=1)

    def addPoint(self, point):
        self.canvas.create_oval(point[0] - 5, point[1] - 5, point[0] + 5,
                                point[1] + 5, outline="black", fill="black")

    def drawTriangulation(self):
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
