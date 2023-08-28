from .grid import Grid
from .text_renderer import TextRenderer
from .algorithms import BinaryTree


def maze_cli() -> int:
    grid = Grid(10, 10)
    BinaryTree.on(grid)
    render = TextRenderer(grid)
    print(render.render())
    return 0
