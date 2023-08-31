import argparse
import random
import sys
from pathlib import Path

from .maze import Maze


class CommandError(Exception):
    pass


class CommandLine:
    def __init__(self) -> None:
        self.width = 5
        self.height = 5
        self.seed: int | None = None
        self.output: str | None = None

    def execute(self) -> int:
        try:
            self.parse_arguments()
            self.run()
            return 0
        except CommandError as e:
            message = e.args[0]
            sys.stderr.write(f"{message}\n")
            result = e.args[1] if len(e.args) == 2 else 1
            return result

    def parse_arguments(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument("width", type=int, help="Width of the maze")
        parser.add_argument("height", type=int, help="Height of the maze")
        parser.add_argument("-s", "--seed", type=int, help="Random number seed")
        parser.add_argument(
            "-o", "--output", type=str, help="Output file. Supports .txt and .png."
        )
        parser.add_argument(
            "-d", "--distances", action="store_true", help="Calculate distances"
        )

        args = parser.parse_args()

        self.width = args.width
        self.height = args.height
        self.seed = args.seed
        self.output = args.output
        self.calculate_distances = args.distances

    def run(self) -> None:
        seed = self.setup_seed()
        maze = Maze.generate(
            self.width,
            self.height,
            Maze.AlgorithmType.BinaryTree,
            self.calculate_distances,
        )

        self.output_maze(maze)
        print(f"Seed: {seed}")

    def output_maze(self, maze: Maze) -> None:
        output = self.output

        if output is None or output == "-":
            text = str(maze)
            print(text)
            return

        path = Path(output)
        if path.suffix == ".txt":
            text = str(maze)
            path.write_text(text)
            return

        if path.suffix == ".png":
            maze.write_png(str(path))
            return

        raise CommandError(f"Invalid filename: {output}")

    def setup_seed(self) -> int:
        seed = self.seed
        if seed is None:
            seed = random.randint(0, 2**64 - 1)
        random.seed(seed)
        return seed


def main() -> int:
    cli = CommandLine()
    return cli.execute()
