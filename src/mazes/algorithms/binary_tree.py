from ..grid import Grid, Direction, Coordinate

import random
from typing import TypeVar, Sequence

T = TypeVar('T')

def sample(l: Sequence[T]) -> T:
    index = random.randint(0, len(l) - 1)
    return l[index]

class BinaryTree:
    def __init__(self, grid: Grid) -> None:
        self._grid = grid

    def generate(self) -> None:
        grid = self._grid
        width = grid.width
        for coord in grid.coordinates():
            x, y = coord
            neighbors: list[Direction] = []
            if y > 0:
                neighbors.append(Direction.N)
            if x < width-1:
                neighbors.append(Direction.E)

            if len(neighbors) != 0:
                neighbor = sample(neighbors)
                grid.link(coord, neighbor)

            yield
