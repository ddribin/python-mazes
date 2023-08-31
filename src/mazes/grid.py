from collections.abc import Iterator
from typing_extensions import Protocol

from .direction import Direction, Coordinate


class ImmutableGrid(Protocol):
    # Abstract methods

    @property
    def width(self) -> int:
        ...

    @property
    def height(self) -> int:
        ...

    def is_valid_coordinate(self, coordinate: Coordinate) -> bool:
        ...

    def __getitem__(self, index: Coordinate) -> Direction | None:
        ...

    def __iter__(self) -> Iterator[tuple[Coordinate, Direction]]:
        ...

    def coordinates(self) -> Iterator[Coordinate]:
        ...

    # Default implementations

    @property
    def northwest_corner(self) -> Coordinate:
        return (0, 0)

    @property
    def northeast_corner(self) -> Coordinate:
        return (self.width - 1, 0)

    @property
    def southwest_corner(self) -> Coordinate:
        return (0, self.height - 1)

    @property
    def souhteast_corner(self) -> Coordinate:
        return (self.width - 1, self.height - 1)


class Grid(ImmutableGrid):
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._grid = self._prepare_grid()

    def _prepare_grid(self) -> list[list[Direction]]:
        row = [Direction.Empty] * self._width
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

    def __getitem__(self, index: Coordinate) -> Direction | None:
        if self.is_valid_coordinate(index):
            x, y = index
            return self._grid[y][x]
        else:
            return None

    def __iter__(self) -> Iterator[tuple[Coordinate, Direction]]:
        for y in range(self._height):
            for x in range(self._width):
                yield (x, y), self._grid[y][x]

    def coordinates(self) -> Iterator[Coordinate]:
        for y in range(self._height):
            for x in range(self._width):
                yield (x, y)

    # Mutable Methods

    def __setitem__(self, index: Coordinate, direction: Direction) -> None:
        if self.is_valid_coordinate(index):
            x, y = index
            self._grid[y][x] = direction

    def mark(self, coordinate: Coordinate, direction: Direction) -> None:
        if self.is_valid_coordinate(coordinate):
            x, y = coordinate
            self._grid[y][x] |= direction

    def link_path(self, start: Coordinate, directions: list[Direction]) -> Coordinate:
        current = start
        for direction in directions:
            self.link(current, direction)
            current = direction.update_coordinate(current)
        return current

    def link(
        self, coordinate: Coordinate, directions: Direction, bidirectional=True
    ) -> None:
        for direction in directions:
            self._link_one(coordinate, direction, bidirectional)

    def _link_one(
        self, coordinate: Coordinate, direction: Direction, bidirectional: bool
    ) -> None:
        other_coordinate = direction.update_coordinate(coordinate)
        if not self.is_valid_coordinate(other_coordinate):
            return

        self.mark(coordinate, direction)
        if bidirectional:
            direction = direction.opposite()
            self.mark(other_coordinate, direction)
