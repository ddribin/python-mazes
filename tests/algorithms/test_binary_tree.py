from mazes.algorithms import BinaryTree, BinaryTreeRandom
from mazes.grid import Grid, Direction as D
from mazes.renderers.text_renderer import TextRenderer
from ..asserts import *

class FakeBinaryTreeRandom(BinaryTreeRandom):
    def __init__(self, fakes: list[D]) -> None:
        self._fakes = fakes
        self._index = 0

    def choose_direction(self, directions: list[D]) -> D:
        direction = self._fakes[self._index]
        self._index += 1
        return direction

class TestBinaryTree:
    def test_binary_tree(self):
        grid = Grid(3, 3)

        directions = [
            D.E, D.E,
            D.N, D.E, D.N,
            D.E, D.N, D.N,
        ]
        text = self.render_grid(grid, directions)

        expected = """
            +---+---+---+
            |           |
            +   +---+   +
            |   |       |
            +---+   +   +
            |       |   |
            +---+---+---+
            """
        assert_render(text, expected)


    def render_grid(self, grid: Grid, fake_directions: list[D]) -> str:
        random = FakeBinaryTreeRandom(fake_directions)
        binary_tree = BinaryTree(grid, random)
        binary_tree.generate()
        text = TextRenderer.render_grid(grid)
        return text
