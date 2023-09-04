from enum import Enum, auto

from PIL import Image, ImageDraw

from ..distances import Distances
from ..grid import Coordinate, Direction, ImmutableGrid

Color = tuple[int, int, int]


class Mode(Enum):
    Backgrounds = auto()
    Walls = auto()


class ImageRenderer:
    @classmethod
    def render_grid_to_png_file(
        cls,
        grid: ImmutableGrid,
        file_name: str,
        distances: Distances | None = None,
        max_distance=0,
    ) -> None:
        renderer = ImageRenderer(grid, distances, max_distance)
        renderer.render_png_file(file_name)

    def __init__(
        self,
        grid: ImmutableGrid,
        distances: Distances | None = None,
        max_distance=0,
        cell_size=5,
        padding=5,
    ) -> None:
        self._grid = grid
        self._distances = distances
        self._max_distance = max_distance
        self._cell_size = cell_size
        self._padding = padding

    def render_png_file(self, file_name: str) -> None:
        image = self.render_png_image()
        image.save(file_name)

    def render_png_image(self) -> Image.Image:
        cell_size = self._cell_size
        padding = self._padding
        grid = self._grid

        img_width = cell_size * grid.width + padding * 2
        img_height = cell_size * grid.height + padding * 2

        background = (255, 255, 255)
        wall = (0, 0, 0)

        image = Image.new("RGBA", (img_width + 1, img_height + 1), color=background)
        draw = ImageDraw.Draw(image)

        for mode in [Mode.Backgrounds, Mode.Walls]:
            for coords, dir in grid:
                grid_x, grid_y = coords
                x1 = grid_x * cell_size + padding
                y1 = grid_y * cell_size + padding
                x2 = (grid_x + 1) * cell_size + padding
                y2 = (grid_y + 1) * cell_size + padding

                if mode == Mode.Backgrounds:
                    color = self.background_color_of(coords)
                    draw.rectangle((x1, y1, x2, y2), fill=color)
                else:
                    if Direction.N not in dir:
                        draw.line((x1, y1, x2, y1), wall)
                    if Direction.W not in dir:
                        draw.line((x1, y1, x1, y2), wall)
                    if Direction.E not in dir:
                        draw.line((x2, y1, x2, y2), wall)
                    if Direction.S not in dir:
                        draw.line((x1, y2, x2, y2), wall)

        return image

    def background_color_of(self, coord: Coordinate) -> Color | None:
        if self._distances is None:
            return None
        distance = self._distances[coord]
        if distance is None:
            return None
        if self._max_distance == 0:
            return (255, 0, 0)
        intensity = float(self._max_distance - distance) / self._max_distance
        dark = round(255 * intensity)
        bright = 128 + round(127 * intensity)
        return (dark, bright, bright)
