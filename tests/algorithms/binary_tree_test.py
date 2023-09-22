from mazes import MutableMazeState
from mazes.algorithms import BinaryTree, BinaryTreeRandom
from mazes.algorithms.utils import flatten
from mazes.grid import Direction as D
from mazes.grid import Grid
from mazes.renderers.text_renderer import TextRenderer

from ..asserts import assert_render


class FakeBinaryTreeRandom(BinaryTreeRandom):
    def __init__(self, fakes: list[D]) -> None:
        self._fakes = fakes
        self._index = 0

    def choose_direction(self, directions: D) -> D:
        direction = self._fakes[self._index]
        self._index += 1
        return direction


class TestBinaryTree:
    def test_binary_tree(self):
        grid = Grid(3, 3)
        state = MutableMazeState(grid, (0, 0))

        directions = [
            [D.E, D.N, D.N],  # y = 2
            [D.N, D.E, D.N],  # y = 1
            [D.E, D.E],  # y = 0
        ]
        text = self.render_grid(state, flatten(directions))

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

    def render_grid(self, state: MutableMazeState, fake_directions: list[D]) -> str:
        random = FakeBinaryTreeRandom(fake_directions)
        binary_tree = BinaryTree(state, random)
        binary_tree.generate()
        text = TextRenderer.render_grid(state.grid)
        return text
