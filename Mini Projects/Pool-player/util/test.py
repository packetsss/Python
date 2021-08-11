from shapely.geometry import LineString, Point

p = Point(5, 5)
c = p.buffer(2).boundary
l = LineString([(0, 0), (3, 3)])
i = c.intersection(l)
print(bool(i))