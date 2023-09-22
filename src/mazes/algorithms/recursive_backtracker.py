import logging
import random
from collections.abc import Iterator

from ..core.maze_state import MazeStep, MutableMazeState
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
        state: MutableMazeState,
        random=RecursiveBacktrackerRandom(),
    ) -> None:
        self._state = state
        self._random = random
        self._logger = logging.getLogger(__name__)

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
