import time
from typing import Iterable, Union, cast

from OCP.BRepOffset import BRepOffset_MakeOffset, BRepOffset_Skin # type: ignore
from OCP.GeomAbs import GeomAbs_Intersection # type: ignore

from cadquery import Workplane, Shape, Edge, Face, Shell, Solid, Wire, Compound, Vector
from cadquery.cq import T, VectorLike

from ._typing import FaceIndices, MeshGrid
from ._util import toTuples, toVectors

from .polyhedron import hull

import numpy


def makePolyhedron(points: Iterable[VectorLike], faces: Iterable[FaceIndices], debug: bool = False) -> Solid:
    vectors = numpy.array(toVectors(points))

    # Create the faces using CadQuery
    print(f'[makePolyhedron] num of faces: {len(faces)} , num of points: {len(points)}') if debug else None
    t0 = time.time()
    shell_faces = [
        Face.makeFromWires(
            Wire.assembleEdges(
                Edge.makeLine(*vts[[-1 + i, i]]) for i in range(vts.size)
            )
        )
        for vts in (vectors[list(face)] for face in faces)
    ]
    print("- shell_faces: %s sec" % (time.time() - t0)) if debug else None

    # Make Shell
    t1 = time.time()
    shell = Shell.makeShell(shell_faces)
    print("- makeShell: %s sec" % (time.time() - t1)) if debug else None

    # Make Solid
    t2 = time.time()
    s = Solid.makeSolid(shell)
    print("- makeSolid: %s sec" % (time.time() - t2)) if debug else None

    return s

def polylineJoin(points: Iterable[VectorLike], join: Union[T, Solid, Compound]) -> Union[Solid, Compound]:
    if isinstance(join, Workplane):
        joinSolidCompound = join.val()
    elif isinstance(join, Solid) or isinstance(join, Compound):
        joinSolidCompound = join
    else:
        raise ValueError(f"Join type '{type(join)}' is not allowed")
    
    join_vts = tuple(v.toTuple() for v in cast(Shape, joinSolidCompound).Vertices())
    joins = tuple(
        tuple(
            Vector(p) + Vector(vt) for vt in join_vts
        ) 
        for p in toTuples(points)
    )

    wp = Workplane()
    for i in range(len(joins) - 1):
        wp = wp.add(Workplane(makePolyhedron(*hull(joins[i] + joins[i + 1]))))

    return cast(Union[Solid, Compound], wp.combine().val())


def splineApproxSurface(points: MeshGrid, thickness: float) -> Union[Solid, Face]:   
    if isinstance(points[0][0], Vector):
        face = Face.makeSplineApprox(cast(list[list[Vector]], points))
    else:
        face = Face.makeSplineApprox([[Vector(*p) for p in col] for col in points])

    # THICKEN SURFACE
    # abs() because negative values are allowed to set direction of thickening
    if abs(thickness) > 0: 
        solid = BRepOffset_MakeOffset()
        solid.Initialize(
            face.wrapped,
            thickness,
            1.0e-5,
            BRepOffset_Skin,
            False,
            False,
            GeomAbs_Intersection,
            True,
        )  # The last True is important to make solid
        solid.MakeOffsetShape()
        return Solid(solid.Shape())
    else:
        return face