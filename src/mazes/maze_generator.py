from __future__ import annotations

from collections.abc import Iterator
from enum import Enum, auto

from . import Coordinate, Grid
from .algorithms import Algorithm, BinaryTree, RecursiveBacktracker, Sidewinder


class MazeGenerator:
    class AlgorithmType(Enum):
        BinaryTree = auto()
        Sidewinder = auto()
        RecursiveBacktracker = auto()

    def __init__(
        self,
        width: int,
        height: int,
        start: Coordinate,
        algorithmType: MazeGenerator.AlgorithmType,
    ) -> None:
        self._grid = Grid(width, height)
        self._start = start
        self._algorithmType = algorithmType
        self._algorithm = self._make_algorithm(algorithmType)

    def _make_algorithm(self, mazeType: MazeGenerator.AlgorithmType) -> Algorithm:
        grid = self._grid
        match mazeType:
            case MazeGenerator.AlgorithmType.BinaryTree:
                return BinaryTree(grid)
            case MazeGenerator.AlgorithmType.Sidewinder:
                return Sidewinder(grid)
            case MazeGenerator.AlgorithmType.RecursiveBacktracker:
                return RecursiveBacktracker(grid)
            case unknown:
                raise ValueError(unknown)

    @property
    def grid(self) -> Grid:
        return self._grid

    def __iter__(self) -> Iterator[None]:
        return self._algorithm.steps()

    def steps(self) -> Iterator[None]:
        return self._algorithm.steps()
