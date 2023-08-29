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
            case Direction.N:
                return Direction.S
            case Direction.S:
                return Direction.N
            case Direction.E:
                return Direction.W
            case Direction.W:
                return Direction.E
            case _:
                return self
            
    def update_coordinate(self, coordinate: Coordinate) -> Coordinate:
        x, y = coordinate
        if Direction.N in self: y -= 1
        if Direction.S in self: y += 1
        if Direction.E in self: x += 1
        if Direction.W in self: x -= 1
        return (x, y)
