from collections.abc import Iterator
import random

from ..grid import Grid
from ..direction import Direction
from .algorithm import Algorithm


class BinaryTreeRandom:
    def choose_direction(self, directions: Direction) -> Direction:
        return random.choice(list(directions))


class BinaryTree(Algorithm):
    def __init__(self, grid: Grid, random=BinaryTreeRandom()) -> None:
        self._grid = grid
        self._random = random

    def steps(self) -> Iterator[None]:
        grid = self._grid
        random = self._random
        width = grid.width

        for coord in grid.coordinates():
            x, y = coord
            neighbors = Direction.Empty
            valid_dirs = grid.valid_directions(coord)
            if Direction.N in valid_dirs:
                neighbors |= Direction.N
            if Direction.E in valid_dirs:
                neighbors |= Direction.E

            if neighbors != Direction.Empty:
                neighbor = random.choose_direction(neighbors)
                grid.link(coord, neighbor)

            yield
