from collections.abc import Iterator

from .maze_state import MazeOperation, MazeOpStep, MutableMazeState


class MazeStepper:
    def __init__(
        self, state: MutableMazeState, operations: Iterator[MazeOperation]
    ) -> None:
        self._state = state
        self._operations = operations

    def step_forward(self) -> None:
        while self._step_operation():
            pass

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
