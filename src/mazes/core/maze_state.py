from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import assert_never

from ..distances import Distances, ImmutableDistances
from ..grid import Coordinate, Direction, Grid, ImmutableGrid


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
class MazeOpSetDistance:
    coord: Coordinate
    distance: int | None


MazeOperation = (
    MazeOpPushRun
    | MazeOpPopRun
    | MazeOpGridLink
    | MazeOpGridUnlink
    | MazeOpSetRun
    | MazeOpSetTargetCoords
    | MazeOpSetTargetDirs
    | MazeOpSetDistance
)


MazeOperations = list[MazeOperation]


@dataclass(frozen=True, slots=True)
class MazeStep:
    forward_operations: list[MazeOperation] = field(default_factory=list)
    backward_operations: list[MazeOperation] = field(default_factory=list)


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

        self._forward_operations: list[MazeOperation] = []
        self._backward_operations: list[MazeOperation] = []
        self._records_operations = True

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
    def pop_maze_step(self) -> MazeStep:
        forward_ops = self._forward_operations
        backward_ops = self._backward_operations
        backward_ops.reverse()

        self._forward_operations = []
        self._backward_operations = []

        step = MazeStep(forward_ops, backward_ops)
        return step

    def push_run(self, coordinate: Coordinate) -> None:
        op = MazeOpPushRun(coordinate)
        self._execute_operation(op)

    def pop_run(self) -> None:
        op = MazeOpPopRun()
        self._execute_operation(op)

    def set_run(self, run: list[Coordinate]) -> None:
        op = MazeOpSetRun(run)
        self._execute_operation(op)

    def grid_link(self, coordinate: Coordinate, direction: Direction) -> None:
        op = MazeOpGridLink(coordinate, direction)
        self._execute_operation(op)

    def grid_unlink(self, coordinate: Coordinate, direction: Direction) -> None:
        op = MazeOpGridUnlink(coordinate, direction)
        self._execute_operation(op)

    def set_target_coordinates(self, coordinates: list[Coordinate]) -> None:
        op = MazeOpSetTargetCoords(coordinates)
        self._execute_operation(op)

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

            case MazeOpSetDistance(coord, val):
                prev_distance = self._distances[coord]
                if val is not None:
                    self._distances[coord] = val
                else:
                    self._distances.clear_at(coord)
                return MazeOpSetDistance(coord, prev_distance)

            case _:
                assert_never(operation)

    def reset_dijstra_distances(self, start: Coordinate) -> None:
        ...

    @property
    def dijkstra_distances(self) -> Distances:
        ...

    def _execute_operation(self, op: MazeOperation) -> None:
        backward_op = self.apply_operation(op)
        if self._records_operations:
            self._forward_operations.append(op)
            self._backward_operations.append(backward_op)
