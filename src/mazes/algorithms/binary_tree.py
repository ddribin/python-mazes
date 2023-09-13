import random
from collections.abc import Iterator

from ..direction import Direction
from ..grid import Coordinate, Grid
from .algorithm import Algorithm


class BinaryTreeRandom:
    def choose_direction(self, directions: Direction) -> Direction:
        return random.choice(list(directions))


class BinaryTree(Algorithm):
    def __init__(self, grid: Grid, random=BinaryTreeRandom()) -> None:
        self._grid = grid
        self._random = random
        self._current: set[Coordinate] = set()
        self._targets: set[Coordinate] = set()

    @property
    def current(self) -> set[Coordinate]:
        return self._current

    @property
    def trail(self) -> set[Coordinate]:
        return set()

    @property
    def targets(self) -> set[Coordinate]:
        return self._targets

    def steps(self) -> Iterator[None]:
        grid = self._grid
        random = self._random

        for coord in grid.coordinates():
            x, y = coord
            neighbors = Direction.Empty
            valid_dirs = grid.valid_directions(coord)
            if Direction.N in valid_dirs:
                neighbors |= Direction.N
            if Direction.E in valid_dirs:
                neighbors |= Direction.E

            self._current = {coord}
            self._targets = {dir.update_coordinate(coord) for dir in neighbors}
            yield

            if neighbors:
                neighbor = random.choose_direction(neighbors)
                grid.link(coord, neighbor)

        self._current = set()
        self._targets = set()
        yield
