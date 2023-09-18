from mazes import Direction as D
from mazes import Grid, MazeOperation, MazeStepper, MutableMazeState
from mazes.maze_state import MazeOpGridLink, MazeOpPushRun, MazeOpStep


class TestMazeStepper:
    def test_step_forward_one(self) -> None:
        grid = Grid(4, 4)
        state = MutableMazeState(grid, (0, 0))
        ops: list[MazeOperation] = [
            MazeOpGridLink((0, 0), D.E),
            MazeOpPushRun((0, 1)),
            MazeOpStep(),
        ]
        stepper = MazeStepper(state, iter(ops))

        stepper.step_forward()

        assert grid.available_directions((0, 0)) == D.S
        assert state.run == [(0, 1)]

    def test_step_backward_one(self) -> None:
        grid = Grid(4, 4)
        state = MutableMazeState(grid, (0, 0))
        ops: list[MazeOperation] = [
            MazeOpGridLink((0, 0), D.E),
            MazeOpPushRun((0, 1)),
            MazeOpStep(),
        ]
        stepper = MazeStepper(state, iter(ops))

        stepper.step_forward()
        stepper.step_backward()

        assert grid.available_directions((0, 0)) == D.S | D.E
        assert state.run == []

    def test_step_backward_then_forward(self) -> None:
        grid = Grid(4, 4)
        state = MutableMazeState(grid, (0, 0))
        ops: list[MazeOperation] = [
            MazeOpGridLink((0, 0), D.E),
            MazeOpPushRun((0, 1)),
            MazeOpStep(),
        ]
        stepper = MazeStepper(state, iter(ops))

        stepper.step_forward()
        stepper.step_backward()
        stepper.step_forward()

        assert grid.available_directions((0, 0)) == D.S
        assert state.run == [(0, 1)]

    def test_step_forward_multiple(self) -> None:
        grid = Grid(4, 4)
        state = MutableMazeState(grid, (0, 0))
        ops: list[MazeOperation] = [
            # Step 1
            MazeOpGridLink((0, 0), D.E),
            MazeOpPushRun((0, 1)),
            MazeOpStep(),
            # Step 2
            MazeOpPushRun((0, 2)),
            MazeOpStep(),
        ]
        stepper = MazeStepper(state, iter(ops))

        stepper.step_forward()
        assert grid.available_directions((0, 0)) == D.S
        assert state.run == [(0, 1)]

        stepper.step_forward()
        assert state.run == [(0, 1), (0, 2)]

        assert not stepper.step_forward()

    def test_step_forward_multiple_then_backward(self) -> None:
        grid = Grid(4, 4)
        state = MutableMazeState(grid, (0, 0))
        ops: list[MazeOperation] = [
            # Step 1
            MazeOpGridLink((0, 0), D.E),
            MazeOpPushRun((0, 1)),
            MazeOpStep(),
            # Step 2
            MazeOpPushRun((0, 2)),
            MazeOpStep(),
        ]
        stepper = MazeStepper(state, iter(ops))

        stepper.step_forward()
        stepper.step_forward()

        assert grid.available_directions((0, 0)) == D.S
        assert state.run == [(0, 1), (0, 2)]

        stepper.step_backward()
        assert grid.available_directions((0, 0)) == D.S
        assert state.run == [(0, 1)]

        stepper.step_backward()
        assert grid.available_directions((0, 0)) == D.S | D.E
        assert state.run == []

    def test_step_forward_then_backward_then_forward(self) -> None:
        grid = Grid(4, 4)
        state = MutableMazeState(grid, (0, 0))
        ops: list[MazeOperation] = [
            # Step 1
            MazeOpGridLink((0, 0), D.E),
            MazeOpPushRun((0, 1)),
            MazeOpStep(),
            # Step 2
            MazeOpPushRun((0, 2)),
            MazeOpStep(),
            # Step 3
            MazeOpPushRun((1, 2)),
            MazeOpStep(),
        ]
        stepper = MazeStepper(state, iter(ops))

        stepper.step_forward()
        stepper.step_forward()
        stepper.step_backward()
        stepper.step_backward()
        stepper.step_forward()
        stepper.step_forward()
        stepper.step_forward()

        assert grid.available_directions((0, 0)) == D.S
        assert state.run == [(0, 1), (0, 2), (1, 2)]

    def test_step_forward_until_end(self) -> None:
        grid = Grid(4, 4)
        state = MutableMazeState(grid, (0, 0))
        ops: list[MazeOperation] = [
            # Step 1
            MazeOpGridLink((0, 0), D.E),
            MazeOpPushRun((0, 1)),
            MazeOpStep(),
            # Step 2
            MazeOpPushRun((0, 2)),
            MazeOpStep(),
            # Step 3
            MazeOpPushRun((1, 2)),
            MazeOpStep(),
        ]
        stepper = MazeStepper(state, iter(ops))

        stepper.step_forward_until_end()

        assert grid.available_directions((0, 0)) == D.S
        assert state.run == [(0, 1), (0, 2), (1, 2)]

    def test_step_backward_until_end(self) -> None:
        grid = Grid(4, 4)
        state = MutableMazeState(grid, (0, 0))
        ops: list[MazeOperation] = [
            # Step 1
            MazeOpGridLink((0, 0), D.E),
            MazeOpPushRun((0, 1)),
            MazeOpStep(),
            # Step 2
            MazeOpPushRun((0, 2)),
            MazeOpStep(),
            # Step 3
            MazeOpPushRun((1, 2)),
            MazeOpStep(),
        ]
        stepper = MazeStepper(state, iter(ops))

        stepper.step_forward_until_end()
        stepper.step_backward_until_end()

        assert grid.available_directions((0, 0)) == D.S | D.E
        assert state.run == []
