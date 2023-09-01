from collections.abc import Iterator

from ..grid import Grid
from ..direction import Direction
from .utils import sample
from .algorithm import Algorithm


class BinaryTreeRandom:
    def choose_direction(self, directions: list[Direction]) -> Direction:
        return sample(directions)


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
            neighbors: list[Direction] = []
            valid_dirs = grid.valid_directions(coord)
            if Direction.N in valid_dirs:
                neighbors.append(Direction.N)  # type: ignore
            if Direction.E in valid_dirs:
                neighbors.append(Direction.E)  # type: ignore

            if len(neighbors) != 0:
                neighbor = random.choose_direction(neighbors)
                grid.link(coord, neighbor)

            yield
