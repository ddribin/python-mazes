from __future__ import annotations

from enum import IntFlag, auto
import numpy as np

class Direction(IntFlag):
    Empty = 0
    N = auto()
    S = auto()
    E = auto()
    W = auto()

    def opposite(self) -> Direction:
        match self:
            case self.N:
                return self.S
            case self.S:
                return self.N
            case self.E:
                return self.W
            case self.W:
                return self.E
            case _:
                return self

class Grid:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._grid = np.zeros((width, height))

    @property
    def width(self) -> int:
        return self._width
    
    @property
    def height(self) -> int:
        return self._height

    def __getitem__(self, index: tuple[int, int]) -> Direction | None:
        x, y = index
        if x not in range(self.width):
            return None
        if y not in range(self.height):
            return None
        print(f"{self._grid=}")
        return self._grid[x][y]

