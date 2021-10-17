from math import sin, cos, radians
from cqmore import Workplane

u_step = 10
v_step = 0.2
thickness = 0.1

# not precise, but workable
points = []
for u in range(0, 360 + u_step, u_step):
    row = []
    for vi in range(11):
        v = -1 + vi * v_step
        row.append((
            (1 + v / 2 * cos(radians(u / 2))) * cos(radians(u)), 
            (1 + v / 2 * cos(radians(u / 2))) * sin(radians(u)), 
            v / 2 * sin(radians(u / 2))
        ))
    
    points.append(row)

mobius_strip = Workplane().gridSurface(points, thickness)