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
        self.overlay_type: str | None = None
        self.algorithm = "binary_tree"

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
        algorithms = ["binary-tree", "sidewinder", "recursive-backtracker"]
        parser.add_argument(
            "-a", "--algorithm", choices=algorithms, default="binary-tree"
        )
        parser.add_argument(
            "-O", "--overlay", choices=["none", "distance", "path", "max", "longest"]
        )

        args = parser.parse_args()

        self.width = args.width
        self.height = args.height
        self.seed = args.seed
        self.output = args.output
        self.overlay_type = args.overlay
        self.algorithm = args.algorithm

    def run(self) -> None:
        seed = self.setup_seed()
        maze = self.generate_maze()
        self.output_maze(maze)
        print(f"Seed: {seed}")

    def generate_maze(self) -> Maze:
        maze = Maze.generate(
            self.width,
            self.height,
            self.maze_algorithm_type(),
            self.maze_overlay_type(),
        )
        return maze

    def maze_overlay_type(self) -> Maze.OverlayType:
        match self.overlay_type:
            case "distance":
                return Maze.OverlayType.Distance
            case "path":
                return Maze.OverlayType.PathTo
            case "max":
                return Maze.OverlayType.PathToMax
            case "longest":
                return Maze.OverlayType.LongestPath
            case None:
                return Maze.OverlayType.Nothing
            case unknown:
                raise ValueError(unknown)

    def maze_algorithm_type(self) -> Maze.AlgorithmType:
        match self.algorithm:
            case "binary-tree":
                return Maze.AlgorithmType.BinaryTree
            case "sidewinder":
                return Maze.AlgorithmType.Sidewinder
            case "recursive-backtracker":
                return Maze.AlgorithmType.RecursiveBacktracker
            case unknown:
                raise ValueError(unknown)

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
