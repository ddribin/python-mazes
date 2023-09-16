import logging
import random
from collections.abc import Iterator

from ..direction import Direction
from ..grid import Coordinate, Grid, ImmutableGrid
from ..maze_generator import (
    MazeOperation,
    MazeOpGridLink,
    MazeOpPopRun,
    MazeOpPushRun,
    MazeOpSetTargetCoords,
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
        self._logger = logging.getLogger(__name__)

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
        self._current = {stack[-1]}
        self._trail = set(stack)

        while stack:
            current = stack[-1]
            available_directions = grid.available_directions(current)

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

    def send_op(self, op: MazeOperation) -> Iterator[MazeOperation]:
        yield op

    def operations(self) -> Iterator[MazeOperation]:
        state = self._state
        assert state is not None
        grid = state.grid
        stack = state.run
        random = self._random

        start_at: Coordinate | None = random.random_coordinate(grid)
        yield MazeOpPushRun(start_at)

        while stack:
            current = stack[-1]
            available_directions = grid.available_directions(current)
            self._logger.debug(
                "stack=%r available_directions=%r targets=%r",
                stack,
                available_directions,
                state.target_coordinates,
            )

            if not available_directions:
                yield MazeOpSetTargetCoords([])
                yield MazeOpPopRun()
            else:
                next_direction = random.choose_direction(available_directions)
                next_coord = next_direction.update_coordinate(current)
                targets = self.targets_from_directions(current, available_directions)

                yield MazeOpGridLink(current, next_direction)
                yield MazeOpPushRun(next_coord)
                yield MazeOpSetTargetCoords(targets)

    def targets_from_directions(
        self, coord: Coordinate, directions: Direction
    ) -> list[Coordinate]:
        targets = [dir.update_coordinate(coord) for dir in directions]
        return targets
