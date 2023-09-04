from collections.abc import Iterator

from .direction import Coordinate

Distance = int | None


class Distances:
    def __init__(self, width: int, height: int, root: Coordinate) -> None:
        self._width = width
        self._height = height
        self._grid = self._prepare_grid()
        self._root = root
        self._max_coordinate = root
        self._max_distance = 0

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

    @property
    def root(self) -> Coordinate:
        return self._root

    @property
    def max_coordinate(self) -> Coordinate:
        return self._max_coordinate

    @property
    def max_distance(self) -> int:
        return self._max_distance

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

    def __getitem__(self, coordinate: Coordinate) -> Distance:
        self.assert_valid_coordinate(coordinate)

        x, y = coordinate
        return self._grid[y][x]

    def __setitem__(self, coordinate: Coordinate, distance: int) -> None:
        self.assert_valid_coordinate(coordinate)

        x, y = coordinate
        self._grid[y][x] = distance
        if distance > self._max_distance:
            self._max_distance = distance
            self._max_coordinate = coordinate

    def coordinates(self) -> Iterator[Coordinate]:
        for y in range(self._height):
            for x in range(self._width):
                yield (x, y)
