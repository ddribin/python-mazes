from ..grid import Grid, Direction, Coordinate

import random
from typing import TypeVar, Sequence

T = TypeVar('T')

def sample(l: Sequence[T]) -> T:
    index = random.randint(0, len(l) - 1)
    return l[index]

class BinaryTree:
    @classmethod
    def on(cls, grid: Grid) -> None:
        width = grid.width
        for coord, linked in grid:
            x, y = coord
            neighbors: list[Direction] = []
            if y > 0 and Direction.N not in linked:
                neighbors.append(Direction.N) # type: ignore
            if x < width-1 and Direction.E not in linked:
                neighbors.append(Direction.E) # type: ignore

            if len(neighbors) != 0:
                neighbor = sample(neighbors)
                grid.link(coord, neighbor)
