from collections.abc import Iterator

from mazes import Direction as D
from mazes import Grid, MazeStep, MazeStepper, MutableMazeState


class TestMazeStepper:
    def test_initial_state(self) -> None:
        grid = Grid(4, 4)
        state = MutableMazeState(grid, (0, 0))

        def steps() -> Iterator[MazeStep]:
            state.grid_link((0, 0), D.E)
            state.push_run((0, 1))
            yield state.pop_maze_step()

        _ = MazeStepper(state, iter([]), steps())

        assert grid.available_directions((0, 0)) == D.S | D.E
        assert state.run == []

    def test_step_forward_one(self) -> None:
        grid = Grid(4, 4)
        state = MutableMazeState(grid, (0, 0))

        def steps() -> Iterator[MazeStep]:
            state.grid_link((0, 0), D.E)
            state.push_run((0, 1))
            yield state.pop_maze_step()

        stepper = MazeStepper(state, iter([]), steps())

        stepper.step_forward()

        assert grid.available_directions((0, 0)) == D.S
        assert state.run == [(0, 1)]

    def test_step_backward_one(self) -> None:
        grid = Grid(4, 4)
        state = MutableMazeState(grid, (0, 0))

        def steps() -> Iterator[MazeStep]:
            state.grid_link((0, 0), D.E)
            state.push_run((0, 1))
            yield state.pop_maze_step()

        stepper = MazeStepper(state, iter([]), steps())

        stepper.step_forward()
        stepper.step_backward()

        assert grid.available_directions((0, 0)) == D.S | D.E
        assert state.run == []

    def test_step_backward_then_forward(self) -> None:
        grid = Grid(4, 4)
        state = MutableMazeState(grid, (0, 0))

        def steps() -> Iterator[MazeStep]:
            state.grid_link((0, 0), D.E)
            state.push_run((0, 1))
            yield state.pop_maze_step()

        stepper = MazeStepper(state, iter([]), steps())

        stepper.step_forward()
        stepper.step_backward()
        stepper.step_forward()

        assert grid.available_directions((0, 0)) == D.S
        assert state.run == [(0, 1)]

    def test_step_forward_multiple(self) -> None:
        grid = Grid(4, 4)
        state = MutableMazeState(grid, (0, 0))

        def steps() -> Iterator[MazeStep]:
            # Step 1
            state.grid_link((0, 0), D.E)
            state.push_run((0, 1))
            yield state.pop_maze_step()
            # Step 2
            state.push_run((0, 2))
            yield state.pop_maze_step()

        stepper = MazeStepper(state, iter([]), steps())

        stepper.step_forward()
        assert grid.available_directions((0, 0)) == D.S
        assert state.run == [(0, 1)]

        stepper.step_forward()
        assert state.run == [(0, 1), (0, 2)]

        assert not stepper.step_forward()

    def test_step_forward_multiple_then_backward(self) -> None:
        grid = Grid(4, 4)
        state = MutableMazeState(grid, (0, 0))

        def steps() -> Iterator[MazeStep]:
            # Step 1
            state.grid_link((0, 0), D.E)
            state.push_run((0, 1))
            yield state.pop_maze_step()
            # Step 2
            state.push_run((0, 2))
            yield state.pop_maze_step()

        stepper = MazeStepper(state, iter([]), steps())

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

        def steps() -> Iterator[MazeStep]:
            # Step 1
            state.grid_link((0, 0), D.E)
            state.push_run((0, 1))
            yield state.pop_maze_step()
            # Step 2
            state.push_run((0, 2))
            yield state.pop_maze_step()
            # Step 3
            state.push_run((1, 2))
            yield state.pop_maze_step()

        stepper = MazeStepper(state, iter([]), steps())

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

        def steps() -> Iterator[MazeStep]:
            # Step 1
            state.grid_link((0, 0), D.E)
            state.push_run((0, 1))
            yield state.pop_maze_step()
            # Step 2
            state.push_run((0, 2))
            yield state.pop_maze_step()
            # Step 3
            state.push_run((1, 2))
            yield state.pop_maze_step()

        stepper = MazeStepper(state, iter([]), steps())

        stepper.step_forward_until_end()

        assert grid.available_directions((0, 0)) == D.S
        assert state.run == [(0, 1), (0, 2), (1, 2)]

    def test_step_backward_until_end(self) -> None:
        grid = Grid(4, 4)
        state = MutableMazeState(grid, (0, 0))

        def steps() -> Iterator[MazeStep]:
            # Step 1
            state.grid_link((0, 0), D.E)
            state.push_run((0, 1))
            yield state.pop_maze_step()
            # Step 2
            state.push_run((0, 2))
            yield state.pop_maze_step()
            # Step 3
            state.push_run((1, 2))
            yield state.pop_maze_step()

        stepper = MazeStepper(state, iter([]), steps())

        stepper.step_forward_until_end()
        stepper.step_backward_until_end()

        assert grid.available_directions((0, 0)) == D.S | D.E
        assert state.run == []
