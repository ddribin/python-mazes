from ..distances import Distances
from ..grid import Coordinate, Direction, ImmutableGrid


class TextRenderer:
    @classmethod
    def render_grid(
        cls, grid: ImmutableGrid, distances: Distances | None = None
    ) -> str:
        renderer = TextRenderer(grid, distances)
        return renderer.render()

    def __init__(self, grid: ImmutableGrid, distances: Distances | None = None) -> None:
        self._grid = grid
        self._distances = distances

    def render(self) -> str:
        grid = self._grid
        width = grid.width
        output = "+" + "---+" * width + "\n"
        top = ""
        bottom = ""
        for coordinate, linked in grid:
            x, y = coordinate
            if x == 0:
                top = "|"
                bottom = "+"

            contents = self.contents_of(coordinate)
            body = f" {contents} "  # Three characters
            east_boundary = " " if Direction.E in linked else "|"
            top += body + east_boundary

            south_boundary = "   " if Direction.S in linked else "---"
            corner = "+"
            bottom += south_boundary + corner

            if x == width - 1:
                output += top + "\n"
                output += bottom + "\n"

        return output

    def contents_of(self, coordinate: Coordinate) -> str:
        if self._distances is None:
            return " "

        distance = self._distances[coordinate]
        if distance is None:
            return " "
        return self.to_base36(distance)

    def to_base36(self, i: int) -> str:
        BASE_36 = "0123456789" "abcdefghijklmnopqrstuvwxyz" "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if i < len(BASE_36):
            return BASE_36[i]
        else:
            return "!"
