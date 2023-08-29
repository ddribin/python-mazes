from typing_extensions import Protocol

class Algorithm(Protocol):
    def generate(self) -> None:
        """
        Generates a maze. This is a generator method that yields at each step.
        """
        ...

    def generate_all(self) -> None:
        """
        Generates all steps
        """
        for _ in self.generate():
            pass
