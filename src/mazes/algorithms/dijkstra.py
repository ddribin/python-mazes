from ..distances import Distances
from ..grid import ImmutableGrid, Coordinate
from collections.abc import Iterator


class Dijkstra:
    def __init__(self, grid: ImmutableGrid, root: Coordinate) -> None:
        self._grid = grid
        self._distances = Distances(grid.width, grid.height)
        self._root = root
        self._max_distance = 0
        self._max_coordinate = root

    @property
    def distances(self) -> Distances:
        return self._distances

    @property
    def max_distance(self) -> int:
        return self._max_distance

    @property
    def max_coordinate(self) -> Coordinate:
        return self._max_coordinate

    def steps(self) -> Iterator[None]:
        yield

    def generate(self) -> None:
        distances = self._distances
        root = self._root
        grid = self._grid

        distances[root] = 0
        frontier = [root]
        max_coord = root
        max_distance = 0

        while frontier:
            new_frontier: list[Coordinate] = []

            for current in frontier:
                linked = grid[current]
                if linked is not None:
                    distance = distances[current]
                    assert distance is not None

                    for direction in linked:
                        next_coord = direction.update_coordinate(current)
                        next_distance = distances[next_coord]
                        if next_distance is not None:
                            continue
                        next_distance = distance + 1
                        distances[next_coord] = next_distance
                        new_frontier.append(next_coord)
                        if next_distance > max_distance:
                            max_coord = next_coord
                            max_distance = next_distance

            frontier = new_frontier

        self._max_distance = max_distance
        self._max_coordinate = max_coord
