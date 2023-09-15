from __future__ import annotations

import random
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import assert_never

from . import Coordinate, Direction, Distances, Grid, ImmutableDistances, ImmutableGrid
from .algorithms import Algorithm


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


@dataclass(frozen=True)
class MazeOpPushStack:
    val: Coordinate


@dataclass(frozen=True)
class MazeOpPopStack:
    pass


@dataclass(frozen=True)
class MazeOpLink:
    coodinate: Coordinate
    dirction: Direction


MazeOperation = MazeOpPushStack | MazeOpPopStack | MazeOpLink

MazeOperations = list[MazeOperation]


class MazeState:
    def __init__(self, grid: Grid, start: Coordinate) -> None:
        width = grid.width
        height = grid.height

        self._grid = grid
        self._start = start
        self._distances = Distances(width, height, start)
        self._path = Distances(width, height, start)
        self._stack: list[Coordinate] = []

    @property
    def grid(self) -> ImmutableGrid:
        return self._grid

    @property
    def start(self) -> Coordinate:
        return self._start

    @property
    def distances(self) -> ImmutableDistances:
        return self._distances

    @property
    def path(self) -> ImmutableDistances:
        return self._path

    @property
    def stack(self) -> Sequence[Coordinate]:
        return self._stack


class MutableMazeState(MazeState):
    def apply_operation(self, operation: MazeOperation) -> None:
        match operation:
            case MazeOpPushStack(val):
                self._stack.append(val)
            case MazeOpPopStack():
                self._stack.pop()
            case MazeOpLink(coord, dir):
                self._grid.link(coord, dir)
            case _:
                assert_never(operation)


class MazeGenerator:
    def __init__(self, options: MazeOptions) -> None:
        self._width = options.width
        self._height = options.height
        self._grid = Grid(options.width, options.height)
        self._start = options.start
        self._end = options.end
        self._algorithmType = options.algorithmType
        self._algorithm = self._init_algorithm(options.algorithmType)
        self._seed = self._init_seed(options.seed)
        self._maze_state = MazeState(self._grid, self._start)

    def _init_algorithm(self, mazeType: AlgorithmType) -> Algorithm:
        from .algorithms import BinaryTree, RecursiveBacktracker, Sidewinder

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

    def _init_seed(self, seed: int | None) -> int:
        if seed is None:
            seed = random.randint(0, 2**64 - 1)
        random.seed(seed)
        return seed

    @property
    def grid(self) -> ImmutableGrid:
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

    @property
    def state(self) -> MazeState:
        return self._maze_state

    def __iter__(self) -> Iterator[None]:
        return self._algorithm.steps()

    def steps(self) -> Iterator[None]:
        return self._algorithm.steps()
