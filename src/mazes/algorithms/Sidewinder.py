from collections.abc import Iterator

from .algorithm import Algorithm
from ..grid import Grid, Coordinate


class Sidewinder(Algorithm):
    def __init__(self, grid: Grid) -> None:
        self._grid = grid

    def steps(self) -> Iterator[None]:
        run: list[Coordinate] = []

        return iter([])
