from typing_extensions import Protocol
from collections.abc import Iterator


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
