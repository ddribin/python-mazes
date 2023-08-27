from mazes import Grid, Direction as D
from mazes.text_renderer import TextRenderer


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

        assert text == ""

    def render(self, grid: Grid) -> str:
        render = TextRenderer(grid)
        return render.render()
