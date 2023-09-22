from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum, auto

from . import Coordinate, Grid, ImmutableGrid
from .core.maze_state import MazeOperation, MazeState, MutableMazeState
from .core.maze_stepper import MazeStepper


class AlgorithmType(Enum):
    BinaryTree = auto()
    Sidewinder = auto()
    RecursiveBacktracker = auto()


@dataclass(slots=True)
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
    from .algorithms import Algorithm

    def __init__(self, options: MazeOptions) -> None:
        self._width = options.width
        self._height = options.height
        self._grid = Grid(options.width, options.height)
        self._start = options.start
        self._end = options.end
        self._maze_state = MutableMazeState(self._grid, self._start)
        self._algorithmType = options.algorithmType
        self._algorithm = self._init_algorithm(options.algorithmType)
        self._seed = self._init_seed(options.seed)

    def _init_algorithm(self, mazeType: AlgorithmType) -> Algorithm:
        from .algorithms import BinaryTree, RecursiveBacktracker, Sidewinder

        state = self._maze_state
        match mazeType:
            case AlgorithmType.BinaryTree:
                return BinaryTree(state)
            case AlgorithmType.Sidewinder:
                return Sidewinder(state)
            case AlgorithmType.RecursiveBacktracker:
                return RecursiveBacktracker(state)
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

    @property
    def targets(self) -> MazeState:
        return self._maze_state

    def make_stepper(self) -> MazeStepper:
        return MazeStepper(self._maze_state, self._algorithm.maze_steps())

    def apply_operation(self, operation: MazeOperation) -> None:
        self._maze_state.apply_operation(operation)
