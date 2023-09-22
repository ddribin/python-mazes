from __future__ import annotations

from enum import Enum, auto

from .algorithms import (
    Algorithm,
    BinaryTree,
    Dijkstra,
    RecursiveBacktracker,
    Sidewinder,
)
from .core.maze_state import MutableMazeState
from .distances import Distances
from .grid import Grid, ImmutableGrid
from .renderers import Color, ImageRenderer, TextRenderer


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
        state = MutableMazeState(grid, (0, 0))

        algorithm = Maze.make_algorithm(algorithmType, grid, state)
        algorithm.generate()

        return Maze(grid, overlayType)

    @classmethod
    def make_algorithm(
        cls, mazeType: Maze.AlgorithmType, grid: Grid, state: MutableMazeState
    ) -> Algorithm:
        match mazeType:
            case Maze.AlgorithmType.BinaryTree:
                return BinaryTree(grid)
            case Maze.AlgorithmType.Sidewinder:
                return Sidewinder(state)
            case Maze.AlgorithmType.RecursiveBacktracker:
                return RecursiveBacktracker(state)
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
                goal = self._dijkstra.distances.max_coordinate
                return self._dijkstra.path_to(goal)

            case Maze.OverlayType.LongestPath:
                return self._dijkstra.longest_path()

            case Maze.OverlayType.Nothing:
                return None

            case unknown:
                raise ValueError(unknown)

    def gradient(self) -> tuple[Color, Color]:
        if self._overlayType == Maze.OverlayType.Distance:
            return ((255, 255, 255), (0, 128, 128))
        else:
            return ((255, 0, 0), (0, 255, 0))

    def __str__(self) -> str:
        renderer = TextRenderer(self._grid, self.distances())
        text = renderer.render()
        return text

    def write_png(self, file_name: str) -> None:
        gradient_start, gradient_end = self.gradient()
        renderer = ImageRenderer(
            self._grid, self.distances(), gradient_start, gradient_end
        )
        renderer.render_png_file(file_name)
