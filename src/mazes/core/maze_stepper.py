from collections import deque
from collections.abc import Iterator

from .maze_state import MazeOperation, MazeStep, MutableMazeState


class MazeStepper:
    def __init__(
        self, state: MutableMazeState, step_generator: Iterator[MazeStep]
    ) -> None:
        self._state = state
        self._backward_steps: deque[MazeStep] = deque()
        self._forward_steps: deque[MazeStep] = deque()
        self._step_generator = step_generator
        self._generator_done = False

    def step_forward_until_end(self) -> None:
        while True:
            did_step = self.step_forward()
            if not did_step:
                break

    def step_backward_until_end(self) -> None:
        while True:
            did_step = self.step_backward()
            if not did_step:
                break

    def step_forward(self) -> bool:
        """
        Go forward one step. Returns `False` if it was unable to step,
        meaning it was at the end.
        """
        if self._forward_steps:
            return self._step_forward_from_saved_steps()
        else:
            return self._step_forward_from_generator()

    def _step_forward_from_saved_steps(self) -> bool:
        step = self._forward_steps.popleft()
        self._apply_all_operations(step.forward_operations)
        self._backward_steps.append(step)
        return True

    def _step_forward_from_generator(self) -> bool:
        try:
            step = next(self._step_generator)
            self._backward_steps.append(step)
            return True
        except StopIteration:
            return False

    def step_backward(self) -> bool:
        if not self._backward_steps:
            return False

        step = self._backward_steps.pop()
        self._apply_all_operations(step.backward_operations)
        self._forward_steps.appendleft(step)
        return True

    def _apply_all_operations(self, operations: list[MazeOperation]) -> None:
        for op in operations:
            self._state.apply_operation(op)
