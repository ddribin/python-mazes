from __future__ import annotations

from .algorithms import Algorithm
from .distances import Distances


class Maze:
    @classmethod
    def generate(
        cls,
        width: int,
        height: int,
        algorithm: Algorithm,
        calculate_distances: bool = False,
    ) -> Maze:
        return Maze()

    def __init__(self) -> None:
        pass

    def increment(self, i: int) -> int:
        return i + 1
