from collections.abc import Iterator
from typing import TypeVar

from ..distances import Distances
from ..grid import ImmutableGrid, Coordinate

T = TypeVar("T")


def unwrap(x: T | None) -> T:
    assert x is not None
    return x


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

    def path_to(self, goal: Coordinate) -> Distances:
        start = self._root
        current = goal
        grid = self._grid
        distances = self._distances

        breadcrumbs = Distances(self._grid.width, self._grid.height, start)
        breadcrumbs[current] = unwrap(distances[current])

        while current != start:
            links = unwrap(grid[current])
            current_distance = unwrap(distances[current])

            for dir in links:
                neighbor = dir.update_coordinate(current)
                neighbor_distance = unwrap(distances[neighbor])
                if neighbor_distance < current_distance:
                    breadcrumbs[neighbor] = neighbor_distance
                    current = neighbor
                    break

        return breadcrumbs

    def longest_path(self) -> Distances:
        new_root = self.max_coordinate

        new_dijkstra = Dijkstra(self._grid, new_root)
        new_dijkstra.generate()
        goal = new_dijkstra.max_coordinate

        path = new_dijkstra.path_to(goal)
        return path

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
