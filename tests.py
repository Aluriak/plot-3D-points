import projection
from projection import Coords
import render_gif


def test_angles_with_origin():
    for x in range(1, 100, 10):
        assert projection.angles_with_origin(Coords(x, 0, 0)) == (90, 0, 0)
    for x in range(1, 100, 10):
        assert projection.angles_with_origin(Coords(0, x, 0)) == (0, 90, 0)
    for x in range(1, 100, 10):
        assert projection.angles_with_origin(Coords(0, 0, x)) == (0, 0, 90)
    assert tuple(map(round, projection.angles_with_origin(Coords(0, 1, 1)))) == (0, 45, 45)
    assert tuple(map(round, projection.angles_with_origin(Coords(1, 0, 1)))) == (45, 0, 45)
    assert tuple(map(round, projection.angles_with_origin(Coords(1, 1, 0)))) == (45, 45, 0)


def test_graph_center():
    assert render_gif.graph_center(((2, 1), (1, 2), (2, 3), (3, 2))) == (2., 2.)
    assert render_gif.graph_center(((2, 1, 0), (1, 2, 0), (2, 3, 0), (3, 2, 0))) == (2., 2., 0)
