import random
from collections.abc import Iterator, Sequence

from ..core.maze_state import MazeStep, MutableMazeState
from ..direction import Direction
from ..grid import Coordinate
from .algorithm import Algorithm


class SidewinderRandom:
    def should_close_out(self) -> bool:
        return random.randint(0, 1) == 1

    def choose_north(self, coords: Sequence[Coordinate]) -> Coordinate:
        return random.choice(coords)


class Sidewinder(Algorithm):
    def __init__(
        self,
        state: MutableMazeState,
        random=SidewinderRandom(),
    ) -> None:
        self._state = state
        self._random = random
        self._current: set[Coordinate] = set()
        self._trail: set[Coordinate] = set()
        self._targets: set[Coordinate] = set()

    @property
    def current(self) -> set[Coordinate]:
        return self._current

    @property
    def trail(self) -> set[Coordinate]:
        return self._trail

    @property
    def targets(self) -> set[Coordinate]:
        return self._targets

    def maze_steps(self) -> Iterator[MazeStep]:
        state = self._state
        grid = state.grid
        random = self._random

        for y in reversed(range(grid.height)):
            state.set_run([])

            for x in range(grid.width):
                coord = (x, y)
                state.push_run(coord)

                valid_dirs = grid.valid_directions(coord)
                at_eastern_boundary = Direction.E not in valid_dirs
                at_northern_boundary = Direction.N not in valid_dirs

                should_close_out = at_eastern_boundary or (
                    not at_northern_boundary and random.should_close_out()
                )

                if should_close_out:
                    targets = [
                        Direction.N.update_coordinate(coord) for coord in state.run
                    ]
                    state.set_target_coordinates(targets)
                    yield state.pop_maze_step()

                    member = random.choose_north(state.run)
                    state.grid_link(member, Direction.N)
                    state.set_run([])
                else:
                    targets = [Direction.E.update_coordinate(coord)]
                    state.set_target_coordinates(targets)
                    yield state.pop_maze_step()

                    state.grid_link(coord, Direction.E)

        self._current = set()
        self._trail = set()
        self._targets = set()
        yield state.pop_maze_step()
