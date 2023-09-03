from __future__ import annotations

from enum import Enum, auto

from .algorithms import (
    Algorithm,
    BinaryTree,
    Sidewinder,
    RecursiveBacktracker,
    Dijkstra,
)
from .distances import Distances
from .grid import Grid, ImmutableGrid, Coordinate
from .renderers import TextRenderer, ImageRenderer


class Maze:
    class AlgorithmType(Enum):
        BinaryTree = auto()
        Sidewinder = auto()
        RecursiveBacktracker = auto()

    class OverlayType(Enum):
        Nothing = auto()
        Distance = auto()
        PathTo = auto()
        PathToMax = auto()
        LongestPath = auto()

    @classmethod
    def generate(
        cls,
        width: int,
        height: int,
        algorithmType: Maze.AlgorithmType,
        overlayType=OverlayType.Nothing,
    ) -> Maze:
        grid = Grid(width, height)

        algorithm = Maze.make_algorithm(algorithmType, grid)
        algorithm.generate()

        return Maze(grid, overlayType)

    @classmethod
    def make_algorithm(cls, mazeType: Maze.AlgorithmType, grid: Grid) -> Algorithm:
        match mazeType:
            case Maze.AlgorithmType.BinaryTree:
                return BinaryTree(grid)
            case Maze.AlgorithmType.Sidewinder:
                return Sidewinder(grid)
            case Maze.AlgorithmType.RecursiveBacktracker:
                return RecursiveBacktracker(grid)
            case unknown:
                raise ValueError(unknown)

    def __init__(self, grid: ImmutableGrid, overlayType: Maze.OverlayType) -> None:
        self._grid = grid
        self._overlayType = overlayType
        self._dijkstra = self._generate_dijkstra()

    def _generate_dijkstra(self) -> Dijkstra:
        dijkstra: Dijkstra
        if self._overlayType == Maze.OverlayType.Distance:
            center = self._grid.center
            dijkstra = Dijkstra(self._grid, center)
        else:
            dijkstra = Dijkstra(self._grid, (0, 0))
        dijkstra.generate()
        return dijkstra

    @property
    def grid(self) -> ImmutableGrid:
        return self._grid

    @property
    def width(self) -> int:
        return self._grid.width

    @property
    def height(self) -> int:
        return self._grid.height

    def distances(self) -> Distances | None:
        match self._overlayType:
            case Maze.OverlayType.Distance:
                return self._dijkstra.distances

            case Maze.OverlayType.PathTo:
                goal = self._grid.southeast_corner
                return self._dijkstra.path_to(goal)

            case Maze.OverlayType.PathToMax:
                goal = self._dijkstra.max_coordinate
                return self._dijkstra.path_to(goal)

            case Maze.OverlayType.LongestPath:
                return self._dijkstra.longest_path()

            case Maze.OverlayType.Nothing:
                return None

            case unknown:
                raise ValueError(unknown)

    def max_distance(self) -> int:
        if self._overlayType == Maze.OverlayType.Distance:
            return self._dijkstra.max_distance
        else:
            return 0

    def __str__(self) -> str:
        renderer = TextRenderer(self._grid, self.distances())
        text = renderer.render()
        return text

    def write_png(self, file_name: str) -> None:
        renderer = ImageRenderer(self._grid, self.distances(), self.max_distance())
        renderer.render_png_file(file_name)
