"""Render graphs in 3D space.

Nodes are points in the 3D space.

"""

import math
import itertools

import imageio
from PIL import Image, ImageDraw

import graph as graph_module
from graph import Graph
import geometry
import projection
from projection import Coords, POV


POV_WIDTH = 90


def points_on_circle(center:(float, float), radius:float, nb_point:int=10) -> (float, float):
    pi, cos, sin = math.pi, math.cos, math.sin
    assert nb_point > 0
    arc = (2*pi / nb_point)
    for doti in range(nb_point):
        x = cos(arc * doti) * radius
        y = sin(arc * doti) * radius
        yield x + center[0], y + center[1]


def draw_3d_graph(graph:Graph, pov_coords:Coords, fname:str='graph.png',
                  verbose:bool=True):
    """Draw a projection of given graph"""
    amplitudes, center = graph.amplitudes, graph.center
    pov_coords = Coords(*pov_coords)
    pov = projection.create_pov_toward(center, pov_coords)
    print('CENTER PROJECTION:', projection.projection(center, pov, verbose=verbose))
    # exit()
    if verbose:
        print('POV:', pov)
        # print('ANGLES OF CENTER:', geometry.angles_from_coords(geometry.coords_centered_on(center, pov.coords)))
    nodes_projections = {
        node: projection.projection(Coords(*node), pov, verbose=verbose)
        for node in graph.nodes
    }
    # draw_map(pov, nodes_projections, center, center)
    if verbose:
        print('NODES PROJECTIONS:', nodes_projections)
    graph_2d = frozenset(
        (nodes_projections[source], nodes_projections[target])
        for source, target in graph.links
        if nodes_projections[source] and nodes_projections[target]
    )
    if verbose:
        print('2D GRAPH:', graph_2d)
    draw_2d_graph(graph_2d, fname=fname, center=projection.projection(center, pov, verbose=verbose))


ITER = 0
def draw_map(pov:POV, projections:dict, center:Coords, relative_center:Coords,
             fname:str='maps/map_{num:03d}.png', size:int=400):
    assert pov.coords.y == center.y
    REC = 4  # points semi-size
    im = Image.new('RGBA', (size, size), 'black')
    draw = ImageDraw.Draw(im)
    # draw various dot objects
    focus = lambda x, z: (x + size // 2 - center.x, z + size // 2 - center.z)
    # focus = lambda x: x + size // 2
    rectangle_at = lambda x, z, col: draw.rectangle((*focus(x-REC, z-REC), *focus(x+REC, z+REC)), fill=col)
    rectangle_at(pov.coords.x, pov.coords.z, 'blue')  # pov position
    rectangle_at(center.x, center.z, 'red')  # absolute center of the graph
    rectangle_at(relative_center.x, relative_center.z, 'yellow')  # center relative to pov position when placed at the center of image

    for coords, ratios in projections.items():
        # print the node itself
        rectangle_at(coords[0], coords[2], 'white')
        # print a line on which the node should be.
        point_one = pov.coords.x, pov.coords.z
        # computation of point two
        ratio_x, _, _ = ratios
        print('RATIO:', ratio_x)
        # geometry power: what is the angle of this line with the x axis ?
        #  you probably need pen and paper to understand this, by drawing it.
        #  this is basically the function that maps the x position of the node
        #  with its angle with POV's orientation axis.
        line_angle = math.radians(pov.orientation) - math.atan(
            abs((0.5 - ratio_x) * size)  # the section of the screen between center and point to print
            /  # opposite side over adjacent side
            ((size/2) / math.tan(math.radians(90 - pov.width / 2)))
        )
        print('LINE ANGLE:', line_angle, '\tin degrees:', math.degrees(line_angle))
        dist_on_x = 220
        point_two = (
            center.x - pov.coords.x + dist_on_x,
            center.z - pov.coords.z + dist_on_x * math.tan(line_angle)
        )
        draw.line((*focus(*point_one), *focus(*point_two)), fill='white')

    # print the orientation of the POV
    point_one = pov.coords.x, pov.coords.z
    dist_on_z = 200
    print('ORIENTATION:', pov.orientation, math.radians(pov.orientation))
    line_angle = math.radians(pov.orientation)  # the remaining expression equals atan(0) == 0
    print('LINE ANGLE:', line_angle, '\tin degrees:', math.degrees(line_angle))
    dist_on_x = 220
    point_two = (
        center.x - pov.coords.x + dist_on_x,
        center.z - pov.coords.z + dist_on_x * math.tan(line_angle)
    )
    draw.line((*focus(*point_one), *focus(*point_two)), fill='red')


    global ITER
    im.save(fname.format(num=ITER))
    ITER += 1


def draw_2d_graph(graph:[(float, float, float), (float, float, float)],
                  fname:str, width:int=400, height:int=400,
                  nodes_color:dict={}, center:(float, float, float)=None):
    """

    Nodes are represented by 3 values: x position, y position and size.

    """
    im = Image.new('RGBA', (width, height), 'black')
    draw = ImageDraw.Draw(im)
    # draw the edges
    scaled_graph = frozenset((
        ((sx*width, sy*height, st+1), (tx*width, ty*height, tt+1))
        for (sx, sy, st), (tx, ty, tt) in graph
    ))

    for (sx, sy, _), (tx, ty, _) in scaled_graph:  # source and target's x, y and size
        # print('EWFDZM:', sx, sy, tx, ty)
        draw.line(((sx, sy), (tx, ty)), fill='white')

    # draw the stars
    nodes = frozenset(itertools.chain.from_iterable(scaled_graph))
    for x, y, size in nodes:
        color = [int(size * 255)] * 3 + [255]
        draw.rectangle((x-size/2, y-size/2, x+size/2, y+size/2), fill=tuple(color))

    # draw the center
    if center:
        x, y, size = center
        x *= width
        y *= height
        draw.rectangle((x-size/2, y-size/2, x+size/2, y+size/2), fill='red')

    im.save(fname)


def run_things(graph, nb_point=100, distance_to_object_factor:float=4.7,
               fname_template:str='output/graph_{num:03d}.png',
               verbose:bool=True):
    dist_to_center = (max(graph.amplitudes[0], graph.amplitudes[2])/2) * distance_to_object_factor
    points = points_on_circle((graph.center.x, graph.center.z), dist_to_center, nb_point=nb_point)
    for n, (x, z) in enumerate(points, start=1):
        print('CIRCLING BY:', x , z)
        fname = fname_template.format(num=n)
        draw_3d_graph(graph, pov_coords=Coords(x, graph.center.y, z),
                      fname=fname, verbose=verbose)
        yield fname


def write_gif(filenames, duration:float=1):
    with imageio.get_writer('graph.gif', mode='I', duration=duration) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)


def draw_circle(nb_point:int=1000):
    """Proof that points_on_circle works well"""
    im = Image.new('RGBA', (1000, 1000), 'black')
    draw = ImageDraw.Draw(im)
    points = points_on_circle((500, 500), 100, nb_point=nb_point)
    size = 6
    for idx, (x, y) in enumerate(points):
        color = (int((y / 300) * 255),) * 3 + (255,)
        color = 'white'
        color = tuple([int(100 + 155 * idx / (nb_point))] * 3 + [255])
        draw.point((x, y), fill=color)
        # draw.rectangle((x-size/2, y-size/2, x+size/2, y+size/2), fill=color)

    im.save('circle.png')


if __name__ == "__main__":
    # draw_circle() ; exit()  # proof that circle is a circleworks

    # data = graph_module.cube()
    data = graph_module.double_tetrahedron()
    # write_gif(run_things(data, nb_point=100, verbose=False), duration=0.01)
    write_gif(run_things(data, nb_point=1, fname_template='graph.png', verbose=True))
