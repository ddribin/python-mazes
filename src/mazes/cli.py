from .grid import Grid
from .text_renderer import TextRenderer
from .algorithms import Algorithm, BinaryTree

import argparse
import random

class MazeCli:
    def __init__(self) -> None:
        self.width = 5
        self.height = 5
        self.seed: int | None = None

    def execute(self) -> int:
        self.parse_arguments()
        return self.run()
    
    def parse_arguments(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument("width", type=int, help="Width of the maze")
        parser.add_argument("height", type=int, help="Height of the maze")
        parser.add_argument("-s", "--seed", type=int, help="Random number seed")

        args = parser.parse_args()

        self.width = args.width
        self.height = args.height
        self.seed = args.seed

    def run(self) -> int:
        seed = self.setup_seed()
        grid = Grid(self.width, self.height)
        algorithm = self.make_algorithm(grid)
        render = TextRenderer(grid)
        algorithm.generate_all()
        print(render.render())
        print(f"Seed: {seed}")
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
