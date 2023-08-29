from ..grid import Grid, Direction, Coordinate
from .utils import sample

class BinaryTreeRandom:
    def choose_direction(self, directions: list[Direction]) -> Direction:
        return sample(directions)

class BinaryTree:
    def __init__(self, grid: Grid, random = BinaryTreeRandom()) -> None:
        self._grid = grid
        self._random = random

    def generate(self) -> None:
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

    def generate_all(self) -> None:
        for _ in self.generate():
            pass
