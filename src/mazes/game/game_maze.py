import math
from collections.abc import Iterator
from enum import Enum, auto

import pygame as pg

from mazes import Coordinate, Direction, Distances, MazeGenerator
from mazes.algorithms import Dijkstra

from .color_gradient import Color, ColorGradient


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

        self._distance_gradient = ColorGradient((253, 246, 227), (38, 139, 210), 256)
        self._path_gradient = ColorGradient((220, 50, 47), (133, 153, 0), 256)

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

    def single_step(self) -> None:
        if self._state is self.State.Generating:
            self.single_step_generating()
        if self._state is self.State.Dijkstra:
            self.single_step_dijkstra()

    def single_step_generating(self) -> None:
        try:
            next(self._maze_steps)
        except StopIteration:
            print("Maze done!")
            self.setup_dijkstra()

    def single_step_dijkstra(self) -> None:
        try:
            assert self._dijkstra_steps is not None
            next(self._dijkstra_steps)
        except StopIteration:
            print("Dijkstra done!")
            self.setup_done()

    def update(self) -> None:
        if self._state is self.State.Generating:
            self.update_generating()
        if self._state is self.State.Dijkstra:
            self.update_dijkstra()

    def update_generating(self) -> None:
        try:
            for _ in range(self.generation_speed * 3):
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
            self.setup_done()

    def setup_done(self) -> None:
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
        fg = (0, 0, 0)

        cell_width = self._cell_width
        cell_height = self._cell_height
        grid = self._maze.grid
        for grid_y in range(self._grid_height):
            for grid_x in range(self._grid_width):
                coord = (grid_x, grid_y)
                dir = grid[coord]
                assert dir is not None

                rect = pg.Rect(x, y, cell_width, cell_height)
                rect_color = self.background_color_of(coord, dir)
                if rect_color is not None:
                    pg.draw.rect(surface, rect_color, rect)

                if Direction.N not in dir:
                    pg.draw.line(surface, fg, (x, y), (x + cell_width, y))
                if Direction.W not in dir:
                    pg.draw.line(surface, fg, (x, y), (x, y + cell_height))
                x += cell_width
            x = start_x
            y += cell_height
        end_x = start_x + self._grid_width * cell_width
        end_y = start_y + self._grid_height * cell_height

        # Draw right edge
        pg.draw.line(surface, fg, (end_x, start_y), (end_x, end_y))
        # Draw bottom edge
        pg.draw.line(surface, fg, (start_x, end_y), (end_x, end_y))

    def background_color_of(self, coord: Coordinate, dir: Direction) -> Color | None:
        color = self.background_color_of_cursor(coord)
        if color is not None:
            return color
        color = self.background_color_of_path(coord)
        if color is not None:
            return color
        color = self.background_color_of_dijkstra(coord)
        if color is not None:
            return color
        if dir is Direction.Empty:
            return (147, 161, 161)

        return None

    def background_color_of_cursor(self, coord: Coordinate) -> Color | None:
        alg = self._maze._algorithm
        if coord in alg.current:
            return (220, 50, 47)
        elif coord in alg.trail:
            return (211, 54, 130)
        elif coord in alg.targets:
            return (181, 137, 0)
        else:
            return None

    def background_color_of_path(self, coord: Coordinate) -> Color | None:
        distances = self._path_distances
        if distances is None:
            return None

        distance = distances[coord]
        if distance is not None:
            max_distance = distances.max_distance
            # inline remap
            intensity = (distance * 255) // max_distance
            color = self._path_gradient.interpolate(intensity)
            return color
        else:
            return None

    def background_color_of_dijkstra(self, coord: Coordinate) -> Color | None:
        if self._dijkstra is None:
            return None
        distances = self._dijkstra.distances
        if distances is None:
            return None
        distance = distances[coord]
        if distance is None:
            return None
        max_distance = distances.max_distance
        # inline remap
        intensity = (distance * 255) // max_distance
        color = self._distance_gradient.interpolate(intensity)
        return color
