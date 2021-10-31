from typing import Iterable, Union, cast
from cadquery import Vector
import numpy

from math import cos, sin, radians

from ._typing import Point3D


class Matrix3D:
    def __init__(self, m: Iterable[Iterable[float]] = None):
        if m is None:
            self.wrapped = _create()
        elif isinstance(m, numpy.ndarray):
            self.wrapped = m
        else:
            self.wrapped = numpy.array(m)

    
    def __mul__(self, that: 'Matrix3D') -> 'Matrix3D':
        return Matrix3D(self.wrapped @ that.wrapped)


    def translate(self, v: Union[Point3D, Vector]) -> 'Matrix3D':
        return Matrix3D(_translate(self.wrapped, v))


    def rotateX(self, angle: float) -> 'Matrix3D':
        return Matrix3D(_rotateX(self.wrapped, angle))

        
    def rotateY(self, angle: float) -> 'Matrix3D':
        return Matrix3D(_rotateY(self.wrapped, angle))


    def rotateZ(self, angle: float) -> 'Matrix3D':
        return Matrix3D(_rotateZ(self.wrapped, angle))


    def rotate(self, direction: Union[Point3D, Vector], angle: float) -> 'Matrix3D':
        return Matrix3D(_rotate(self.wrapped, direction, angle))


    def transform(self, v: Union[Point3D, Vector]) -> Point3D:
        return _transform(self.wrapped, v)


_identity = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

def _create() -> numpy.ndarray:
    return numpy.array(_identity)

# Post-Multiplication (Right-Multiplication)

def _translate(m: numpy.ndarray, v: Union[Point3D, Vector]) -> numpy.ndarray:
    vt = (v.x, v.y, v.z) if isinstance(v, Vector) else v
    return m @ numpy.array([
        [1, 0, 0, vt[0]],
        [0, 1, 0, vt[1]],
        [0, 0, 1, vt[2]],
        [0, 0, 0, 1]
    ]) 


def _rotateX(m: numpy.ndarray, angle: float) -> numpy.ndarray:
    rad = radians(angle)
    c = cos(rad)
    s = sin(rad)
    return m @ numpy.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ]) 


def _rotateY(m: numpy.ndarray, angle: float) -> numpy.ndarray:
    rad = radians(angle)
    c = cos(rad)
    s = sin(rad)
    return m @ numpy.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ]) 


def _rotateZ(m: numpy.ndarray, angle: float) -> numpy.ndarray:
    rad = radians(angle)
    c = cos(rad)
    s = sin(rad)
    return m @ numpy.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]) 


def _transform(m: numpy.ndarray, v: Union[Point3D, Vector]) -> Point3D:
    vt = (v.x, v.y, v.z, 1) if isinstance(v, Vector) else v + (1,)
    return cast(Point3D, tuple((m @ vt)[:-1]))


# Quaternions and spatial rotation
def _rotate(m: numpy.ndarray, direction: Union[Point3D, Vector], angle: float) -> numpy.ndarray:
    dir = direction if isinstance(direction, Vector) else Vector(*direction)
    axis = dir.normalized()
    half_a = radians(angle / 2)
    s = sin(half_a)
    x = s * axis.x
    y = s * axis.y
    z = s * axis.z
    w = cos(half_a)
    x2 = x + x
    y2 = y + y
    z2 = z + z
    xx = x * x2
    yx = y * x2
    yy = y * y2
    zx = z * x2
    zy = z * y2
    zz = z * z2
    wx = w * x2
    wy = w * y2
    wz = w * z2  
    return m @ numpy.array([
        [1 - yy - zz, yx - wz, zx + wy, 0],
        [yx + wz, 1 - xx - zz, zy - wx, 0],
        [zx - wy, zy + wx, 1 - xx - yy, 0],
        [0, 0, 0, 1]
    ]) 