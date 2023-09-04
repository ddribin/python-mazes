from mazes.algorithms import RecursiveBacktracker, RecursiveBacktrackerRandom
from mazes.algorithms.utils import flatten
from mazes.direction import Direction as D
from mazes.grid import Coordinate, Grid
from mazes.renderers import TextRenderer

from ..asserts import *


class FakeRecursiveBacktrackerRandom(RecursiveBacktrackerRandom):
    def __init__(self, start: Coordinate, directions: list[D]) -> None:
        self._start = start
        self._directions = directions
        self._index = 0

    def random_coordinate(self, grid: Grid) -> Coordinate:
        return (0, 1)

    def choose_direction(self, directions: D) -> D:
        direction = self._directions[self._index]
        self._index += 1
        return direction


class TestRecursiveBacktracker:
    def test_recursive_backtracer(self):
        grid = Grid(4, 4)

        directions = [
            [D.N, D.E, D.S, D.S, D.S, D.W, D.N],  # (0, 1) to (0, 2)
            [D.E, D.N, D.E, D.S],  # (1, 3) to (3, 3)
            [D.N, D.N, D.W, D.S],  # (3, 2) to (3, 0)
        ]
        text = self.render_grid(grid, (0, 1), flatten(directions))

        expected = """
            +---+---+---+---+
            |       |       |
            +   +   +   +   +
            |   |   |   |   |
            +---+   +---+   +
            |   |   |       |
            +   +   +   +   +
            |           |   |
            +---+---+---+---+
            """
        print(text)
        print(expected)
        assert_render(text, expected)

    def render_grid(self, grid: Grid, start: Coordinate, directions: list[D]) -> str:
        random = FakeRecursiveBacktrackerRandom(start, directions)
        sidewinder = RecursiveBacktracker(grid, random)
        sidewinder.generate()
        text = TextRenderer.render_grid(grid)
        return text
