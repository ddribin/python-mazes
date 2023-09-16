from pprint import pp

from mazes.algorithms import RecursiveBacktracker, RecursiveBacktrackerRandom
from mazes.algorithms.utils import flatten
from mazes.direction import Direction as D
from mazes.grid import Coordinate, Grid, ImmutableGrid
from mazes.maze_generator import MazeOperation, MutableMazeState
from mazes.renderers import TextRenderer

from ..asserts import assert_render


class FakeRecursiveBacktrackerRandom(RecursiveBacktrackerRandom):
    def __init__(self, start: Coordinate, directions: list[D]) -> None:
        self._start = start
        self._directions = directions
        self._index = 0

    def random_coordinate(self, grid: ImmutableGrid) -> Coordinate:
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
        assert_render(text, expected)

    def test_recursive_backtracker_operations(self) -> None:
        grid = Grid(4, 4)
        state = MutableMazeState(grid, (0, 1))

        directions = [
            [D.N, D.E, D.S, D.S, D.S, D.W, D.N],  # (0, 1) to (0, 2)
            [D.E, D.N, D.E, D.S],  # (1, 3) to (3, 3)
            [D.N, D.N, D.W, D.S],  # (3, 2) to (3, 0)
        ]

        algo = self.make_algorithm(grid, (0, 1), flatten(directions), state)
        saved_ops: list[MazeOperation] = []
        for op in algo.operations():
            saved_ops.append(op)
            state.apply_operation(op)

        text = TextRenderer.render_grid(grid)

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
        assert_render(text, expected)
        pp(saved_ops)

    def render_grid(self, grid: Grid, start: Coordinate, directions: list[D]) -> str:
        random = FakeRecursiveBacktrackerRandom(start, directions)
        algorithm = RecursiveBacktracker(grid, random)
        algorithm.generate()
        text = TextRenderer.render_grid(grid)
        return text

    def make_algorithm(
        self,
        grid: Grid,
        start: Coordinate,
        directions: list[D],
        state: MutableMazeState,
    ) -> RecursiveBacktracker:
        random = FakeRecursiveBacktrackerRandom(start, directions)
        algorithm = RecursiveBacktracker(grid, random, state)
        return algorithm
