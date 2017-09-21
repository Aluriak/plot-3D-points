import math
import projection
from projection import Coords
import graph
import render_gif
import geometry
from geometry import Coords


def test_angles_from_coords():
    angles_from_coords = geometry.angles_from_coords
    for x in range(1, 100, 10):
        assert angles_from_coords(Coords(x, 0, 0)) == (0, 90, 90)
    for x in range(1, 100, 10):
        assert angles_from_coords(Coords(0, x, 0)) == (90, 0, 90)
    for x in range(1, 100, 10):
        assert angles_from_coords(Coords(0, 0, x)) == (90, 90, 0)
    assert tuple(map(round, angles_from_coords(Coords(0, 1, 1)))) == (90, 45, 45)
    assert tuple(map(round, angles_from_coords(Coords(1, 0, 1)))) == (45, 90, 45)
    assert tuple(map(round, angles_from_coords(Coords(1, 1, 0)))) == (45, 45, 90)


def test_coords_from_angles():
    coords_from_angles = geometry.coords_from_angles
    assert tuple(map(round, coords_from_angles(Coords(90, 45, 45), math.sqrt(2)))) == (0, 1, 1)
    assert tuple(map(round, coords_from_angles(Coords(45, 90, 45), math.sqrt(2)))) == (1, 0, 1)
    assert tuple(map(round, coords_from_angles(Coords(45, 45, 90), math.sqrt(2)))) == (1, 1, 0)


def test_distance():
    dist = geometry.distance_between
    odist = geometry.distance_to_origin

    a, b = Coords(0, 0, 0), Coords(1, 1, 1)
    assert geometry.distance_to_origin(a) == 0.
    assert dist(a, a) == dist(b, b) == 0.
    assert dist(a, b) == odist(b) == math.sqrt(3)

    c, d, e = Coords(1, 0, 0), Coords(0, 1, 0), Coords(0, 0, 1)
    assert dist(a, c) == dist(a, d) == dist(a, e) == 1.
    assert odist(c) == odist(d) == odist(e) == 1.
    assert dist(d, c) == dist(d, e) == dist(e, c) == math.sqrt(2)

    f = Coords(-7.7, 0, 2.4)
    assert round(odist(f), 2) == round(dist(a, f), 2) == 8.07


def test_origin_switch():
    dist = geometry.distance_between
    a, b = Coords(0, 0, 0), Coords(1, 1, 1)
    c, d, e = Coords(1, 0, 0), Coords(0, 1, 0), Coords(0, 0, 1)
    assert geometry.coords_centered_on(a, b) == Coords(-1, -1, -1)
    assert geometry.coords_centered_on(c, a) == c
    assert geometry.coords_centered_on(d, a) == d
    assert geometry.coords_centered_on(e, a) == e


def test_graph_center():
    assert graph.center(((2, 1), (1, 2), (2, 3), (3, 2))) == (2., 2.)
    assert graph.center(((2, 1, 0), (1, 2, 0), (2, 3, 0), (3, 2, 0))) == (2., 2., 0)


def test_coords_in_system():
    ROUNDING = 4
    rounded = lambda c: Coords(round(c.x, ROUNDING), round(c.y, ROUNDING), round(c.z, ROUNDING))
    coords_in_system = lambda a,b,c: rounded(geometry.coords_in_system(a,b,c))
    a, null = Coords(1, 1, 0), Coords(0, 0, 0)
    assert coords_in_system(a, a, null) == null
    assert coords_in_system(a, null, null) == a
    assert coords_in_system(null, null, null) == null
    assert coords_in_system(null, a, null) == Coords(-1, -1, 0)

    # now, work with angle
    assert rounded(coords_in_system(Coords(1, 1, 0), null, Coords(0, 0, -45))) == rounded(Coords(math.sqrt(2), 0, 0))
    assert rounded(coords_in_system(Coords(1, 1, 0), null, Coords(0, 0, -90))) == rounded(Coords(1, -1, 0))

    # now, rotation and translation !
    for x in range(-90, 90, 20):
        assert rounded(coords_in_system(Coords(1, 1, 10), a, Coords(0, 0, x))) == rounded(Coords(0, 0, 10))
    assert rounded(coords_in_system(a, null, Coords(0, -90, 0))) == rounded(Coords(0, 1, -1))
