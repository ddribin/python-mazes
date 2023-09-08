import math
from collections.abc import Iterator
from enum import Enum, auto

import pygame as pg

from mazes import Coordinate, Direction, Distances, MazeGenerator
from mazes.algorithms import Dijkstra

Color = tuple[int, int, int]


class GameMaze:
    class State(Enum):
        Generating = auto()
        Dijkstra = auto()
        Done = auto()

    def __init__(
        self,
        grid_width: int,
        grid_height: int,
        screen_width: int,
        screen_height: int,
        padding_x: int,
        padding_y: int,
    ) -> None:
        self._grid_width = grid_width
        self._grid_height = grid_height
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._padding_x = padding_x
        self._padding_y = padding_y
        self.generation_speed = 0

        self._cell_width = math.floor((screen_width - padding_x * 2) / grid_width)
        self._cell_height = math.floor((screen_height - padding_y * 2) / grid_height)

        # Adjust padding to center in screen
        actual_width = self._cell_width * grid_width
        self._padding_x = math.floor((screen_width - actual_width) / 2)
        actual_height = self._cell_height * grid_height
        self._padding_y = math.floor((screen_height - actual_height) / 2)

        self._gradient_start = (255, 255, 255)
        self._gradient_end = (128, 0, 255)

        self.reset()

    def reset(self) -> None:
        self._maze = MazeGenerator(
            self._grid_width,
            self._grid_height,
            (0, self._grid_height - 1),
            MazeGenerator.AlgorithmType.RecursiveBacktracker,
        )
        self._maze_steps = self._maze.steps()
        self._state = self.State.Generating
        self.generation_speed = 0
        self._dijkstra: Dijkstra | None = None
        self._dijkstra_steps: Iterator[None] | None = None
        self._path_distances: Distances | None = None

    def update(self) -> None:
        if self._state is self.State.Generating:
            self.update_generating()
        if self._state is self.State.Dijkstra:
            self.update_dijkstra()

    def update_generating(self) -> None:
        try:
            for _ in range(self.generation_speed):
                next(self._maze_steps)
        except StopIteration:
            print("Maze done!")
            self.setup_dijkstra()

    def setup_dijkstra(self) -> None:
        self._dijkstra = Dijkstra(self._maze.grid, self._maze.grid.northwest_corner)
        self._dijkstra_steps = self._dijkstra.steps()
        self._state = self.State.Dijkstra

    def update_dijkstra(self) -> None:
        try:
            for _ in range(self.generation_speed):
                assert self._dijkstra_steps is not None
                next(self._dijkstra_steps)
        except StopIteration:
            print("Dijkstra done!")
            assert self._dijkstra is not None
            goal = self._maze.grid.southeast_corner
            self._path_distances = self._dijkstra.path_to(goal)
            self._state = self.State.Done

    def run_to_completion(self) -> None:
        if self._state is not self.State.Generating:
            return

        for _ in self._maze_steps:
            pass

        self.setup_dijkstra()

    def draw(self, surface: pg.Surface) -> None:
        start_x, start_y = (self._padding_x, self._padding_y)
        x, y = (start_x, start_y)
        if self._state is self.State.Generating:
            fg = (128, 0, 128)
        else:
            fg = (0, 0, 0)
        cell_width = self._cell_width
        cell_height = self._cell_height
        grid = self._maze.grid
        for grid_y in range(self._grid_height):
            for grid_x in range(self._grid_width):
                coord = (grid_x, grid_y)
                rect = pg.Rect(x, y, cell_width, cell_height)
                rect_color = self.background_color_of(coord)
                if rect_color is not None:
                    pg.draw.rect(surface, rect_color, rect)

                dir = grid[coord]
                assert dir is not None
                if Direction.N not in dir:
                    pg.draw.line(surface, fg, (x, y), (x + cell_width, y))
                if Direction.W not in dir:
                    pg.draw.line(surface, fg, (x, y), (x, y + cell_height))
                x += cell_width
            x = start_x
            y += cell_height
        end_x = start_x + self._grid_width * cell_width
        end_y = start_y + self._grid_height * cell_height
        pg.draw.line(surface, fg, (end_x, start_y), (end_x, end_y))
        pg.draw.line(surface, fg, (start_x, end_y), (end_x, end_y))

    def background_color_of(self, coord: Coordinate) -> Color | None:
        if self._path_distances is not None:
            distances = self._path_distances
            distance = distances[coord]
            if distance is not None:
                max_distance = distances.max_distance
                intensity = float(max_distance - distance) / max_distance
                start_color = (255, 0, 0)
                end_color = (0, 255, 0)
                return self.interpolate_color(start_color, end_color, intensity)
        if self._dijkstra is None:
            return None
        distances = self._dijkstra.distances
        if distances is None:
            return None
        distance = distances[coord]
        if distance is None:
            return None
        max_distance = distances.max_distance
        intensity = float(max_distance - distance) / max_distance
        color = self.interpolate_color(
            self._gradient_start, self._gradient_end, intensity
        )
        return color

    def interpolate_color(self, c1: Color, c2: Color, val: float) -> Color:
        r1, g1, b1 = c1
        r2, g2, b2 = c2
        r = round((r1 - r2) * val) + r2
        g = round((g1 - g2) * val) + g2
        b = round((b1 - b2) * val) + b2
        return (r, g, b)
