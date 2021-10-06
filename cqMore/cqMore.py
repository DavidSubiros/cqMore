from .wire import (
    makePolygon,
    bool2D
)

from .solid import (
    polyhedron,
    surface
)

from typing import (
    Iterable,
    Union
)

from .cq_typing import (
    T,
    VectorLike,
    FaceIndices,
    MeshGrid
)

from cadquery import (
    Wire
)

import cadquery

class Workplane(cadquery.Workplane):
    """
    Define plugins. You may simply use `cqMore.Workplane` to replace `cadquery.Workplane`. For example:

        from cqMore import Workplane

        result = (Workplane()
                    .rect(10, 10)
                    .makePolygon(((-2, -2), (2, -2), (2, 2), (-2, 2))).extrude(1)
                 )

    You may also attach methods of `cqMore.Workplane` to `cadquery.Workplane`, such as:

        from cadquery import Workplane
        import cqMore

        Workplane.makePolygon = cqMore.Workplane.makePolygon

        result = (Workplane()
                    .rect(10, 10)
                    .makePolygon(((-2, -2), (2, -2), (2, 2), (-2, 2))).extrude(1)
                 )

    """

    def makePolygon(self: T, points: Iterable[VectorLike], forConstruction: bool = False) -> T:
        """
        Make a multiple sided wire from `points`. 
        
        ## Parameters

        - `points`: the list of x,y points of the polygon.
        - `forConstruction`: should the new wires be reference geometry only?
        
        ## Examples
        
            from cqMore import Workplane

            triangle = Workplane().makePolygon(((-2, -2), (2, -2), (0, 2))) 

        """

        p = makePolygon(points, forConstruction)
        return self.eachpoint(lambda loc: p.moved(loc), True)

    def intersect2D(self: T, toIntersect: Union[T, Wire]) -> T:
        """
        Intersect the provided wire from the current wire. 

        ## Parameters

        - `toIntersect`: a wire object, or a CQ object having a wire – object to intersect.

        ## Examples

            from cqMore import Workplane

            r1 = Workplane('YZ').rect(10, 10)
            r2 = Workplane('YZ').center(5, 5).rect(10, 10)
            intersected = r1.intersect2D(r2)

        """

        return bool2D(self, toIntersect, 'intersect')
        
    def union2D(self: T, toUnion: Union[T, Wire]) -> T:
        """
        Union the provided wire from the current wire. 

        ## Parameters

        - `toUnion`: a wire object, or a CQ object having a wire – object to union.       

        ## Examples 

            from cqMore import Workplane

            r1 = Workplane('YZ').rect(10, 10)
            r2 = Workplane('YZ').center(5, 5).rect(10, 10)
            unioned = r1.union2D(r2)

        """

        return bool2D(self, toUnion, 'union')

    def cut2D(self: T, toCut: Union[T, Wire]) -> T:
        """
        Cut the provided wire from the current wire. 

        ## Parameters

        - `toCut`: a wire object, or a CQ object having a wire – object to cut.       

        ## Examples 

            from cqMore import Workplane

            r1 = Workplane('YZ').rect(10, 10)
            r2 = Workplane('YZ').center(5, 5).rect(10, 10)
            cutted = r1.cut2D(r2)

        """

        return bool2D(self, toCut, 'cut')

    def polyhedron(self: T, points: Iterable[VectorLike], faces: Iterable[FaceIndices], combine: bool = True, clean: bool = True) -> T:
        poly = polyhedron(points, faces)
        poly_all = self.eachpoint(lambda loc: poly.moved(loc), True)
        
        if not combine:
            return poly_all
        else:
            return self.union(poly_all, clean=clean)

    def surface(self: T, points: MeshGrid, thickness: float, combine: bool = True, clean: bool = True) -> T:
        sf = surface(points, thickness)
        sf_all = self.eachpoint(lambda loc: sf.moved(loc), True)
        
        if not combine:
            return sf_all
        else:
            return self.union(sf_all, clean=clean)

if __name__ == '__main__':
    import doctest
    doctest.testmod() 