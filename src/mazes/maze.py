from __future__ import annotations

from enum import Enum, auto

from .algorithms import Algorithm, BinaryTree
from .distances import Distances
from .grid import Grid, ImmutableGrid


class Maze:
    class Type(Enum):
        BinaryTree = auto()

    @classmethod
    def generate(
        cls,
        width: int,
        height: int,
        mazeType: Maze.Type,
        calculate_distances: bool = False,
    ) -> Maze:
        grid = Grid(width, height)

        algorithm = Maze.make_algorithm(mazeType, grid)
        algorithm.generate()

        distances: Distances | None = None
        if calculate_distances:
            middle = (int(grid.width / 2), int(grid.height / 2))
            distances = Distances.from_root(grid, middle)

        return Maze(grid, distances)

    @classmethod
    def make_algorithm(cls, mazeType: Maze.Type, grid: Grid) -> Algorithm:
        match mazeType:
            case Maze.Type.BinaryTree:
                return BinaryTree(grid)

            case _:
                return BinaryTree(grid)

    def __init__(self, grid: ImmutableGrid, distances: Distances | None) -> None:
        self._grid = grid
        self._distances = distances
        pass

    @property
    def grid(self) -> ImmutableGrid:
        return self._grid

    @property
    def distances(self) -> Distances | None:
        return self._distances

    @property
    def width(self) -> int:
        return self._grid.width

    @property
    def height(self) -> int:
        return self._grid.height
