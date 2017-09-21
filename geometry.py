"""Definition of geometry.

"""
import math
from collections import namedtuple

Coords = namedtuple('Coords', 'x, y, z')
Coords2D = namedtuple('Coords2D', 'x, y')


def coords_in_system(point:Coords, system_origin:Coords,
                     system_rotation:Coords) -> Coords:
    """Return the coords of given point in the coordinate system
    of given origin and with given angles (in degrees) with the standard system.

    """
    point = coords_centered_on(point, system_origin)
    point = with_rotated_axis(point, system_rotation)
    return point


def with_rotated_axis(point:Coords, rotation:Coords) -> Coords:
    """Returns coordinates of given point after given rotation
    (in degrees) for each axis"""
    x_rotation, y_rotation, z_rotation = map(math.radians, rotation)
    px, py, pz = point
    cos, sin = math.cos, math.sin
    if x_rotation:
        py, pz = (
            py * cos(x_rotation) - pz * sin(x_rotation),
            py * sin(x_rotation) + pz * cos(x_rotation)
        )
    if y_rotation:
        px, pz = (
            px * cos(y_rotation) - pz * sin(y_rotation),
            px * sin(y_rotation) + pz * cos(y_rotation)
        )
    if z_rotation:
        px, py = (
            px * cos(z_rotation) - py * sin(z_rotation),
            px * sin(z_rotation) + py * cos(z_rotation)
        )
    return Coords(px, py, pz)


def angles_from_coords(coords:Coords) -> Coords:
    """Return the angles (in degrees) formed by each axis and the line ((0, 0, 0), coords)"""
    dist = math.sqrt(coords.x**2 + coords.y**2 + coords.z**2)
    if dist == 0.:  return 0, 0, 0
    x = math.degrees(math.acos(coords.x / dist))
    y = math.degrees(math.acos(coords.y / dist))
    z = math.degrees(math.acos(coords.z / dist))
    return x, y, z


def coords_from_angles(angles:Coords, distance:float=1.) -> Coords:
    """Return the coords at given distance of origin, and with line ((0, 0, 0), coords)
    having given angles (in degrees) with axis.

    """
    if distance == 0.:
        return Coords(0, 0, 0)
    # print(*((math.radians(angle)) for angle in angles))
    # print(*(math.sin(math.radians(angle)) for angle in angles))
    # print(*(distance * math.cos(math.radians(angle)) for angle in angles))
    return Coords(*(distance * math.cos(math.radians(angle)) for angle in angles))



def distance_to_origin(coords) -> float:
    return distance_between(coords, (0, 0, 0))
def distance_between(a:Coords, b:Coords) -> float:
    ax, ay, az = a
    bx, by, bz = b
    # print('EYTTEC:', (ax - bx), (ay - by), (az - bz))
    return math.sqrt((ax - bx)**2 + (ay - by)**2 + (az - bz)**2)


def coords_centered_on(obj:Coords, origin:Coords) -> Coords:
    """Return the coords of object in the coordinate system is centered
    on given coords.

    """
    return Coords(x=obj.x - origin.x, y=obj.y - origin.y, z=obj.z - origin.z)
