# python-voronoi
### Introduction
This project is designed to produce Voronoi diagrams and Delaunay
triangulation in n-dimensions. Included is also a GUI that allows for the
visualization of the creation of Delaunay Triangulations in 2D. This involves
a visibility walk, as well as a "face-shattering" algorithm to keep the
triangulation Delaunay.

### Testing
To run all the tests, run `python3 -m unittest discover -v`.
To run a particular test, run `python3 -m unittest -v pyVor.tests.testPredicates`
(optionally replacing `testPredicates` with the test you actually want to run).

### Requirements
- tk (needs to be installed via package manager. For example `pacman -S tk`)

### Running Arbitrary Files
`python3 -m pyVor.path.to.file`

### GUI
To run the GUI, simply run `python3 main/gui.py`
Key bindings are as follows:
- `left click` adds a point
- `c` on a triangle shows the circumcircle
- `<backspace>` clear all circumcircles
- `s` toggle visualization
