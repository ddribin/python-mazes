from __future__ import annotations

from enum import IntFlag, auto

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
