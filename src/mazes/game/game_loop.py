import math

import pygame as pg

from mazes import Direction, MazeGenerator


class VisualMaze:
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

        self.reset()

    def reset(self) -> None:
        self._maze = MazeGenerator(
            self._grid_width,
            self._grid_height,
            (0, 0),
            MazeGenerator.AlgorithmType.RecursiveBacktracker,
        )
        self._maze_steps = self._maze.steps()
        self._maze_generated = False
        self.generation_speed = 0

    def update(self) -> None:
        if not self._maze_generated:
            try:
                for _ in range(self.generation_speed):
                    next(self._maze_steps)
            except StopIteration:
                print("Maze done!")
                self._maze_generated = True

    def run_to_completion(self) -> None:
        for _ in self._maze_steps:
            pass
        self._maze_generated = True

    def draw(self, surface: pg.Surface) -> None:
        start_x, start_y = (self._padding_x, self._padding_y)
        x, y = (start_x, start_y)
        if self._maze_generated:
            fg = (255, 255, 255)
        else:
            fg = (255, 0, 255)
        cell_width = self._cell_width
        cell_height = self._cell_height
        grid = self._maze.grid
        for grid_y in range(self._grid_height):
            for grid_x in range(self._grid_width):
                dir = grid[grid_x, grid_y]
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


class GameLoop:
    def __init__(self) -> None:
        self._running = True
        self.width = 800
        self.height = 600

    def execute(self) -> int:
        pg.init()
        pg.display.set_caption("Maze Game")
        SCREENRECT = pg.Rect(0, 0, self.width, self.height)
        FPS = 60
        winstyle = 0  # |FULLSCREEN
        bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
        self._screen = pg.display.set_mode(
            SCREENRECT.size, winstyle, bestdepth, vsync=1
        )
        clock = pg.time.Clock()
        self.init()

        # Main loop
        frame = 0
        while self._running:
            self.update()

            self.draw()
            pg.display.flip()

            clock.tick(FPS)
            frame += 1
            frame = frame % FPS
            if frame == 0:
                fps = clock.get_fps()
                print(f"FPS: {fps}")

        pg.quit()
        return 0

    def init(self) -> None:
        self._player = pg.Rect((300, 250, 50, 50))
        self._maze = VisualMaze(24, 18, self.width, self.height, 40, 40)

    def update(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False

        self._maze.update()

        key = pg.key.get_pressed()
        if key[pg.K_r]:
            self._maze.reset()
        if key[pg.K_SPACE]:
            self._maze.generation_speed = 1
        else:
            self._maze.generation_speed = 0
        if key[pg.K_j]:
            self._maze.run_to_completion()
        if key[pg.K_q]:
            self._running = False

    def draw(self) -> None:
        screen = self._screen
        screen.fill((0, 0, 0))

        self._maze.draw(screen)


def main() -> int:
    game_loop = GameLoop()
    return game_loop.execute()
