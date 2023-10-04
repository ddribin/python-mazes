import pytest

from mazes import Direction as D
from mazes import Grid
from mazes.core.maze_state import (
    MazeOperations,
    MazeOpGridLink,
    MazeOpGridUnlink,
    MazeOpPopRun,
    MazeOpPushRun,
    MazeOpSetDistance,
    MazeOpSetMaxDistance,
    MazeOpSetRun,
    MazeOpSetTargetCoords,
    MazeOpSetTargetDirs,
    MutableMazeState,
)


class TestMazeState:
    def test_initial_state(self) -> None:
        state = self.make_state()

        assert state.run == []
        assert state.target_coordinates == []
        assert state.grid[(0, 0)] == D.Empty
        assert state.grid[(1, 1)] == D.Empty
        assert state.grid[(0, 1)] == D.Empty

        assert state.distances[(0, 0)] is None
        assert state.distances[(0, 1)] is None
        assert state.distances[(1, 0)] is None
        assert state.max_distance is None
        assert state.max_coordinate is None

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

    def test_set_distance_op(self) -> None:
        state = self.make_state()

        _ = state.apply_operation(MazeOpSetDistance((0, 0), 0))

        assert state.distances[(0, 0)] == 0
        assert state.distances[(0, 1)] is None

    def test_clear_distance_op(self) -> None:
        state = self.make_state()

        _ = state.apply_operation(MazeOpSetDistance((0, 0), 0))
        _ = state.apply_operation(MazeOpSetDistance((0, 0), None))

        assert state.distances[(0, 0)] is None
        assert state.distances[(0, 1)] is None

    def test_set_distance_op_undo(self) -> None:
        state = self.make_state()

        op = state.apply_operation(MazeOpSetDistance((0, 0), 0))
        state.apply_operation(op)

        assert state.distances[(0, 0)] is None
        assert state.distances[(0, 1)] is None

    def test_clear_distance_op_undo(self) -> None:
        state = self.make_state()

        _ = state.apply_operation(MazeOpSetDistance((0, 0), 0))
        op = state.apply_operation(MazeOpSetDistance((0, 0), None))
        state.apply_operation(op)

        assert state.distances[(0, 0)] == 0
        assert state.distances[(0, 1)] is None

    def test_set_max_distance_op(self) -> None:
        state = self.make_state()

        _ = state.apply_operation(MazeOpSetMaxDistance((1, 1), 5))

        assert state.max_distance == 5
        assert state.max_coordinate == (1, 1)

    def test_set_max_distance_op_undo(self) -> None:
        state = self.make_state()

        op = state.apply_operation(MazeOpSetMaxDistance((1, 1), 5))
        state.apply_operation(op)

        assert state.max_distance is None
        assert state.max_coordinate is None

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

    # Mutations

    def test_push_run(self) -> None:
        state = self.make_state()

        state.push_run((1, 1))

        step = state.pop_maze_step()
        assert state.run == [(1, 1)]
        assert step.forward_operations == [MazeOpPushRun((1, 1))]
        assert step.backward_operations == [MazeOpPopRun()]

    def test_pop_run(self) -> None:
        state = self.make_state()
        state.push_run((1, 1))
        state.pop_maze_step()

        state.pop_run()

        step = state.pop_maze_step()
        assert state.run == []
        assert step.forward_operations == [MazeOpPopRun()]
        assert step.backward_operations == [MazeOpPushRun((1, 1))]

    def test_pop_run_underflow(self) -> None:
        state = self.make_state()
        state.push_run((1, 1))
        state.pop_run()

        with pytest.raises(IndexError) as _:
            state.pop_run()

    def test_set_run(self) -> None:
        state = self.make_state()
        state.push_run((1, 1))
        state.push_run((2, 2))
        state.pop_maze_step()

        state.set_run([(3, 3), (4, 4)])

        step = state.pop_maze_step()
        assert state.run == [(3, 3), (4, 4)]
        assert step.forward_operations == [MazeOpSetRun([(3, 3), (4, 4)])]
        assert step.backward_operations == [MazeOpSetRun([(1, 1), (2, 2)])]

    def test_grid_link(self) -> None:
        state = self.make_state()

        state.grid_link((0, 0), D.S)

        step = state.pop_maze_step()
        assert state.grid[(0, 0)] == D.S
        assert state.grid[(0, 1)] == D.N
        assert step.forward_operations == [MazeOpGridLink((0, 0), D.S)]
        assert step.backward_operations == [MazeOpGridUnlink((0, 0), D.S)]

    def test_grid_unlink(self) -> None:
        state = self.make_state()
        state.grid_link((0, 0), D.S)
        state.pop_maze_step()

        state.grid_unlink((0, 0), D.S)

        step = state.pop_maze_step()
        assert state.grid[(0, 0)] == D.Empty
        assert state.grid[(0, 1)] == D.Empty
        assert step.forward_operations == [MazeOpGridUnlink((0, 0), D.S)]
        assert step.backward_operations == [MazeOpGridLink((0, 0), D.S)]

    def test_set_target_coords(self) -> None:
        state = self.make_state()

        state.set_target_coordinates([(1, 1), (2, 2)])

        step = state.pop_maze_step()
        assert state.target_coordinates == [(1, 1), (2, 2)]
        assert step.forward_operations == [MazeOpSetTargetCoords([(1, 1), (2, 2)])]
        assert step.backward_operations == [MazeOpSetTargetCoords([])]

    def test_pop_empty_step(self) -> None:
        state = self.make_state()

        state.push_run((1, 1))
        state.pop_maze_step()

        step = state.pop_maze_step()
        assert step.forward_operations == []
        assert step.backward_operations == []

    def test_set_distances(self) -> None:
        state = self.make_state()

        state.set_distances((0, 0), 0)

        step = state.pop_maze_step()
        assert state.distances[(0, 0)] == 0
        assert state.distances[(0, 1)] is None
        assert step.forward_operations == [
            MazeOpSetDistance((0, 0), 0),
            MazeOpSetMaxDistance((0, 0), 0),
        ]
        assert step.backward_operations == [
            MazeOpSetMaxDistance(None, None),
            MazeOpSetDistance((0, 0), None),
        ]

    def test_multiple_mutations(self) -> None:
        state = self.make_state()

        state.set_target_coordinates([(1, 0), (0, 1)])
        state.push_run((1, 0))
        state.grid_link((0, 0), D.S)
        state.set_target_coordinates([(2, 0), (1, 1)])

        step = state.pop_maze_step()
        assert state.target_coordinates == [(2, 0), (1, 1)]
        assert state.run == [(1, 0)]
        assert state.grid[(0, 0)] == D.S
        assert state.grid[(0, 1)] == D.N
        assert step.forward_operations == [
            MazeOpSetTargetCoords([(1, 0), (0, 1)]),
            MazeOpPushRun((1, 0)),
            MazeOpGridLink((0, 0), D.S),
            MazeOpSetTargetCoords([(2, 0), (1, 1)]),
        ]
        assert step.backward_operations == [
            MazeOpSetTargetCoords([(1, 0), (0, 1)]),
            MazeOpGridUnlink((0, 0), D.S),
            MazeOpPopRun(),
            MazeOpSetTargetCoords([]),
        ]

    def make_state(self) -> MutableMazeState:
        grid = Grid(5, 5)
        state = MutableMazeState(grid, (0, 0))
        return state
