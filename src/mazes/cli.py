import argparse
import random

from .grid import Grid
from .renderers import TextRenderer, ImageRenderer
from .algorithms import Algorithm, BinaryTree


class MazeCli:
    def __init__(self) -> None:
        self.width = 5
        self.height = 5
        self.seed: int | None = None
        self.output: str | None = None

    def execute(self) -> int:
        self.parse_arguments()
        return self.run()

    def parse_arguments(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument("width", type=int, help="Width of the maze")
        parser.add_argument("height", type=int, help="Height of the maze")
        parser.add_argument("-s", "--seed", type=int, help="Random number seed")
        parser.add_argument("-o", "--output", type=str, help="Output file")

        args = parser.parse_args()

        self.width = args.width
        self.height = args.height
        self.seed = args.seed
        self.output = args.output

    def run(self) -> int:
        seed = self.setup_seed()
        grid = Grid(self.width, self.height)
        algorithm = self.make_algorithm(grid)
        algorithm.generate()

        print(TextRenderer.render_grid(grid))
        print(f"Seed: {seed}")

        if self.output is not None:
            ImageRenderer.render_grid_to_png_file(grid, self.output)
        return 0

    def make_algorithm(self, grid: Grid) -> Algorithm:
        algorithm = BinaryTree(grid)
        return algorithm

    def setup_seed(self) -> int:
        seed = self.seed
        if seed is None:
            seed = random.randint(0, 2**64 - 1)
        random.seed(seed)
        return seed


def maze_cli() -> int:
    cli = MazeCli()
    return cli.execute()
