from itertools import chain

from mazes.algorithms import Dijkstra
from mazes.grid import Grid, ImmutableGrid, Direction as D
from mazes.renderers import TextRenderer

from ..asserts import *


class TestDijkstra:
    def test_dijstra(self):
        grid = self.make_grid()
        dijkstra = Dijkstra(grid, (0, 0))

        dijkstra.generate()

        expected = [
            [0, 1, 2, 9],
            [7, 4, 3, 8],
            [6, 5, 6, 7],
            [7, 8, 7, 8],
        ]

        distances = dijkstra.distances
        for y in range(4):
            for x in range(4):
                assert distances[x, y] == expected[y][x], f"({x=}, {y=})"

        assert dijkstra.max_distance == 9
        assert dijkstra.max_coordinate == (3, 0)

    def make_grid(self) -> ImmutableGrid:
        grid = Grid(4, 4)

        coord = grid.link_path((0, 0), [D.E, D.E, D.S, D.W, D.S])
        assert coord == (1, 2)

        coord = grid.link_path((1, 2), [D.W, D.N])
        assert coord == (0, 1)

        coord = grid.link_path((0, 2), [D.S])
        assert coord == (0, 3)

        coord = grid.link_path((1, 2), [D.E])
        assert coord == (2, 2)

        coord = grid.link_path((2, 2), [D.E, D.N, D.N])
        assert coord == (3, 0)

        coord = grid.link_path((2, 2), [D.S])
        assert coord == (2, 3)

        coord = grid.link_path((2, 3), [D.E])
        assert coord == (3, 3)

        coord = grid.link_path((2, 3), [D.W])
        assert coord == (1, 3)

        expected = (
            #  0   1   2   3
            "+---+---+---+---+\n"
            "|           |   |\n"  # 0
            "+---+---+   +   +\n"
            "|   |       |   |\n"  # 1
            "+   +   +---+   +\n"
            "|               |\n"  # 2
            "+   +---+   +---+\n"
            "|   |           |\n"  # 3
            "+---+---+---+---+\n"
        )
        text = TextRenderer.render_grid(grid)
        assert_render(text, expected)

        return grid
