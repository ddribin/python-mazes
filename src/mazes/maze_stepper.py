from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass, field

from .maze_state import MazeOperation, MazeOpStep, MutableMazeState


@dataclass(frozen=True, slots=True)
class MazeStep:
    forward_operations: list[MazeOperation] = field(default_factory=list)
    backward_operations: list[MazeOperation] = field(default_factory=list)


class MazeStepper:
    def __init__(
        self, state: MutableMazeState, generator: Iterator[MazeOperation]
    ) -> None:
        self._state = state
        self._backward_steps: deque[MazeStep] = deque()
        self._forward_steps: deque[MazeStep] = deque()
        self._generator = generator
        self._generator_done = False

    def step_forward(self) -> None:
        if self._forward_steps:
            self._step_forward_from_saved_steps()
        else:
            self._step_forward_from_generator()

    def _step_forward_from_saved_steps(self) -> None:
        step = self._forward_steps.popleft()
        self._apply_all_operations(step.forward_operations)
        self._backward_steps.append(step)

    def _step_forward_from_generator(self) -> None:
        step = self._next_generator_step()
        if step is not None:
            self._backward_steps.append(step)

    def _pull_step(self) -> list[MazeOperation]:
        step: list[MazeOperation] = []
        while True:
            op = self._next_generator_operation()
            if op is not None:
                step.append(op)
            else:
                break

        return step

    def _next_generator_step(self) -> MazeStep | None:
        forward_ops: list[MazeOperation] = []
        backward_ops: list[MazeOperation] = []

        while True:
            op = self._next_generator_operation()
            if op is None:
                break
            backward_op = self._state.apply_operation(op)
            forward_ops.append(op)
            backward_ops.append(backward_op)

        if forward_ops:
            # Want to execute backward ops in reverse order
            backward_ops.reverse()
            step = MazeStep(forward_ops, backward_ops)
            return step
        else:
            return None

    def _next_generator_operation(self) -> MazeOperation | None:
        op = next(self._generator)
        match op:
            case MazeOpStep():
                return None

            case _:
                return op

    def _step_operation(self) -> bool:
        op = next(self._generator)
        match op:
            case MazeOpStep():
                return False

            case _:
                self._state.apply_operation(op)
                return True

    def step_backward(self) -> None:
        if not self._backward_steps:
            return

        step = self._backward_steps.pop()
        self._apply_all_operations(step.backward_operations)
        self._forward_steps.appendleft(step)

    def _apply_all_operations(self, operations: list[MazeOperation]) -> None:
        for op in operations:
            self._state.apply_operation(op)
