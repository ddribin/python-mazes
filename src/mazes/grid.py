from .direction import Direction

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

    def __getitem__(self, index: tuple[int, int]) -> Direction | None:
        x, y = index
        if x not in range(self._width):
            return None
        if y not in range(self._height):
            return None
        return self._grid[y][x]
    
    def link(self, direction: Direction, bidirectional = True) -> None:
        ...

