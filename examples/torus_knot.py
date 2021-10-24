from cqmore import Workplane
from cqmore.curve import torusKnot, parametricEquation

from cadquery import Plane, Vector

origin = torusKnot(0, p = 2, q = 3)
v1 = Vector(*torusKnot(0.9, p = 2, q = 3))
v2 = Vector(*torusKnot(0.1, p = 2, q = 3))

r = (Workplane(Plane(origin = origin, normal=(v2 - v1)))
        .polygon(5, 1)
        .sweep(
            Workplane().parametricCurve(
                parametricEquation(torusKnot, p = 2, q = 3)
            ), 
            auxSpine = Workplane('XZ').rect(1, 1)
        )
    )