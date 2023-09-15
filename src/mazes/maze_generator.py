from __future__ import annotations

import random
from collections.abc import Iterator
from dataclasses import dataclass, field
from enum import Enum, auto

from . import Coordinate, Grid
from .algorithms import Algorithm, BinaryTree, RecursiveBacktracker, Sidewinder


class AlgorithmType(Enum):
    BinaryTree = auto()
    Sidewinder = auto()
    RecursiveBacktracker = auto()


@dataclass
class MazeOptions:
    width: int
    height: int
    algorithmType: AlgorithmType = AlgorithmType.RecursiveBacktracker
    start: Coordinate = field(init=False)
    end: Coordinate = field(init=False)
    seed: int | None = None

    def __post_init__(self):
        self.start = self.northwest_corner
        self.end = self.southeast_corner

    @property
    def northwest_corner(self) -> Coordinate:
        return (0, 0)

    @property
    def northeast_corner(self) -> Coordinate:
        return (self.width - 1, 0)

    @property
    def southwest_corner(self) -> Coordinate:
        return (0, self.height - 1)

    @property
    def southeast_corner(self) -> Coordinate:
        return (self.width - 1, self.height - 1)


class MazeGenerator:
    def __init__(self, options: MazeOptions) -> None:
        self._grid = Grid(options.width, options.height)
        self._start = options.start
        self._end = options.end
        self._algorithmType = options.algorithmType
        self._algorithm = self._make_algorithm(options.algorithmType)
        if options.seed is None:
            seed = random.randint(0, 2**64 - 1)
        else:
            seed = options.seed
        random.seed(seed)
        self._seed = seed

    def _make_algorithm(self, mazeType: AlgorithmType) -> Algorithm:
        grid = self._grid
        match mazeType:
            case AlgorithmType.BinaryTree:
                return BinaryTree(grid)
            case AlgorithmType.Sidewinder:
                return Sidewinder(grid)
            case AlgorithmType.RecursiveBacktracker:
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
    def end(self) -> Coordinate:
        return self._end

    @property
    def seed(self) -> int:
        return self._seed

    def __iter__(self) -> Iterator[None]:
        return self._algorithm.steps()

    def steps(self) -> Iterator[None]:
        return self._algorithm.steps()
