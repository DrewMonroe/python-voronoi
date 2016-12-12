#!/usr/bin/env python3

"""A gui for Delaunay triangulations and Voronoi diagrams in the plane"""

import time
from tkinter import Tk, Canvas, Frame, BOTH

import pyVor.primitives
import pyVor.utils
import pyVor.structures


class TriangulationGUI(Frame):
    """Class used for representing a triangulation"""

    def __init__(self, parent):
        """Constructor which takes in parent (the main window)"""
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.points = []
        self.delt = None
        self.working = False
        self.edge_dic = {}
        self.visualization = False
        self.voronoi_on = False
        self.voronoi = None

    def draw_point_locate(self, face):
        """Show the point location for a given face"""
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
        self.canvas.update_idletasks()
        # Sleep so that the user can actually see what's happening
        time.sleep(.5)
        self.canvas.delete("locate")  # Delete the highlighted triangle

    def click(self, event):
        """Event for when the user clicks on the screen"""
        # working is used so that the user cannot add points while the
        # algorithm is running. If we don't have this, we would have a weird
        # error sometimes that would cause points not to be added
        if self.working:
            return

        self.working = True
        self.canvas.delete("circle")  # the circumcircle may not be valid
        point = pyVor.primitives.Point(event.x, event.y)
        self.points.append(point)
        self.add_point(point)
        self.clear_vononoi()  # the voronoi diagram may not be valid anymore
        self.add_point(pyVor.primitives.Point(event.x, event.y))
        # if the triangulation exists, add the point to the triangulation,
        # otherwise, make a new triangulation
        if self.delt:
            self.delt.delaunay_add(pyVor.primitives.Point(event.x, event.y),
                                   homogeneous=False)
        else:
            self.delt = pyVor.structures.DelaunayTriangulation(
                (pyVor.primitives.Point(event.x, event.y),),
                randomize=False,
                homogeneous=False,
                # draw_circle=self.draw_circle,
                # location_visualizer=self.draw_point_locate,
                # draw_triangulation=self.draw_triangulation,
                # highlight_edge=self.highlight_edge,
                # delete_edge=self.delete_edge,
                gui=self)
        self.canvas.delete("locate")
        self.draw_triangulation(self.delt)
        if self.voronoi_on:
            self.draw_voronoi()
        self.working = False

    def show_circle(self, event):
        """Shows a circumcircle for a triangle if the user wants to see it"""
        face = self.delt.locate(pyVor.primitives.Point(event.x, event.y, 1))
        self.draw_circle(face)

    def draw_circle(self, face, color="black", delete=False, sleep=False):
        if delete:
            self.canvas.delete("circle")
        for vert in face.vertices:
            if vert.point[2] == 0:
                return
        center = pyVor.utils.circumcenter(
            *[vert.point for vert in face.vertices])
        face_point = next(iter(face.vertices)).point
        distance = float((face_point - center).norm_squared()) ** .5
        self.canvas.create_oval(center[0] - distance, center[1] - distance,
                                center[0] + distance, center[1] + distance,
                                outline=color, dash=(5,), tag="circle")
        self.canvas.update_idletasks()
        if sleep:
            time.sleep(1)

    def highlight_edge(self, facet, color="black", tag="edge", add=True):
        points = []
        for point in facet.points():
            points.append(point[0])
            points.append(point[1])
        line = self.canvas.create_line(*points, fill=color, tag=tag)
        if add:
            self.edge_dic[facet] = line
        self.canvas.update()

    def clear(self, event):
        """Removes all circles"""
        self.canvas.delete("circle")

    def toggle_visualization(self, event):
        """Switch visualization on and off"""
        # if self.visualization:
        #     self.set_visualize(False)
        # else:
        #     self.set_visualize(True)
        self.visualization = not self.visualization

    def toggle_voronoi(self, event):
        """Switches the voronoi diagram on or off"""
        self.voronoi_on = False if self.voronoi_on else True
        if self.voronoi_on:
            self.draw_voronoi()
            self.canvas.update()
        else:
            self.clear_vononoi()

    def clear_vononoi(self):
        """Delete the voronoi diagram from the screen"""
        self.canvas.delete("voronoipoint")
        self.canvas.delete("voronoiedge")

    def draw_voronoi(self):
        """Draws the voronoi diagram"""
        self.voronoi = pyVor.structures.Voronoi(self.delt)
        for point in self.voronoi.points:
            self.add_point(point, color="red", tag="voronoipoint")

        for edge in self.voronoi.edges:
            point1, point2 = edge
            point1 = point1[:-1].to_vector() * 1000000 if point1[-1] == 0\
                else point1[:-1].to_vector()
            point2 = point2[:-1].to_vector() * 1000000 if point2[-1] == 0\
                else point2[:-1].to_vector()
            self.canvas.create_line(*point1, *point2,
                                    fill="red", tag="voronoipoint")

    def initUI(self):
        """Initialize the window"""
        self.parent.title("Delaunay Triangulation")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("c", self.show_circle)
        self.canvas.bind("<Button-2>", self.show_circle)
        self.canvas.bind("<Button-3>", self.show_circle)
        self.canvas.bind("<BackSpace>", self.clear)
        self.canvas.bind("<v>", self.toggle_voronoi)
        self.canvas.bind("s", self.toggle_visualization)
        self.canvas.bind("p", self.print_point_history)
        self.canvas.focus_set()
        self.canvas.pack(fill=BOTH, expand=1)

    def delete_edge(self, facet):
        self.canvas.delete(self.edge_dic[facet])
        self.canvas.update_idletasks()

    def add_point(self, point, color="black", tag=""):
        """Add a point to the screen"""
        self.canvas.create_oval(point[0] - 5, point[1] - 5, point[0] + 5,
                                point[1] + 5,
                                outline=color,
                                fill=color,
                                tag=tag)

    def draw_triangulation(self, triangulation, clear=False, sleep=False):
        """Actually draw the triangulation"""
        self.canvas.delete("triangle")
        self.canvas.delete("circle")
        self.canvas.delete("highlight_edge")
        if clear:
            self.canvas.delete("all")
            for point in self.points:
                self.add_point(point)
        faces = triangulation.face_point_sets(homogeneous=False)
        for face in faces:
            face_points = []
            for point in face:
                face_points.append(point[0])
                face_points.append(point[1])
            self.canvas.create_polygon(*face_points, fill="", outline="black",
                                       tag="triangle")
        # facets = triangulation.get_facets()
        # for facet in facets:
        # if not self.is_infinite(facet):
        #        self.highlight_edge(facet, tag="triangle")
        self.canvas.update_idletasks()
        if sleep:
            time.sleep(0.5)

    def is_infinite(self, facet):
        points = facet.points()
        if points[0][2] == 0 or points[1][2] == 0:
            return True
        return False

    def print_point_history(self, event):
        """Print to stdout the list of points added so far, in order"""
        print(self.delt.point_history.__repr__())


def main():
    root = Tk()
    TriangulationGUI(root)
    root.geometry("500x500")
    root.mainloop()

if __name__ == '__main__':
    main()
