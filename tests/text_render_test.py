from mazes import Grid, Direction as D
from mazes.text_renderer import TextRenderer

import textwrap

def assert_render(actual: str, expected: str) -> None:
    __tracebackhide__ = True
    expected = textwrap.dedent(expected).lstrip()
    assert actual == expected
    actual_lines = actual.splitlines()
    expected_lines = expected.splitlines()
    for i, lines in enumerate(zip(actual_lines, expected_lines)):
        actual_line, expected_line = lines
        assert actual_line == expected_line, f"line {i}"

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
        render = TextRenderer(grid)
        return render.render()
