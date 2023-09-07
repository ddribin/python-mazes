import math

import pygame as pg

from mazes import Direction, MazeGenerator


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
        self._grid_width = 24
        self._grid_height = 18
        self._padding_x = 40
        self._padding_y = 40
        self._cell_width = math.floor(
            (self.width - self._padding_x * 2) / self._grid_width
        )
        self._cell_height = math.floor(
            (self.height - self._padding_x * 2) / self._grid_height
        )

        # Adjust padding to center in screen
        actual_width = self._cell_width * self._grid_width
        self._padding_x = math.floor((self.width - actual_width) / 2)
        actual_height = self._cell_height * self._grid_height
        self._padding_y = math.floor((self.height - actual_height) / 2)

        self.start_maze()

    def start_maze(self) -> None:
        self._maze = MazeGenerator(
            self._grid_width,
            self._grid_height,
            (0, 0),
            MazeGenerator.AlgorithmType.RecursiveBacktracker,
        )
        self._maze_steps = self._maze.steps()
        self._maze_generated = False
        self._maze_generation_speed = 0

    def update(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False

        if not self._maze_generated:
            try:
                for _ in range(self._maze_generation_speed):
                    next(self._maze_steps)
            except StopIteration:
                print("Maze done!")
                self._maze_generated = True

        key = pg.key.get_pressed()
        if key[pg.K_r]:
            self.start_maze()
        if key[pg.K_SPACE]:
            self._maze_generation_speed = 1
        else:
            self._maze_generation_speed = 0
        if key[pg.K_j]:
            for _ in self._maze_steps:
                pass
            self._maze_generated = True
        if key[pg.K_q]:
            self._running = False

    def draw(self) -> None:
        screen = self._screen
        screen.fill((0, 0, 0))

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
                    pg.draw.line(screen, fg, (x, y), (x + cell_width, y))
                if Direction.W not in dir:
                    pg.draw.line(screen, fg, (x, y), (x, y + cell_height))
                x += cell_width
            x = start_x
            y += cell_height
        end_x = start_x + self._grid_width * cell_width
        end_y = start_y + self._grid_height * cell_height
        pg.draw.line(screen, fg, (end_x, start_y), (end_x, end_y))
        pg.draw.line(screen, fg, (start_x, end_y), (end_x, end_y))

        # self._player = pg.draw.rect(self._screen, (255, 0, 0), self._player)


def main() -> int:
    game_loop = GameLoop()
    return game_loop.execute()
