import random
from collections.abc import Iterator

from ..direction import Direction
from ..grid import Coordinate, Grid
from .algorithm import Algorithm


class RecursiveBacktrackerRandom:
    def random_coordinate(self, grid: Grid) -> Coordinate:
        x = random.randrange(0, grid.width)
        y = random.randrange(0, grid.height)
        return (x, y)

    def choose_direction(self, directions: Direction) -> Direction:
        return random.choice(list(directions))


class RecursiveBacktracker(Algorithm):
    def __init__(self, grid: Grid, random=RecursiveBacktrackerRandom()) -> None:
        self._grid = grid
        self._random = random

    def steps(self) -> Iterator[None]:
        grid = self._grid
        random = self._random

        start_at = random.random_coordinate(grid)
        stack = [start_at]
        yield

        while stack:
            current = stack[-1]
            valid_dirs = grid.valid_directions(current)
            available_directions = Direction.Empty
            for dir in valid_dirs:
                coord = dir.update_coordinate(current)
                if not grid[coord]:
                    available_directions |= dir

            if not available_directions:
                stack.pop()
            else:
                next_direction = random.choose_direction(available_directions)
                grid.link(current, next_direction)
                next_coord = next_direction.update_coordinate(current)
                stack.append(next_coord)
                yield
