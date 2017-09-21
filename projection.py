"""Compute projections of 3D space on 2D spaces.

x and y are the 2D dimension. z is the depth.

"""

import math
from collections import namedtuple
import geometry
from geometry import angles_from_coords


POV_WIDTH = 90
Coords = namedtuple('Coords', 'x, y, z')
Coords2D = namedtuple('Coords2D', 'x, y')
POV = namedtuple('POV', 'coords, rotation, width, height')
# coords: a Coords instance, position of the observer in the world
# orientation: angle in degree between the view axis and the x axis
# elevation: angle in degree between the view axis and the y axis
# width: angle in degree of the view from the x axis
# height: angle in degree of the view from the y axis
Projection = namedtuple('Projection', 'node, position, angles')
# node: the projected object
# position: Coords2D, that are the position of the node on-screen
# angles: Coords2D, that are the angle on witch 


def projection(global_coords:(float, float, float), pov:POV, dot_radius:float=10,
               verbose:bool=True) -> (float, float) or None:
    """Return (x, y, radius) of dot in 2D space for given POV, coords of the dot
    and its radius.

    If the dot is not in the POV field of view, returns None.

    """
    # pov is aligned with x axis and system origin
    coords = geometry.coords_in_system(global_coords, pov.coords, pov.rotation)
    if verbose:
        print()
        print('POV:', pov)
        print('GLOBAL COORDS:', global_coords)
        print('COORDS:', coords)
    distance = geometry.distance_to_origin(coords)
    x_angle_with_origin, y_angle_with_origin, z_angle_with_origin = angles_from_coords(coords)
    if verbose:
        print('ANGLES:', x_angle_with_origin, y_angle_with_origin, z_angle_with_origin)
    _global_dist_ = geometry.distance_between(global_coords, pov.coords)
    # assert distance == _global_dist_, "{} and {} are not equal".format(distance, _global_dist_)

    # determine if the object is in field of view for the x axis
    min_angle_x = -pov.width/2
    max_angle_x = pov.width/2
    if min_angle_x <= x_angle_with_origin <= max_angle_x:
        pass  # the object is printable in x
    else:  # the object is out of the field of view
        if verbose:
            print('X-OUT:', min_angle_x, x_angle_with_origin, max_angle_x)
        return None

    # determine if the object is in field of view for the y axis
    min_angle_y = -pov.height/2 + 90
    max_angle_y = pov.height/2 + 90
    if min_angle_y <= y_angle_with_origin <= max_angle_y:
        pass  # the object is printable in y
    else:  # the object is out of the field of view
        if verbose:
            print('Y-OUT:', min_angle_y, y_angle_with_origin, max_angle_y)
        return None

    # Determine the x coord of the object in the projection
    proj_x = (x_angle_with_origin - min_angle_x) / (max_angle_x - min_angle_x)
    proj_y = (y_angle_with_origin - min_angle_y) / (max_angle_y - min_angle_y)
    size = (1/distance) * dot_radius
    if verbose:
        print('NODE PROJECTIONS:', proj_x, proj_y, '\tsize:', size, '\tdistance:', distance, end='\n\n')
    return proj_x, proj_y, size


def create_pov_toward(global_coords:Coords, pov_coords:Coords) -> POV:
    """Return a POV that is directed toward given global coords and placed at given coords"""
    relative_coords = geometry.coords_centered_on(global_coords, pov_coords)
    angles = geometry.angles_from_coords(relative_coords)
    print('ANGLES:', angles)
    rotation = Coords(
        0,  # camera is straight up, not upside-down or left-right or whatever
        0,  # camera is face to the x axis, so no rotation here
        angles[0],  # camera is face to the object in x
    )
    # rotation = angles

    print('GLOBAL:', global_coords)
    print('ROTATION:', rotation)
    return POV(
        Coords(*pov_coords),
        Coords(*rotation),
        POV_WIDTH, POV_WIDTH,
    )



if __name__ == "__main__":
    pov = POV(Coords(0, 0, 0), (0, 0, 0), 45, 45)
    print(projection(Coords(2, 5, 1), pov))
