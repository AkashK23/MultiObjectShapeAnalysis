# MultiObjectShapeAnalysis
Obtaining shape statistics on adjacent object pairs

fit2D.py:

This file fits a 2D s-rep to a flat 2D object.
Input: set of discrete points on the boundary of the 2D objects
Ouput: skeletal points and boundary points of the fitted 2D s-rep

curvedSrep.py

This file maps the skeletal points of the inputted ellipsoids skeleton onto the XY plane.
Then a 2D s-rep is fit to the translated/rotated set of points
Then, the 2D s-rep is mapped back to the space of their original locations
input: skeletal points of ellipsoid s-rep
output: s-rep of the ellipsoid's s-rep

mapToSkel.py

This code takes in the meshes of the adjacent objects, finds the overlap region, and calls the other scripts to obtain the 2d s-rep of the shared boundary
Input: Two meshes of adjacent objects
Output: 2D s-rep of shared boundary

