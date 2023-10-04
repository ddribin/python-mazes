from __future__ import annotations

from collections.abc import Iterator

from ..core.maze_state import MazeStep, MutableMazeState
from ..distances import Distances
from ..grid import Coordinate, ImmutableGrid
from .utils import unwrap


class Dijkstra:
    def __init__(
        self,
        grid: ImmutableGrid,
        root: Coordinate,
        state: MutableMazeState | None = None,
    ) -> None:
        self._grid = grid
        self._state = state
        self._distances = Distances(grid.width, grid.height, root)

    @property
    def distances(self) -> Distances:
        return self._distances

    def steps(self) -> Iterator[None]:
        distances = self._distances
        root = distances.root
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
            yield

        self._max_distance = max_distance
        self._max_coordinate = max_coord

    def maze_steps(self) -> Iterator[MazeStep]:
        state = self._state
        assert state is not None

        distances = state.distances
        root = distances.root
        grid = state.grid

        state.set_distances(root, 0)
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
                        state.set_distances(next_coord, next_distance)
                        new_frontier.append(next_coord)
                        if next_distance > max_distance:
                            max_coord = next_coord
                            max_distance = next_distance

            frontier = new_frontier
            yield state.pop_maze_step()

        self._max_distance = max_distance
        self._max_coordinate = max_coord

    def generate(self) -> None:
        for _ in self.steps():
            pass

    def path_to(self, goal: Coordinate) -> Distances:
        state = self._state
        assert state is not None

        distances = state.distances
        start = distances.root
        current = goal
        grid = self._grid

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
        new_root = self._distances.max_coordinate

        new_dijkstra = Dijkstra(self._grid, new_root)
        new_dijkstra.generate()
        goal = new_dijkstra._distances.max_coordinate

        path = new_dijkstra.path_to(goal)
        return path
