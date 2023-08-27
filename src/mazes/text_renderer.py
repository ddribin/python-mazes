from .grid import Grid

class TextRenderer:
    def __init__(self, grid: Grid) -> None:
        self._grid = grid

    def render(self) -> str:
        return ""
