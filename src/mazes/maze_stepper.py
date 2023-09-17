from collections.abc import Iterator

from .maze_state import MazeOperation, MazeOpStep, MutableMazeState


class MazeStepper:
    def __init__(
        self, state: MutableMazeState, operations: Iterator[MazeOperation]
    ) -> None:
        self._state = state
        self._operations = operations
        self._previous_operations: list[MazeOperation] = []
        self._previous_index = 0

    def step_forward(self) -> None:
        while self._step_operation():
            pass

    def _pull_step(self) -> list[MazeOperation]:
        step: list[MazeOperation] = []
        while True:
            op = self._next_operation()
            if op is not None:
                step.append(op)
            else:
                break

        return step

    def _next_operation(self) -> MazeOperation | None:
        op = next(self._operations)
        match op:
            case MazeOpStep():
                return None

            case _:
                return op

    def _step_operation(self) -> bool:
        op = next(self._operations)
        match op:
            case MazeOpStep():
                return False

            case _:
                self._state.apply_operation(op)
                return True

    def step_backward(self) -> bool:
        return False
