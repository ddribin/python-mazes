from __future__ import annotations

from enum import Enum, auto

from .algorithms import Algorithm, BinaryTree
from .distances import Distances
from .grid import Grid, ImmutableGrid, Coordinate
from .renderers import TextRenderer, ImageRenderer


from typing import TypeVar, Sequence

T = TypeVar("T")


def unwrap(x: T | None) -> T:
    assert x is not None
    return x


class Maze:
    class AlgorithmType(Enum):
        BinaryTree = auto()

    class OverlayType(Enum):
        Nothing = auto()
        Distance = auto()
        PathTo = auto()
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

        distances = Maze.make_distances(overlayType, grid)

        return Maze(grid, distances)

    @classmethod
    def make_algorithm(cls, mazeType: Maze.AlgorithmType, grid: Grid) -> Algorithm:
        match mazeType:
            case Maze.AlgorithmType.BinaryTree:
                return BinaryTree(grid)

            case _:
                return BinaryTree(grid)

    @classmethod
    def make_distances(
        cls, overlayType: Maze.OverlayType, grid: ImmutableGrid
    ) -> Distances | None:
        match overlayType:
            case Maze.OverlayType.Distance:
                return Maze.make_distance_distances(grid)
            case Maze.OverlayType.PathTo:
                return Maze.make_path_to_distances(grid)
            case Maze.OverlayType.LongestPath:
                return Maze.make_longest_path_distances(grid)
            case _:
                return None

    @classmethod
    def make_distance_distances(cls, grid: ImmutableGrid) -> Distances:
        middle = (int(grid.width / 2), int(grid.height / 2))
        distances = Distances.from_root(grid, middle)
        return distances

    @classmethod
    def make_path_to_distances(cls, grid: ImmutableGrid) -> Distances:
        start = grid.northwest_corner
        goal = grid.southwest_corner
        distances = Distances.from_root(grid, start)
        return Maze.path_to(grid, start, goal, distances)

    @classmethod
    def path_to(
        cls,
        grid: ImmutableGrid,
        start: Coordinate,
        goal: Coordinate,
        distances: Distances,
    ) -> Distances:
        current = goal

        breadcrumbs = Distances(grid.width, grid.height, start)
        breadcrumbs[current] = unwrap(distances[current])

        while current != start:
            links = unwrap(grid[current])
            current_distance = unwrap(distances[current])
            # print(f"{current=}: {current_distance=} {links=}")

            for dir in links:
                neighbor = dir.update_coordinate(current)
                neighbor_distance = unwrap(distances[neighbor])
                # print(f"  {dir=} {neighbor=}: {neighbor_distance=}")
                if neighbor_distance < current_distance:
                    breadcrumbs[neighbor] = neighbor_distance
                    current = neighbor
                    break

        return breadcrumbs

    @classmethod
    def make_longest_path_distances(cls, grid: ImmutableGrid) -> Distances:
        start = grid.northeast_corner
        distances = Distances.from_root(grid, start)
        new_start, distance = distances.max

        new_distances = Distances.from_root(grid, new_start)
        goal, _ = new_distances.max
        path = Maze.path_to(grid, new_start, goal, new_distances)
        return path

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
