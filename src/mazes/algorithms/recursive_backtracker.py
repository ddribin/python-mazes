import logging
import random
from collections.abc import Iterator

from ..core.maze_state import MazeState, MazeStep
from ..direction import Direction
from ..grid import Coordinate, ImmutableGrid
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
        state: MazeState,
        random=RecursiveBacktrackerRandom(),
    ) -> None:
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
        raise NotImplementedError()

    def maze_steps(self) -> Iterator[MazeStep]:
        state = self._state
        assert state is not None
        grid = state.grid
        stack = state.run
        random = self._random

        start_at = random.random_coordinate(grid)
        state.push_run(start_at)

        while stack:
            current = stack[-1]
            available_directions = grid.available_directions(current)

            if not available_directions:
                state.set_target_coordinates([])
                yield state.pop_maze_step()
                state.pop_run()
            else:
                targets = self.targets_from_directions(current, available_directions)
                state.set_target_coordinates(targets)
                yield state.pop_maze_step()

                next_direction = random.choose_direction(available_directions)
                next_coord = next_direction.update_coordinate(current)
                state.grid_link(current, next_direction)
                state.push_run(next_coord)

        yield state.pop_maze_step()

    def targets_from_directions(
        self, coord: Coordinate, directions: Direction
    ) -> list[Coordinate]:
        targets = [dir.update_coordinate(coord) for dir in directions]
        return targets
