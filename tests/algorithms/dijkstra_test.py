import pytest

from mazes.algorithms import Dijkstra
from mazes.core import MutableMazeState
from mazes.grid import Direction as D
from mazes.grid import Grid
from mazes.renderers import TextRenderer

from ..asserts import assert_distances, assert_render


class TestDijkstra:
    @pytest.mark.skip
    def test_distances(self):
        dijkstra = self.generate_dijkstra()
        distances = dijkstra.distances

        expected = [
            [0, 1, 2, 9],
            [7, 4, 3, 8],
            [6, 5, 6, 7],
            [7, 8, 7, 8],
        ]

        assert_distances(distances, expected)
        assert distances.root == (0, 0)
        assert distances.max_coordinate == (3, 0)
        assert distances.max_distance == 9

    def test_distances_steps(self):
        grid = self.make_grid()
        state = MutableMazeState(grid, (0, 0))
        dijkstra = Dijkstra(grid, (0, 0), state)
        dijkstra.generate()

        distances = state.distances

        expected = [
            [0, 1, 2, 9],
            [7, 4, 3, 8],
            [6, 5, 6, 7],
            [7, 8, 7, 8],
        ]

        assert_distances(distances, expected)
        assert distances.root == (0, 0)
        assert distances.max_coordinate == (3, 0)
        assert distances.max_distance == 9

    def test_path_to(self):
        grid = self.make_grid()
        state = MutableMazeState(grid, (0, 0))
        dijkstra = Dijkstra(grid, (0, 0), state)
        dijkstra.generate()

        distances = dijkstra.path_to((3, 3))

        N = None
        expected = [
            [0, 1, 2, N],
            [N, 4, 3, N],
            [N, 5, 6, N],
            [N, N, 7, 8],
        ]
        assert_distances(distances, expected)
        assert distances.root == (0, 0)
        assert distances.max_coordinate == (3, 3)
        assert distances.max_distance == 8

    @pytest.mark.skip
    def test_longest_path(self):
        grid = self.make_grid()
        state = MutableMazeState(grid, (0, 0))
        dijkstra = Dijkstra(grid, (0, 0), state)
        dijkstra.generate()

        distances = dijkstra.longest_path()

        N = None
        expected = [
            [9, 8, 7, 0],
            [N, 5, 6, 1],
            [N, 4, 3, 2],
            [N, N, N, N],
        ]
        assert_distances(distances, expected)
        assert distances.root == (3, 0)
        assert distances.max_distance == 9
        assert distances.max_coordinate == (0, 0)

    def generate_dijkstra(self) -> Dijkstra:
        grid = self.make_grid()
        state = MutableMazeState(grid, (0, 0))
        dijkstra = Dijkstra(grid, (0, 0), state)
        dijkstra.generate()
        return dijkstra

    def make_grid(self) -> Grid:
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
