import random
from collections.abc import Iterator

from ..core.maze_state import MazeStep, MutableMazeState
from ..direction import Direction
from ..grid import Coordinate
from .algorithm import Algorithm


class BinaryTreeRandom:
    def choose_direction(self, directions: Direction) -> Direction:
        return random.choice(list(directions))


class BinaryTree(Algorithm):
    def __init__(self, state: MutableMazeState, random=BinaryTreeRandom()) -> None:
        self._state = state
        self._random = random

    @property
    def current(self) -> set[Coordinate]:
        return set()

    @property
    def trail(self) -> set[Coordinate]:
        return set()

    @property
    def targets(self) -> set[Coordinate]:
        return set()

    def maze_steps(self) -> Iterator[MazeStep]:
        state = self._state
        grid = state.grid
        random = self._random

        for coord in grid.coordinates_bottom_first():
            neighbors = Direction.Empty
            valid_dirs = grid.valid_directions(coord)
            if Direction.N in valid_dirs:
                neighbors |= Direction.N
            if Direction.E in valid_dirs:
                neighbors |= Direction.E

            state.set_run([coord])
            targets = [dir.update_coordinate(coord) for dir in neighbors]
            state.set_target_coordinates(targets)
            yield state.pop_maze_step()

            if neighbors:
                neighbor = random.choose_direction(neighbors)
                state.grid_link(coord, neighbor)

        state.set_run([])
        yield state.pop_maze_step()
