from __future__ import annotations

from .direction import Direction, Coordinate
from .grid import ImmutableGrid

Distance = int | None


class Distances:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._grid = self._prepare_grid()

    def _prepare_grid(self) -> list[list[Distance]]:
        row: list[Distance] = [None] * self._width
        grid = [row.copy() for _ in range(self._height)]
        return grid

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def is_valid_coordinate(self, coordinate: Coordinate) -> bool:
        x, y = coordinate
        if x not in range(self._width):
            return False
        if y not in range(self._height):
            return False
        return True

    def assert_valid_coordinate(self, coordinate: Coordinate) -> None:
        if not self.is_valid_coordinate(coordinate):
            raise IndexError

    def __getitem__(self, index: Coordinate) -> Distance:
        self.assert_valid_coordinate(index)

        x, y = index
        return self._grid[y][x]

    def __setitem__(self, index: Coordinate, distance: int) -> None:
        self.assert_valid_coordinate(index)

        x, y = index
        self._grid[y][x] = distance

    @classmethod
    def from_root(cls, grid: ImmutableGrid, root: Coordinate) -> Distances:
        distances = Distances(grid.width, grid.height)
        distances[root] = 0
        frontier = [root]

        while frontier:
            new_frontier: list[Coordinate] = []

            for current in frontier:
                linked = grid[current]
                if linked is not None:
                    distance = distances[current]
                    if distance is None:
                        raise RuntimeError

                    for direction in linked:
                        next_coord = direction.update_coordinate(current)
                        next_distance = distances[next_coord]
                        if next_distance is not None:
                            continue
                        distances[next_coord] = distance + 1
                        new_frontier.append(next_coord)

            frontier = new_frontier

        return distances
