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
        self._current: set[Coordinate] = set()
        self._trail: set[Coordinate] = set()
        self._targets: set[Coordinate] = set()

    @property
    def current(self) -> set[Coordinate]:
        return self._current

    @property
    def trail(self) -> set[Coordinate]:
        return self._trail

    @property
    def targets(self) -> set[Coordinate]:
        return self._targets

    def steps(self) -> Iterator[None]:
        grid = self._grid
        random = self._random

        start_at = random.random_coordinate(grid)
        stack = [start_at]

        while stack:
            current = stack[-1]
            valid_dirs = grid.valid_directions(current)
            available_directions = Direction.Empty
            for dir in valid_dirs:
                coord = dir.update_coordinate(current)
                if not grid[coord]:
                    available_directions |= dir
                    coord = dir.update_coordinate(current)

            self._current = {current}
            self._trail = set(stack)

            if not available_directions:
                self._targets = set()
                yield
                stack.pop()
            else:
                self._targets = {
                    dir.update_coordinate(current) for dir in available_directions
                }
                yield
                next_direction = random.choose_direction(available_directions)
                grid.link(current, next_direction)
                next_coord = next_direction.update_coordinate(current)
                stack.append(next_coord)

        self._current = set()
        self._trail = set()
        self._targets = set()
        yield
