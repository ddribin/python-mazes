import logging

import pygame as pg

from .game_maze import GameMaze


class InputButton:
    def __init__(self, key) -> None:
        self._key = key
        self._key_down = False

    def update(self) -> bool:
        """
        Return `True` if key is down
        """
        key = pg.key.get_pressed()
        key_down = key[self._key]
        trigger = False
        if key_down and not self._key_down:
            trigger = True
        self._key_down = key_down
        return trigger


class RepeatingInputButton:
    def __init__(self, key) -> None:
        self._key = key
        self._key_down = False
        self._timer: int | None = None

    def update(self) -> bool:
        """
        Return `True` if key is down
        """
        keys = pg.key.get_pressed()
        key_down = keys[self._key]
        if key_down:
            return self._tick_timer()
        else:
            self._timer = None
            return False

    def _tick_timer(self):
        trigger = False
        if self._timer is None:
            self._timer = 60
            trigger = True
        else:
            if self._timer == 0:
                trigger = True
                self._timer = 5
            else:
                self._timer -= 1
        return trigger


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
                self.logger.debug("FPS: %f", fps)

        pg.quit()
        return 0

    def init(self) -> None:
        self._player = pg.Rect((300, 250, 50, 50))
        self._maze = GameMaze(24 * 3 // 2, 18 * 3 // 2, self.width, self.height, 20, 20)
        self._reset_button = InputButton(pg.K_r)
        self._jump_button = InputButton(pg.K_j)
        self._next_button = RepeatingInputButton(pg.K_RIGHT)
        self._prev_button = RepeatingInputButton(pg.K_LEFT)
        self._quit_button = InputButton(pg.K_q)

    def update(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False

        self._maze.update()

        key = pg.key.get_pressed()
        if self._reset_button.update():
            self._maze.reset()

        if key[pg.K_SPACE]:
            self._maze.generation_speed = 1
        else:
            self._maze.generation_speed = 0

        if self._jump_button.update():
            self._maze.run_to_completion()
        if self._next_button.update():
            self._maze.single_step_forward()
        if self._prev_button.update():
            self._maze.single_step_backward()
        if self._quit_button.update():
            self._running = False

    def draw(self) -> None:
        screen = self._screen
        screen.fill((238, 232, 213))

        self._maze.draw(screen)


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    game_loop = GameLoop()
    return game_loop.execute()
