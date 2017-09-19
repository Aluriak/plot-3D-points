"""Compute projections of 3D space on 2D spaces.

x and y are the 2D dimension. z is the depth.

"""

import math
from collections import namedtuple

Coords = namedtuple('Coords', 'x, y, z')
POV = namedtuple('POV', 'coords, orientation, elevation, width, height')
# coords: a Coords instance, position of the observer in the world
# orientation: angle in degree between the view axis and the x axis
# elevation: angle in degree between the view axis and the y axis
# width: angle in degree of the view from the x axis
# height: angle in degree of the view from the y axis


def projection(coords:(float, float, float), pov:POV, dot_radius:float=10) -> (float, float) or None:
    """Return (x, y, radius) of dot in 2D space for given POV, coords of the dot
    and its radius.

    If the dot is not in the POV field of view, returns None.

    """
    _assertion_dist_ = distance_between(coords, pov.coords)
    print('COORDS:', coords)
    coords = coords_centered_on(coords, pov.coords)  # center on pov
    print('CENTERED_COORDS:', coords)
    distance = distance_to_origin(coords)
    x_angle_with_origin, y_angle_with_origin, z_angle_with_origin = angles_with_origin(coords)
    print('ANGLES:', x_angle_with_origin, y_angle_with_origin, z_angle_with_origin)
    assert distance == _assertion_dist_, "{} and {} are not equal".format(distance, _assertion_dist_)

    # determine if the object is in field of view for the x axis
    field_of_view_min_angle_x = pov.orientation - pov.width/2
    field_of_view_max_angle_x = pov.orientation + pov.width/2
    if field_of_view_min_angle_x <= x_angle_with_origin <= field_of_view_max_angle_x:
        pass  # the object is printable in x
    else:  # the object is out of the field of view
        print('OUT:', field_of_view_min_angle_x, x_angle_with_origin, field_of_view_max_angle_x)
        return None

    # determine if the object is in field of view for the y axis
    field_of_view_min_angle_y = pov.elevation - pov.height/2
    field_of_view_max_angle_y = pov.elevation + pov.height/2
    if field_of_view_min_angle_y <= y_angle_with_origin <= field_of_view_max_angle_y:
        pass  # the object is printable in y
    else:  # the object is out of the field of view
        print('OUT:', field_of_view_min_angle_y, y_angle_with_origin, field_of_view_max_angle_y)
        return None

    # Determine the x coord of the object in the projection
    proj_x = (x_angle_with_origin - field_of_view_min_angle_x) / (field_of_view_max_angle_x - field_of_view_min_angle_x)
    proj_y = (y_angle_with_origin - field_of_view_min_angle_y) / (field_of_view_max_angle_y - field_of_view_min_angle_y)
    size = (1/distance) * dot_radius
    print('PROJECTIONS:', proj_x, proj_y, size, distance)
    print()
    return proj_x, proj_y, size


def angles_with_origin(coords:Coords) -> (float, float, float):
    """Return the angles formed by axis and (origin, coords)"""
    # x = math.atan(math.sqrt(coords.y**2 + coords.z**2) / coords.x) if coords.x != 0 else 0
    # y = math.atan(math.sqrt(coords.x**2 + coords.z**2) / coords.y) if coords.y != 0 else 0
    # z = math.atan(math.sqrt(coords.x**2 + coords.y**2) / coords.z) if coords.z != 0 else 0
    dist = math.sqrt(coords.x**2 + coords.y**2 + coords.z**2)
    if dist == 0.:  return 0, 0, 0
    x = math.degrees(math.acos(coords.x / dist))
    y = math.degrees(math.acos(coords.y / dist))
    z = math.degrees(math.acos(coords.z / dist))
    return x, y, z

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



if __name__ == "__main__":
    pov = POV(Coords(0, 0, 0), 0, 0, 45, 45)
    print(projection(Coords(2, 5, 1), pov))
