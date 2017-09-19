import math
import projection
from projection import Coords
import graph
import render_gif


def test_angles_with_origin():
    for x in range(1, 100, 10):
        assert projection.angles_with_origin(Coords(x, 0, 0)) == (0, 90, 90)
    for x in range(1, 100, 10):
        assert projection.angles_with_origin(Coords(0, x, 0)) == (90, 0, 90)
    for x in range(1, 100, 10):
        assert projection.angles_with_origin(Coords(0, 0, x)) == (90, 90, 0)
    assert tuple(map(round, projection.angles_with_origin(Coords(0, 1, 1)))) == (90, 45, 45)
    assert tuple(map(round, projection.angles_with_origin(Coords(1, 0, 1)))) == (45, 90, 45)
    assert tuple(map(round, projection.angles_with_origin(Coords(1, 1, 0)))) == (45, 45, 90)


def test_distance():
    dist = projection.distance_between
    odist = projection.distance_to_origin

    a, b = Coords(0, 0, 0), Coords(1, 1, 1)
    assert projection.distance_to_origin(a) == 0.
    assert dist(a, a) == dist(b, b) == 0.
    assert dist(a, b) == odist(b) == math.sqrt(3)

    c, d, e = Coords(1, 0, 0), Coords(0, 1, 0), Coords(0, 0, 1)
    assert dist(a, c) == dist(a, d) == dist(a, e) == 1.
    assert odist(c) == odist(d) == odist(e) == 1.
    assert dist(d, c) == dist(d, e) == dist(e, c) == math.sqrt(2)

    f = Coords(-7.7, 0, 2.4)
    assert round(odist(f), 2) == round(dist(a, f), 2) == 8.07


def test_origin_switch():
    dist = projection.distance_between
    a, b = Coords(0, 0, 0), Coords(1, 1, 1)
    c, d, e = Coords(1, 0, 0), Coords(0, 1, 0), Coords(0, 0, 1)
    assert projection.coords_centered_on(a, b) == Coords(-1, -1, -1)
    assert projection.coords_centered_on(c, a) == c
    assert projection.coords_centered_on(d, a) == d
    assert projection.coords_centered_on(e, a) == e


def test_graph_center():
    assert graph.graph_center(((2, 1), (1, 2), (2, 3), (3, 2))) == (2., 2.)
    assert graph.graph_center(((2, 1, 0), (1, 2, 0), (2, 3, 0), (3, 2, 0))) == (2., 2., 0)
