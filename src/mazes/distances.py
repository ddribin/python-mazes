from __future__ import annotations

from collections.abc import Iterator

from .direction import Direction, Coordinate
from .grid import ImmutableGrid

Distance = int | None


class Distances:
    def __init__(self, width: int, height: int, root: Coordinate) -> None:
        self._width = width
        self._height = height
        self._root = root
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

    def coordinates(self) -> Iterator[Coordinate]:
        for y in range(self._height):
            for x in range(self._width):
                yield (x, y)

    def _set_max(self, coordinate: Coordinate, distance: int) -> None:
        self._max = (coordinate, distance)

    @property
    def max(self) -> tuple[Coordinate, int]:
        return self._max

    @property
    def max_(self) -> tuple[Coordinate, int]:
        max_distance = 0
        max_coord = self._root

        for coord in self.coordinates():
            distance = self[coord]
            if distance is not None and distance > max_distance:
                max_coord = coord
                max_distance = distance

        return (max_coord, max_distance)

    @classmethod
    def from_root(cls, grid: ImmutableGrid, root: Coordinate) -> Distances:
        distances = Distances(grid.width, grid.height, root)
        distances[root] = 0
        frontier = [root]
        max_coord = root
        max_distance = 0

        while frontier:
            new_frontier: list[Coordinate] = []

            for current in frontier:
                linked = grid[current]
                if linked is not None:
                    distance = distances[current]
                    assert distance is not None

                    for direction in linked:
                        next_coord = direction.update_coordinate(current)
                        next_distance = distances[next_coord]
                        if next_distance is not None:
                            continue
                        next_distance = distance + 1
                        distances[next_coord] = next_distance
                        new_frontier.append(next_coord)
                        if next_distance > max_distance:
                            max_coord = next_coord
                            max_distance = next_distance

            frontier = new_frontier

        distances._set_max(max_coord, max_distance)

        return distances
