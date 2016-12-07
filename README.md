# python-voronoi
### Introduction
This project is designed to produce Voronoi diagrams and Delaunay
triangulation in n-dimensions. Included is also a GUI that allows for the
visualization of the creation of Delaunay Triangulations in 2D. This involves
a visibility walk, as well as a "face-shattering" algorithm to keep the
triangulation Delaunay. It is also possible to see the dual to the Delaunay
triangulation (the Voronoi Diagram)

### Testing
To run all the tests, run `python3 -m unittest discover -v`.
To run a particular test, run `python3 -m unittest -v pyVor.tests.testPredicates`
(optionally replacing `testPredicates` with the test you actually want to run).

### Requirements
- If running on Linux, the GUI requires tk to be installed via package manager
(for example `pacman -S tk`) since it does not ship with the Linux version
of python

### Running Arbitrary Files
`python3 -m pyVor.path.to.file`

### GUI
To run the GUI, simply run `python3 main/gui.py`
Key bindings are as follows:
- `left click` to add a point
- `c` on a triangle to show the circumcircle
- `<backspace>` to clear all circumcircles
- `s` to toggle visualization
- `v` to toggle showing the Voronoi diagram
- `p` to print the points added to standard out
