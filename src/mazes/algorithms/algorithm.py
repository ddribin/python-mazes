from collections.abc import Iterator

from typing_extensions import Protocol


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
