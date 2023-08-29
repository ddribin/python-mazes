from .grid import Grid
from .text_renderer import TextRenderer
from .algorithms import BinaryTree

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
        algorithm = BinaryTree(grid)
        render = TextRenderer(grid)
        self.generate_all(algorithm)
        print(render.render())
        print(f"Seed: {seed}")
        return 0
    
    def generate_all(self, algorithm: BinaryTree) -> None:
        for _ in algorithm.generate():
            pass

    def setup_seed(self) -> int:
        seed = self.seed
        if seed is None:
            seed = random.randint(0, 2**64 - 1)
        random.seed(seed)
        return seed

def maze_cli() -> int:
    cli = MazeCli()
    return cli.execute()
