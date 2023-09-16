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
class MazeOpPushRun:
    val: Coordinate


@dataclass(frozen=True)
class MazeOpPopRun:
    pass


@dataclass(frozen=True)
class MazeOpSetRun:
    val: list[Coordinate] = field(default_factory=list)


@dataclass(frozen=True)
class MazeOpGridLink:
    coordinate: Coordinate
    direction: Direction


@dataclass(frozen=True)
class MazeOpGridUnlink:
    coordinate: Coordinate
    direction: Direction


@dataclass(frozen=True)
class MazeOpSetTargets:
    val: list[Coordinate] = field(default_factory=list)


MazeOperation = (
    MazeOpPushRun
    | MazeOpPopRun
    | MazeOpGridLink
    | MazeOpGridUnlink
    | MazeOpSetRun
    | MazeOpSetTargets
)

MazeOperations = list[MazeOperation]


class MazeState:
    def __init__(self, grid: Grid, start: Coordinate) -> None:
        width = grid.width
        height = grid.height

        self._grid = grid
        self._start = start
        self._distances = Distances(width, height, start)
        self._path = Distances(width, height, start)
        self._run: list[Coordinate] = []
        self._targets: list[Coordinate] = []

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
    def run(self) -> Sequence[Coordinate]:
        return self._run

    @property
    def targets(self) -> Sequence[Coordinate]:
        return self._targets


class MutableMazeState(MazeState):
    def apply_operation(self, operation: MazeOperation) -> MazeOperation:
        match operation:
            case MazeOpPushRun(val):
                self._run.append(val)
                return MazeOpPopRun()

            case MazeOpPopRun():
                head = self._run[-1]
                self._run.pop()
                return MazeOpPushRun(head)

            case MazeOpSetRun(val):
                run = self._run
                self._run = val
                return MazeOpSetRun(run)

            case MazeOpGridLink(coord, dir):
                self._grid.link(coord, dir)
                return MazeOpGridUnlink(coord, dir)

            case MazeOpGridUnlink(coord, dir):
                self._grid.unlink(coord, dir)
                return MazeOpGridLink(coord, dir)

            case MazeOpSetTargets(val):
                targets = self._targets
                self._targets = val
                return MazeOpSetTargets(targets)

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
