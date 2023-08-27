from .direction import Direction, Coordinate

class Grid:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._grid = self._prepare_grid()

    def _prepare_grid(self) -> list[list[Direction]]:
        grid = []
        for y in range(self._height):
            row = []
            for x in range(self._width):
                row.append(Direction.Empty)
            grid.append(row)
        print(f"{grid=}")
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
    
    def __setitem__(self, index: Coordinate, direction: Direction) -> None:
        if self.is_valid_coordinate(index):
            x, y = index
            self._grid[y][x] = direction
    
    def mark(self, coordinate: Coordinate, direction: Direction) -> None:
        if self.is_valid_coordinate(coordinate):
            x, y = coordinate
            self._grid[y][x] |= direction
    
    def link(self, coordinate: Coordinate, direction: Direction,
             bidirectional = True) -> None:
        other_coordinate = direction.update_coordinate(coordinate)
        if not self.is_valid_coordinate(other_coordinate):
            return
        
        self.mark(coordinate, direction)
        if bidirectional:
            direction = direction.opposite()
            self.mark(other_coordinate, direction)



