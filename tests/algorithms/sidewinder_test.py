from collections.abc import Sequence

from mazes.algorithms import Sidewinder, SidewinderRandom
from mazes.algorithms.utils import flatten
from mazes.core.maze_state import MutableMazeState
from mazes.grid import Coordinate, Grid
from mazes.renderers import TextRenderer

from ..asserts import assert_render


class FakeSidewinderRandom(SidewinderRandom):
    def __init__(self, should_close_out: list[bool]) -> None:
        self._should_close_out = should_close_out
        self._should_close_out_index = 0

    def should_close_out(self) -> bool:
        should_close_out = self._should_close_out[self._should_close_out_index]
        self._should_close_out_index += 1
        return should_close_out

    def choose_north(self, coords: Sequence[Coordinate]) -> Coordinate:
        # Always choose the last item
        return coords[-1]


class TestSidewinder:
    def test_sidewinder_operations(self):
        grid = Grid(3, 3)
        state = MutableMazeState(grid, (0, 1))
        should_close_out = [
            [False, False],  # y == 2
            [True, False],  # y == 1
        ]

        random = FakeSidewinderRandom(flatten(should_close_out))
        sidewinder = Sidewinder(state, random)
        sidewinder.generate()

        text = TextRenderer.render_grid(grid)

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
