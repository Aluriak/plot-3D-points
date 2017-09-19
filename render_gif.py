"""Render graphs in 3D space.

Nodes are points in the 3D space.

"""

import math
import itertools

import imageio
from PIL import Image, ImageDraw

import graph as graph_module
from graph import Graph
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


def draw_3d_graph(graph:Graph, pov_coords:POV, fname:str='graph.png',
                  verbose:bool=True):
    """Draw a projection of given graph"""
    amplitudes, center = graph.amplitudes, graph.center
    pov_coords = Coords(*pov_coords)
    center_coords_centered = projection.coords_centered_on(center, pov_coords)
    pov = projection.POV(
        pov_coords,
        *projection.angles_with_origin(center_coords_centered)[:2],  # directed toward the center of the graph
        POV_WIDTH, POV_WIDTH,
    )
    if verbose:
        print('POV:', pov)
        print('ANGLES OF CENTER:', projection.angles_with_origin(center))
    nodes_projections = {
        node: projection.projection(Coords(*node), pov, verbose=verbose)
        for node in graph.nodes
    }
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
