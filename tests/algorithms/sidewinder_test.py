from mazes.algorithms import Sidewinder, SidewinderRandom
from mazes.algorithms.utils import flatten
from mazes.grid import Coordinate, Grid
from mazes.renderers import TextRenderer

from ..asserts import *


class FakeSidewindoerRandom(SidewinderRandom):
    def __init__(self, should_close_out: list[bool]) -> None:
        self._should_close_out = should_close_out
        self._should_close_out_index = 0

    def should_close_out(self) -> bool:
        should_close_out = self._should_close_out[self._should_close_out_index]
        self._should_close_out_index += 1
        return should_close_out

    def choose_north(self, coords: list[Coordinate]) -> Coordinate:
        # Always choose the last item
        return coords[-1]


class TestSidewinder:
    def test_sidewinder(self):
        grid = Grid(3, 3)
        should_close_out = [
            [True, False, False],  # y == 1
            [False, False, False],  # y == 2
        ]

        text = self.render_grid(grid, should_close_out)

        # Random seed of 5402118375022309858!!
        expected = """
            +---+---+---+
            |           |
            +   +---+   +
            |   |       |
            +---+---+   +
            |           |
            +---+---+---+
            """
        assert_render(text, expected)

    def render_grid(self, grid: Grid, should_close_out: list[list[bool]]) -> str:
        random = FakeSidewindoerRandom(flatten(should_close_out))
        sidewinder = Sidewinder(grid, random)
        sidewinder.generate()
        text = TextRenderer.render_grid(grid)
        return text
