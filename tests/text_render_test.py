from mazes import Direction as D
from mazes import Grid
from mazes.renderers.text_renderer import TextRenderer

from .asserts import assert_render


class TestTextRenderer:
    def test_empty_grid(self):
        grid = Grid(3, 3)

        text = self.render(grid)

        expected = """
            +---+---+---+
            |   |   |   |
            +---+---+---+
            |   |   |   |
            +---+---+---+
            |   |   |   |
            +---+---+---+
            """

        assert_render(text, expected)

    def test_east_link(self):
        grid = Grid(3, 3)
        grid.link((0, 0), D.E)

        text = self.render(grid)

        expected = """
            +---+---+---+
            |       |   |
            +---+---+---+
            |   |   |   |
            +---+---+---+
            |   |   |   |
            +---+---+---+
            """

        assert_render(text, expected)

    def test_south_link(self):
        grid = Grid(3, 3)
        grid.link((0, 0), D.S)

        text = self.render(grid)

        expected = """
            +---+---+---+
            |   |   |   |
            +   +---+---+
            |   |   |   |
            +---+---+---+
            |   |   |   |
            +---+---+---+
            """

        assert_render(text, expected)

    def test_link_path(self):
        grid = Grid(3, 3)
        path = []
        path.extend([D.E, D.E, D.S])  # 1st row
        path.extend([D.W, D.W, D.S])  # 2nd row
        path.extend([D.E, D.E])  # 3rd
        grid.link_path((0, 0), path)

        text = self.render(grid)

        expected = """
            +---+---+---+
            |           |
            +---+---+   +
            |           |
            +   +---+---+
            |           |
            +---+---+---+
            """

        assert_render(text, expected)

    def render(self, grid: Grid) -> str:
        return TextRenderer.render_grid(grid)
