from collections.abc import Iterator

from ..grid import Grid, Direction
from .utils import sample
from .algorithm import Algorithm

class BinaryTreeRandom:
    def choose_direction(self, directions: list[Direction]) -> Direction:
        return sample(directions)

class BinaryTree(Algorithm):
    def __init__(self, grid: Grid, random = BinaryTreeRandom()) -> None:
        self._grid = grid
        self._random = random

    def steps(self) -> Iterator[None]:
        grid = self._grid
        random = self._random
        width = grid.width

        for coord in grid.coordinates():
            x, y = coord
            neighbors: list[Direction] = []
            if y > 0:
                neighbors.append(Direction.N)
            if x < width-1:
                neighbors.append(Direction.E)

            if len(neighbors) != 0:
                neighbor = random.choose_direction(neighbors)
                grid.link(coord, neighbor)

            yield
