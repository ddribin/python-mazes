from __future__ import annotations

import random
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
        seed: int | None = None,
    ) -> None:
        self._grid = Grid(width, height)
        self._start = start
        self._algorithmType = algorithmType
        self._algorithm = self._make_algorithm(algorithmType)
        if seed is None:
            seed = random.randint(0, 2**64 - 1)
        random.seed(seed)
        self._seed = seed

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

    @property
    def start(self) -> Coordinate:
        return self._start

    @property
    def seed(self) -> int:
        return self._seed

    def __iter__(self) -> Iterator[None]:
        return self._algorithm.steps()

    def steps(self) -> Iterator[None]:
        return self._algorithm.steps()
