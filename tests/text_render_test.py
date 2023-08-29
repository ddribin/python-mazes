from mazes import Grid, Direction as D
from mazes.text_renderer import TextRenderer
from tests.asserts import *

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
        grid.link((0, 0), D.E)
        grid.link((1, 0), D.E)
        grid.link((2, 0), D.S)

        grid.link((2, 1), D.W)
        grid.link((1, 1), D.W)
        grid.link((0, 1), D.S)
        
        grid.link((0, 2), D.E)
        grid.link((1, 2), D.E)

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
