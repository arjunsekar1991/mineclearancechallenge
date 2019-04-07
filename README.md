# mineclearancechallenge

The approach is to scan the entire area using some pattern like interlaced scanning.

Once we come across 3 closely located points in x direction there is a chance for that point to be a circle
hence we just triangulate 3 closest point
from there we are calculating the approimate centre
and the radius for the circle.

Is the pattern we are searching for is a line then it can located by finding 2 closer y values.

From there can calculate slope betweeb the two points and then try to locate the rest of the points
