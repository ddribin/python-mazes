from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import assert_never

from . import Coordinate, Direction, Distances, Grid, ImmutableDistances, ImmutableGrid


@dataclass(frozen=True, slots=True)
class MazeOpPushRun:
    val: Coordinate


@dataclass(frozen=True, slots=True)
class MazeOpPopRun:
    pass


@dataclass(frozen=True, slots=True)
class MazeOpSetRun:
    val: list[Coordinate] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class MazeOpGridLink:
    coordinate: Coordinate
    direction: Direction


@dataclass(frozen=True, slots=True)
class MazeOpGridUnlink:
    coordinate: Coordinate
    direction: Direction


@dataclass(frozen=True, slots=True)
class MazeOpSetTargetCoords:
    val: list[Coordinate] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class MazeOpSetTargetDirs:
    directions: Direction


@dataclass(frozen=True, slots=True)
class MazeOpStep:
    pass


MazeOperation = (
    MazeOpPushRun
    | MazeOpPopRun
    | MazeOpGridLink
    | MazeOpGridUnlink
    | MazeOpSetRun
    | MazeOpSetTargetCoords
    | MazeOpSetTargetDirs
    | MazeOpStep
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
        self._target_coordinates: list[Coordinate] = []
        self._target_directions = Direction.Empty

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
    def target_coordinates(self) -> Sequence[Coordinate]:
        return self._target_coordinates

    @property
    def target_directions(self) -> Direction:
        return self._target_directions


class MutableMazeState(MazeState):
    def apply_operation(self, operation: MazeOperation) -> MazeOperation:
        match operation:
            case MazeOpPushRun(val):
                self._run.append(val)
                return MazeOpPopRun()

            case MazeOpPopRun():
                old_head = self._run[-1]
                self._run.pop()
                return MazeOpPushRun(old_head)

            case MazeOpSetRun(val):
                prev_run = self._run
                self._run = val
                return MazeOpSetRun(prev_run)

            case MazeOpGridLink(coord, dir):
                self._grid.link(coord, dir)
                return MazeOpGridUnlink(coord, dir)

            case MazeOpGridUnlink(coord, dir):
                self._grid.unlink(coord, dir)
                return MazeOpGridLink(coord, dir)

            case MazeOpSetTargetCoords(val):
                prev_targets = self._target_coordinates
                self._target_coordinates = val
                return MazeOpSetTargetCoords(prev_targets)

            case MazeOpSetTargetDirs(dirs):
                prev_dirs = self._target_directions
                self._target_directions = dirs
                return MazeOpSetTargetDirs(prev_dirs)

            case MazeOpStep():
                return operation

            case _:
                assert_never(operation)
