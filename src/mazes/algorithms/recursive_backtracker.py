import random
from collections.abc import Iterator

from ..direction import Direction
from ..grid import Coordinate, Grid, ImmutableGrid
from ..maze_generator import (  # MazeOpPopStack,
    MazeOperations,
    MazeOpLink,
    MazeOpPopStack,
    MazeOpPushStack,
    MazeState,
)
from .algorithm import Algorithm


class RecursiveBacktrackerRandom:
    def random_coordinate(self, grid: ImmutableGrid) -> Coordinate:
        x = random.randrange(0, grid.width)
        y = random.randrange(0, grid.height)
        return (x, y)

    def choose_direction(self, directions: Direction) -> Direction:
        return random.choice(list(directions))


class RecursiveBacktracker(Algorithm):
    def __init__(
        self,
        grid: Grid,
        random=RecursiveBacktrackerRandom(),
        state: MazeState | None = None,
    ) -> None:
        self._grid = grid
        self._random = random
        self._current: set[Coordinate] = set()
        self._trail: set[Coordinate] = set()
        self._targets: set[Coordinate] = set()
        self._state = state

    @property
    def current(self) -> set[Coordinate]:
        return self._current

    @property
    def trail(self) -> set[Coordinate]:
        return self._trail

    @property
    def targets(self) -> set[Coordinate]:
        return self._targets

    def steps(self) -> Iterator[None]:
        grid = self._grid
        random = self._random

        start_at = random.random_coordinate(grid)
        stack = [start_at]

        while stack:
            current = stack[-1]
            valid_dirs = grid.valid_directions(current)
            available_directions = Direction.Empty
            for dir in valid_dirs:
                coord = dir.update_coordinate(current)
                if not grid[coord]:
                    available_directions |= dir
                    coord = dir.update_coordinate(current)

            self._current = {current}
            self._trail = set(stack)

            if not available_directions:
                self._targets = set()
                yield
                stack.pop()
            else:
                self._targets = {
                    dir.update_coordinate(current) for dir in available_directions
                }
                yield
                next_direction = random.choose_direction(available_directions)
                grid.link(current, next_direction)
                next_coord = next_direction.update_coordinate(current)
                stack.append(next_coord)

        self._current = set()
        self._trail = set()
        self._targets = set()
        yield

    def initial_operations(self) -> MazeOperations:
        state = self._state
        assert state is not None

        grid = state.grid
        random = self._random
        start_at = random.random_coordinate(grid)
        return [MazeOpPushStack(start_at)]

    def operations(self) -> Iterator[MazeOperations]:
        state = self._state
        assert state is not None
        grid = state.grid
        stack = state.stack
        random = self._random

        start_at = random.random_coordinate(grid)
        yield [MazeOpPushStack(start_at)]

        while stack:
            current = stack[-1]
            valid_dirs = grid.valid_directions(current)
            available_directions = Direction.Empty
            for dir in valid_dirs:
                coord = dir.update_coordinate(current)
                if not grid[coord]:
                    available_directions |= dir
                    coord = dir.update_coordinate(current)

            if not available_directions:
                yield [MazeOpPopStack()]
            else:
                next_direction = random.choose_direction(available_directions)
                next_coord = next_direction.update_coordinate(current)

                yield [MazeOpLink(current, next_direction), MazeOpPushStack(next_coord)]
                # grid.link(current, next_direction)
                # stack.append(next_coord)
