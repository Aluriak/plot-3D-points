"""Definition and functions around the Graph object,
and repository of many example graphs.

"""

import itertools
from collections import namedtuple

from projection import Coords

Graph = namedtuple('Graph', 'links, center, nodes, dimensions, amplitudes')


def graph_from_edges(graph:[(float, float, float), (float, float, float)]) -> Graph:
    nodes = frozenset(itertools.chain.from_iterable(graph))
    print('NODES:', nodes)
    center_ = Coords(*center(nodes))
    print('CENTER:', center_)
    return Graph(graph, center_, nodes, dimensions(nodes), amplitudes(nodes))


def center(nodes:[(float, ..., float)]) -> (float, ..., float):
    """Return the center of given nodes in space of whatever dimension"""
    by_coords = tuple(zip(*nodes))
    center = lambda s: ((max(s) - min(s)) / 2) + min(s)
    return tuple(map(center, by_coords))

def dimensions(nodes:[(float, ..., float)]) -> float:
    """Return the maximal difference of coords in each dimension"""
    by_coords = tuple(zip(*nodes))
    dims = lambda s: (max(s), min(s))
    return tuple(map(dims, by_coords))

def amplitudes(nodes:[(float, ..., float)]) -> float:
    """Return the amplitude of coords in each dimension"""
    by_coords = tuple(zip(*nodes))
    diff = lambda s: max(s) - min(s)
    return tuple(map(diff, by_coords))


def cube() -> Graph:
    return graph_from_edges((  # a cube
        # front square
        ((2, 2, 5), (2, 4, 5)),
        ((2, 4, 5), (4, 4, 5)),
        ((4, 4, 5), (4, 2, 5)),
        ((4, 2, 5), (2, 2, 5)),
        # back square
        ((3, 3, 7), (3, 5, 7)),
        ((3, 5, 7), (5, 5, 7)),
        ((5, 5, 7), (5, 3, 7)),
        ((5, 3, 7), (3, 3, 7)),
        # links between the two
        ((2, 2, 5), (3, 3, 7)),
        ((2, 4, 5), (3, 5, 7)),
        ((4, 2, 5), (5, 3, 7)),
        ((4, 4, 5), (5, 5, 7)),
    ))


def double_tetrahedron() -> Graph:
    return graph_from_edges((
        # front dot, linked to the four dots of the square
        ((50, 50, 10), (20, 20, 50)),
        ((50, 50, 10), (20, 80, 50)),
        ((50, 50, 10), (80, 20, 50)),
        ((50, 50, 10), (80, 80, 50)),
        # the square itself
        ((20, 80, 50), (80, 80, 50)),
        ((20, 80, 50), (20, 20, 50)),
        ((80, 20, 50), (80, 80, 50)),
        ((80, 20, 50), (20, 20, 50)),
        # back dot, linked to the four dots of the square,
        #  and slightly closer to it than front dot
        ((50, 50, 70), (20, 20, 50)),
        ((50, 50, 70), (20, 80, 50)),
        ((50, 50, 70), (80, 20, 50)),
        ((50, 50, 70), (80, 80, 50)),
    ))
