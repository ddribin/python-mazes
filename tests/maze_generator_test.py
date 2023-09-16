import pytest

from mazes import AlgorithmType, Direction, Grid, MazeOptions
from mazes.maze_generator import (
    MazeOperations,
    MazeOpGridLink,
    MazeOpGridUnlink,
    MazeOpPopRun,
    MazeOpPushRun,
    MazeOpSetRun,
    MazeOpSetTargets,
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
        assert state.targets == []
        assert state.grid[(0, 0)] == Direction.Empty
        assert state.grid[(1, 1)] == Direction.Empty
        assert state.grid[(0, 1)] == Direction.Empty

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

    def test_set_targets_op(self) -> None:
        state = self.make_state()

        state.apply_operation(MazeOpSetTargets([(1, 1), (2, 2)]))
        state.apply_operation(MazeOpSetTargets([(3, 3), (4, 4)]))

        assert state.targets == [(3, 3), (4, 4)]

    def test_set_targets_op_undo(self) -> None:
        state = self.make_state()

        state.apply_operation(MazeOpSetTargets([(1, 1), (2, 2)]))
        op = state.apply_operation(MazeOpSetTargets([(3, 3), (4, 4)]))
        state.apply_operation(op)

        assert state.targets == [(1, 1), (2, 2)]

    def test_grid_link_op(self) -> None:
        state = self.make_state()

        state.apply_operation(MazeOpGridLink((0, 0), Direction.S))

        assert state.grid[(0, 0)] == Direction.S
        assert state.grid[(0, 1)] == Direction.N

    def test_grid_link_op_undo(self) -> None:
        state = self.make_state()

        op = state.apply_operation(MazeOpGridLink((0, 0), Direction.S))
        state.apply_operation(op)

        assert state.grid[(0, 0)] == Direction.Empty
        assert state.grid[(0, 1)] == Direction.Empty

    def test_grid_unlink_op(self) -> None:
        state = self.make_state()

        state.apply_operation(MazeOpGridLink((0, 0), Direction.S))
        state.apply_operation(MazeOpGridUnlink((0, 0), Direction.S))

        assert state.grid[(0, 0)] == Direction.Empty
        assert state.grid[(0, 1)] == Direction.Empty

    def test_grid_unlink_op_undo(self) -> None:
        state = self.make_state()

        state.apply_operation(MazeOpGridLink((0, 0), Direction.S))
        op = state.apply_operation(MazeOpGridUnlink((0, 0), Direction.S))
        state.apply_operation(op)

        assert state.grid[(0, 0)] == Direction.S
        assert state.grid[(0, 1)] == Direction.N

    def test_multiple_undo(self) -> None:
        state = self.make_state()

        ops = [
            MazeOpSetTargets([(1, 0), (0, 1)]),
            MazeOpPushRun((1, 0)),
            MazeOpGridLink((0, 0), Direction.E),
            MazeOpSetTargets([(2, 0), (1, 1)]),
        ]
        undo_ops: MazeOperations = []
        for op in ops:
            undo_op = state.apply_operation(op)
            undo_ops.append(undo_op)

        for op in reversed(undo_ops):
            state.apply_operation(op)

        # Should be back to initial state
        assert state.run == []
        assert state.targets == []
        assert state.grid[(0, 0)] == Direction.Empty
        assert state.grid[(1, 1)] == Direction.Empty
        assert state.grid[(0, 1)] == Direction.Empty

    def make_state(self) -> MutableMazeState:
        grid = Grid(5, 5)
        state = MutableMazeState(grid, (0, 0))
        return state
