from ..distances import Distances
from ..grid import ImmutableGrid, Coordinate
from collections.abc import Iterator


class Dijkstra:
    def __init__(self, grid: ImmutableGrid, root: Coordinate) -> None:
        self._grid = grid
        self._root = root
        self._max = 0

    def steps(self) -> Iterator[None]:
        yield

    def generate(self) -> None:
        pass
