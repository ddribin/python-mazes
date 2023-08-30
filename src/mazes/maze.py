from __future__ import annotations

from enum import Enum, auto

from .algorithms import Algorithm, BinaryTree
from .distances import Distances
from .grid import Grid, ImmutableGrid
from .renderers import TextRenderer, ImageRenderer


class Maze:
    class AlgorithmType(Enum):
        BinaryTree = auto()

    @classmethod
    def generate(
        cls,
        width: int,
        height: int,
        algorithmType: Maze.AlgorithmType,
        calculate_distances: bool = False,
    ) -> Maze:
        grid = Grid(width, height)

        algorithm = Maze.make_algorithm(algorithmType, grid)
        algorithm.generate()

        distances: Distances | None = None
        if calculate_distances:
            middle = (int(grid.width / 2), int(grid.height / 2))
            distances = Distances.from_root(grid, middle)

        return Maze(grid, distances)

    @classmethod
    def make_algorithm(cls, mazeType: Maze.AlgorithmType, grid: Grid) -> Algorithm:
        match mazeType:
            case Maze.AlgorithmType.BinaryTree:
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

    def __str__(self) -> str:
        renderer = TextRenderer(self._grid, self._distances)
        text = renderer.render()
        return text

    def write_png(self, file_name: str) -> None:
        renderer = ImageRenderer(self._grid, self._distances)
        renderer.render_png_file(file_name)
