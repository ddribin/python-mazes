from collections.abc import Iterator

from typing_extensions import Protocol

from .direction import Coordinate, Direction


class ImmutableGrid(Protocol):
    # Abstract methods

    @property
    def width(self) -> int:
        ...

    @property
    def height(self) -> int:
        ...

    def __getitem__(self, index: Coordinate) -> Direction | None:
        ...

    def __iter__(self) -> Iterator[tuple[Coordinate, Direction]]:
        ...

    def coordinates(self) -> Iterator[Coordinate]:
        ...

    # Default implementations

    def is_valid_coordinate(self, coordinate: Coordinate) -> bool:
        x, y = coordinate
        if x not in range(self.width):
            return False
        if y not in range(self.height):
            return False
        return True

    def valid_directions(self, coordinate: Coordinate) -> Direction:
        x, y = coordinate
        valid_directions = Direction.Empty
        if y > 0:
            valid_directions |= Direction.N
        if y < self.height - 1:
            valid_directions |= Direction.S
        if x > 0:
            valid_directions |= Direction.W
        if x < self.width - 1:
            valid_directions |= Direction.E

        return valid_directions

    def available_directions(self, coord: Coordinate) -> Direction:
        available_directions = Direction.Empty
        for dir in self.valid_directions(coord):
            next_coord = dir.update_coordinate(coord)
            if self[next_coord] is Direction.Empty:
                available_directions |= dir
        return available_directions

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
    def southeast_corner(self) -> Coordinate:
        return (self.width - 1, self.height - 1)

    @property
    def center(self) -> Coordinate:
        center = (int(self.width / 2), int(self.height / 2))
        return center

    def __str__(self) -> str:
        from .renderers import TextRenderer

        return TextRenderer.render_grid(self)


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

    def unmark(self, coordinate: Coordinate, direction: Direction) -> None:
        if self.is_valid_coordinate(coordinate):
            x, y = coordinate
            self._grid[y][x] &= ~direction

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

    def unlink(
        self, coordinate: Coordinate, directions: Direction, bidirectional=True
    ) -> None:
        for direction in directions:
            self._unlink_one(coordinate, direction, bidirectional)

    def _unlink_one(
        self, coordinate: Coordinate, direction: Direction, bidirectional: bool
    ) -> None:
        other_coordinate = direction.update_coordinate(coordinate)
        if not self.is_valid_coordinate(other_coordinate):
            return

        self.unmark(coordinate, direction)
        if bidirectional:
            direction = direction.opposite()
            self.unmark(other_coordinate, direction)
