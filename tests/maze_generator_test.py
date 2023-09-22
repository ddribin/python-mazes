import pytest

from mazes import AlgorithmType
from mazes import Direction as D
from mazes import Grid, MazeOptions
from mazes.core.maze_state import (
    MazeOperations,
    MazeOpGridLink,
    MazeOpGridUnlink,
    MazeOpPopRun,
    MazeOpPushRun,
    MazeOpSetRun,
    MazeOpSetTargetCoords,
    MazeOpSetTargetDirs,
    MutableMazeState,
)


class TestMazeGenerator:
    def test_maze_options_default_values(self) -> None:
        options = MazeOptions(2, 3)

        assert options.width == 2
        assert options.height == 3
        assert options.algorithmType == AlgorithmType.RecursiveBacktracker
        assert options.start == (0, 0)
        assert options.end == (1, 2)
        assert options.seed is None

    def test_initial_state(self) -> None:
        state = self.make_state()

        assert state.run == []
        assert state.target_coordinates == []
        assert state.grid[(0, 0)] == D.Empty
        assert state.grid[(1, 1)] == D.Empty
        assert state.grid[(0, 1)] == D.Empty

    def test_push_run_op(self) -> None:
        state = self.make_state()

        state.apply_operation(MazeOpPushRun((1, 1)))
        state.apply_operation(MazeOpPushRun((2, 2)))

        assert state.run == [(1, 1), (2, 2)]

    def test_push_run_op_undo(self) -> None:
        state = self.make_state()

        op = state.apply_operation(MazeOpPushRun((1, 1)))
        state.apply_operation(op)

        assert state.run == []

    def test_pop_run_op(self) -> None:
        state = self.make_state()

        state.apply_operation(MazeOpPushRun((1, 1)))
        state.apply_operation(MazeOpPushRun((2, 2)))
        state.apply_operation(MazeOpPopRun())

        assert state.run == [(1, 1)]

    def test_pop_run_op_undo(self) -> None:
        state = self.make_state()

        state.apply_operation(MazeOpPushRun((1, 1)))
        state.apply_operation(MazeOpPushRun((2, 2)))
        op = state.apply_operation(MazeOpPopRun())
        state.apply_operation(op)

        assert state.run == [(1, 1), (2, 2)]

    def test_pop_run_op_underflow(self) -> None:
        state = self.make_state()

        with pytest.raises(IndexError) as _:
            state.apply_operation(MazeOpPushRun((1, 1)))
            state.apply_operation(MazeOpPopRun())
            state.apply_operation(MazeOpPopRun())

    def test_set_run_op(self) -> None:
        state = self.make_state()

        state.apply_operation(MazeOpPushRun((1, 1)))
        state.apply_operation(MazeOpPushRun((2, 2)))
        state.apply_operation(MazeOpSetRun([(3, 3), (4, 4)]))

        assert state.run == [(3, 3), (4, 4)]

    def test_set_run_op_undo(self) -> None:
        state = self.make_state()

        state.apply_operation(MazeOpPushRun((1, 1)))
        state.apply_operation(MazeOpPushRun((2, 2)))
        op = state.apply_operation(MazeOpSetRun([(3, 3), (4, 4)]))
        state.apply_operation(op)

        assert state.run == [(1, 1), (2, 2)]

    def test_set_target_coords_op(self) -> None:
        state = self.make_state()

        state.apply_operation(MazeOpSetTargetCoords([(1, 1), (2, 2)]))
        state.apply_operation(MazeOpSetTargetCoords([(3, 3), (4, 4)]))

        assert state.target_coordinates == [(3, 3), (4, 4)]

    def test_set_target_coords_op_undo(self) -> None:
        state = self.make_state()

        state.apply_operation(MazeOpSetTargetCoords([(1, 1), (2, 2)]))
        op = state.apply_operation(MazeOpSetTargetCoords([(3, 3), (4, 4)]))
        state.apply_operation(op)

        assert state.target_coordinates == [(1, 1), (2, 2)]

    def test_set_target_dirs_op(self) -> None:
        state = self.make_state()

        state.apply_operation(MazeOpSetTargetDirs(D.S | D.E))
        state.apply_operation(MazeOpSetTargetDirs(D.N | D.W))

        assert state.target_directions == (D.N | D.W)

    def test_set_target_dirs_op_undo(self) -> None:
        state = self.make_state()

        state.apply_operation(MazeOpSetTargetDirs(D.S | D.E))
        op = state.apply_operation(MazeOpSetTargetDirs(D.N | D.W))
        state.apply_operation(op)

        assert state.target_directions == (D.S | D.E)

    def test_grid_link_op(self) -> None:
        state = self.make_state()

        state.apply_operation(MazeOpGridLink((0, 0), D.S))

        assert state.grid[(0, 0)] == D.S
        assert state.grid[(0, 1)] == D.N

    def test_grid_link_op_undo(self) -> None:
        state = self.make_state()

        op = state.apply_operation(MazeOpGridLink((0, 0), D.S))
        state.apply_operation(op)

        assert state.grid[(0, 0)] == D.Empty
        assert state.grid[(0, 1)] == D.Empty

    def test_grid_unlink_op(self) -> None:
        state = self.make_state()

        state.apply_operation(MazeOpGridLink((0, 0), D.S))
        state.apply_operation(MazeOpGridUnlink((0, 0), D.S))

        assert state.grid[(0, 0)] == D.Empty
        assert state.grid[(0, 1)] == D.Empty

    def test_grid_unlink_op_undo(self) -> None:
        state = self.make_state()

        state.apply_operation(MazeOpGridLink((0, 0), D.S))
        op = state.apply_operation(MazeOpGridUnlink((0, 0), D.S))
        state.apply_operation(op)

        assert state.grid[(0, 0)] == D.S
        assert state.grid[(0, 1)] == D.N

    def test_multiple_undo(self) -> None:
        state = self.make_state()

        ops: MazeOperations = [
            MazeOpSetTargetCoords([(1, 0), (0, 1)]),
            MazeOpPushRun((1, 0)),
            MazeOpGridLink((0, 0), D.E),
            MazeOpSetTargetCoords([(2, 0), (1, 1)]),
        ]
        undo_ops: MazeOperations = []
        for op in ops:
            undo_op = state.apply_operation(op)
            undo_ops.append(undo_op)

        for op in reversed(undo_ops):
            state.apply_operation(op)

        # Should be back to initial state
        assert state.run == []
        assert state.target_coordinates == []
        assert state.grid[(0, 0)] == D.Empty
        assert state.grid[(1, 1)] == D.Empty
        assert state.grid[(0, 1)] == D.Empty

    def make_state(self) -> MutableMazeState:
        grid = Grid(5, 5)
        state = MutableMazeState(grid, (0, 0))
        return state
