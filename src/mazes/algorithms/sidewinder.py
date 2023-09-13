import random
from collections.abc import Iterator

from ..direction import Direction
from ..grid import Coordinate, Grid
from .algorithm import Algorithm


class SidewinderRandom:
    def should_close_out(self) -> bool:
        return random.randint(0, 1) == 1

    def choose_north(self, coords: list[Coordinate]) -> Coordinate:
        return random.choice(coords)


class Sidewinder(Algorithm):
    def __init__(self, grid: Grid, random=SidewinderRandom()) -> None:
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

        for y in range(grid.height):
            run: list[Coordinate] = []

            for x in range(grid.width):
                coord = (x, y)
                run.append(coord)

                valid_dirs = grid.valid_directions(coord)
                at_eastern_boundary = Direction.E not in valid_dirs
                at_northern_boundary = Direction.N not in valid_dirs

                should_close_out = at_eastern_boundary or (
                    not at_northern_boundary and random.should_close_out()
                )

                self._current = {coord}
                self._trail = set(run)

                if should_close_out:
                    self._targets = {
                        Direction.N.update_coordinate(coord) for coord in run
                    }
                    yield

                    member = random.choose_north(run)
                    grid.link(member, Direction.N)
                    run.clear()
                else:
                    self._targets = {Direction.E.update_coordinate(coord)}
                    yield

                    grid.link(coord, Direction.E)

        self._current = set()
        self._trail = set()
        self._targets = set()
        yield
