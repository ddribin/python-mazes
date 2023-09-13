from collections.abc import Iterator

from typing_extensions import Protocol

from ..grid import Coordinate


def next_step(step_iterator: Iterator[None]) -> bool:
    has_more = True
    try:
        next(step_iterator)
    except StopIteration:
        has_more = False
    return has_more


class Algorithm(Protocol):
    def steps(self) -> Iterator[None]:
        """
        Generates a maze. This is a generator method that yields at each step.
        """
        ...

    def generate(self) -> None:
        """
        Generates all steps.
        """
        for _ in self.steps():
            pass

    @property
    def current(self) -> set[Coordinate]:
        ...

    @property
    def trail(self) -> set[Coordinate]:
        ...

    @property
    def targets(self) -> set[Coordinate]:
        ...
