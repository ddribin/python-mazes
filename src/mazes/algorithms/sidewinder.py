from collections.abc import Iterator
import random

from .algorithm import Algorithm

from ..grid import Grid, Coordinate
from ..direction import Direction


class SidewinderRandom:
    def should_close_out(self) -> bool:
        return random.randint(0, 1) == 1

    def choose_north(self, coords: list[Coordinate]) -> Coordinate:
        return random.choice(coords)


class Sidewinder(Algorithm):
    def __init__(self, grid: Grid, random=SidewinderRandom()) -> None:
        self._grid = grid
        self._random = random

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

                if should_close_out:
                    member = random.choose_north(run)
                    grid.link(member, Direction.N)
                    run.clear()
                else:
                    if Direction.E in valid_dirs:
                        grid.link(coord, Direction.E)

                yield
