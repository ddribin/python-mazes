from __future__ import annotations

from enum import IntFlag, auto
from typing import TypeAlias

Coordinate: TypeAlias = tuple[int, int]

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
            
    def update_coordinate(self, coordinate: Coordinate) -> Coordinate:
        x, y = coordinate
        if self.N in self: y -= 1
        if self.S in self: y += 1
        if self.E in self: x += 1
        if self.W in self: x -= 1
        return (x, y)
