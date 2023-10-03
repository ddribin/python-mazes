import logging
import math
from collections.abc import Iterator
from enum import Enum, auto

import pygame as pg

from mazes import (
    AlgorithmType,
    Coordinate,
    Direction,
    Distances,
    MazeGenerator,
    MazeOptions,
    MazeStepper,
)
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
        self.logger = logging.getLogger(__name__)
        self._grid_width = grid_width
        self._grid_height = grid_height
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._padding_x = padding_x
        self._padding_y = padding_y

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
        options = MazeOptions(self._grid_width, self._grid_height)

        options.algorithmType = AlgorithmType.RecursiveBacktracker
        options.start = options.northwest_corner
        options.end = options.southeast_corner

        # options.algorithmType = AlgorithmType.Sidewinder
        # options.start = options.southwest_corner
        # options.end = options.southeast_corner

        # options.algorithmType = AlgorithmType.BinaryTree
        # options.start = options.southwest_corner
        # options.end = options.northwest_corner

        logging.info("options: %s", options)
        self._maze = MazeGenerator(options)
        print(f"Seed: {self._maze.seed}")
        self._maze_stepper = self._maze.make_stepper()
        self._state = self.State.Generating
        self._generation_speed = 0
        self._generation_speed_sign = 1
        self._generation_timer = 0
        self._generation_timer_steps = 0
        self._generation_timer_multiplier = 3
        self._dijkstra: Dijkstra | None = None
        self._dijkstra_steps: Iterator[None] | None = None
        self._path_distances: Distances | None = None
        self._pulse_gradient = ColorGradient((220, 50, 47), (235, 136, 134), 256)
        self._pulse_tick = 0

        self.clear_cursors()

    @property
    def generation_velocity(self) -> int:
        return self._generation_speed * self._generation_speed_sign

    @generation_velocity.setter
    def generation_velocity(self, velocity: int) -> None:
        if velocity >= 0:
            self._generation_speed = velocity
            self._generation_speed_sign = 1
        else:
            self._generation_speed = velocity * -1
            self._generation_speed_sign = -1

    def clear_cursors(self) -> None:
        self._current: set[Coordinate] = set()
        self._trail: set[Coordinate] = set()
        self._targets: set[Coordinate] = set()

    def update_cursors(self) -> None:
        run = self._maze.state.run
        if len(run) > 0:
            self._current = {run[-1]}
            self._trail = set(run[:-1])
        else:
            self._current = set()
            self._trail = set()
        self._targets = set(self._maze.state.target_coordinates)

    def single_step_forward(self) -> None:
        if self._state is self.State.Generating:
            self.single_step_generating()
        if self._state is self.State.Dijkstra:
            self.single_step_dijkstra()

    def single_step_generating(self) -> None:
        self._pulse_tick = 0
        did_step = self._maze_stepper.step_forward()
        self.update_cursors()

        if not did_step:
            self.logger.info("Maze done!")
            self.setup_dijkstra()

    def single_step_dijkstra(self) -> None:
        self._pulse_tick = 0
        did_step = self._dijkstra_stepper.step_forward()

        if not did_step:
            self.logger.info("Dijkstra done!")
            self.setup_done()

    def single_step_dijkstra_x(self) -> None:
        try:
            assert self._dijkstra_steps is not None
            self._pulse_tick = 0
            next(self._dijkstra_steps)
        except StopIteration:
            self.logger.info("Dijkstra done!")
            self.setup_done()

    def single_step_backward(self) -> None:
        if self._state is self.State.Generating:
            self.single_step_backward_generating()
        if self._state is self.State.Dijkstra:
            self.single_step_backward_dijkstra()

    def single_step_backward_generating(self) -> None:
        self._pulse_tick = 0
        did_step = self._maze_stepper.step_backward()
        if did_step:
            self.update_cursors()
        else:
            self.clear_cursors()

    def single_step_backward_dijkstra(self) -> None:
        self._pulse_tick = 0
        _ = self._dijkstra_stepper.step_backward()

    def update(self) -> None:
        self.update_generation_timer()
        if self._state is self.State.Generating:
            self.update_generating()
        if self._state is self.State.Dijkstra:
            self.update_dijkstra()
        if self._state is self.State.Done:
            self._pulse_tick = 0
        else:
            self._pulse_tick += 9

    def update_generation_timer(self) -> None:
        self._generation_timer += (
            self._generation_speed * self._generation_timer_multiplier
        )
        self._generation_timer_steps = self._generation_timer // 100
        self._generation_timer %= 100

    def update_generating(self) -> None:
        did_step = True
        if self._generation_speed_sign > 0:
            did_step = self.update_generating_forward()
        if self._generation_speed_sign < 0:
            did_step = self.update_generating_backward()

        if did_step:
            self.update_cursors()
        else:
            self.logger.info("Maze done!")
            self.setup_dijkstra()

    def update_generating_forward(self) -> bool:
        did_step = True
        for _ in range(self._generation_timer_steps):
            did_step = self._maze_stepper.step_forward()
            if not did_step:
                break
        return did_step

    def update_generating_backward(self) -> bool:
        for _ in range(self._generation_timer_steps):
            did_step = self._maze_stepper.step_backward()
            if not did_step:
                break
        return True

    def setup_dijkstra(self) -> None:
        self.clear_cursors()
        self._generation_timer_multiplier = 1
        self._dijkstra = Dijkstra(
            self._maze.grid, self._maze.start, self._maze.mutable_state
        )
        self._dijkstra_steps = self._dijkstra.steps()
        self._dijkstra_stepper = MazeStepper(
            self._maze.mutable_state, self._dijkstra.maze_steps()
        )
        self._state = self.State.Dijkstra
        self._pulse_gradient = ColorGradient((38, 139, 210), (22, 82, 124), 256)
        self._pulse_tick = 0

    def update_dijkstra(self) -> None:
        try:
            for _ in range(self._generation_timer_steps):
                assert self._dijkstra_steps is not None
                next(self._dijkstra_steps)
        except StopIteration:
            self.logger.info("Dijkstra done!")
            self.setup_done()

    def setup_done(self) -> None:
        assert self._dijkstra is not None
        self.logger.info("Start %r -> End: %r", self._maze.start, self._maze.end)
        goal = self._maze.end
        self._path_distances = self._dijkstra.path_to(goal)
        self._state = self.State.Done

    def run_to_completion(self) -> None:
        if self._state is self.State.Generating:
            self._maze_stepper.step_forward_until_end()
            self.setup_dijkstra()
        elif self._state is self.State.Dijkstra:
            assert self._dijkstra_steps is not None
            for _ in self._dijkstra_steps:
                pass
            self.setup_done()

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
        if coord in self._current:
            val = self._pulse_tick % 512
            if val > 255:
                val = 255 - (val - 256)
            return self._pulse_gradient.interpolate(val)
        elif coord in self._trail:
            return (211, 54, 130)
        elif coord in self._targets:
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

        color: Color
        if distance == max_distance:
            val = self._pulse_tick % 512
            if val > 255:
                val = 255 - (val - 256)
            color = self._pulse_gradient.interpolate(val)
        else:
            # inline remap
            intensity = (distance * 255) // max_distance
            color = self._distance_gradient.interpolate(intensity)

        return color
