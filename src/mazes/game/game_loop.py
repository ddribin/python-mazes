import logging

import pygame as pg

from .game_maze import GameMaze


class GameLoop:
    def __init__(self) -> None:
        self._running = True
        self.width = 800
        self.height = 600
        self.logger = logging.getLogger(__name__)

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
                self.logger.info("FPS: %f", fps)

        pg.quit()
        return 0

    def init(self) -> None:
        self._player = pg.Rect((300, 250, 50, 50))
        self._maze = GameMaze(24 * 3 // 2, 18 * 3 // 2, self.width, self.height, 20, 20)
        self._step_timer: int | None = None
        self._reset_key_down = False
        self._jump_key_down = False

    def update(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False

        self._maze.update()

        key = pg.key.get_pressed()
        old_reset_key_down = self._reset_key_down
        self._reset_key_down = key[pg.K_r]
        if not old_reset_key_down and self._reset_key_down:
            self._maze.reset()

        if key[pg.K_SPACE]:
            self._maze.generation_speed = 1
        else:
            self._maze.generation_speed = 0

        old_jump_key_down = self._jump_key_down
        self._jump_key_down = key[pg.K_j]
        if not old_jump_key_down and self._jump_key_down:
            self._maze.run_to_completion()
        if key[pg.K_RIGHT]:
            self.tick_single_step_timer()
        else:
            self._step_timer = None
        if key[pg.K_q]:
            self._running = False

    def tick_single_step_timer(self):
        if self._step_timer is None:
            self._step_timer = 60
            self._maze.single_step()
        else:
            if self._step_timer == 0:
                self._maze.single_step()
                self._step_timer = 5
            else:
                self._step_timer -= 1

    def draw(self) -> None:
        screen = self._screen
        screen.fill((238, 232, 213))

        self._maze.draw(screen)


def main() -> int:
    # logging.basicConfig(level=logging.DEBUG)
    game_loop = GameLoop()
    return game_loop.execute()
