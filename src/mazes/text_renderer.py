from .grid import Grid, Direction

class TextRenderer:
    def __init__(self, grid: Grid) -> None:
        self._grid = grid

    def render(self) -> str:
        grid = self._grid
        width = grid.width
        output = "+" + "---+" * width + "\n"
        top = ""
        bottom = ""
        for (coordinate, linked) in grid:
            x, y = coordinate
            if x == 0:
                top = "|"
                bottom = "+"

            body = "   " # Three spaces
            east_boundary = " " if Direction.E in linked else "|"
            top += body + east_boundary

            south_boundary = "   " if Direction.S in linked else "---"
            corner = "+"
            bottom += south_boundary + corner

            if x == width-1:
                output += top + "\n"
                output += bottom + "\n"

        return output
