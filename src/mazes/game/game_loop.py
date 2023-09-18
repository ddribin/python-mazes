import logging

import pygame as pg

from .game_maze import GameMaze


class ButtonInput:
    def __init__(self) -> None:
        self._is_down = False
        self._triggered = False

    @property
    def is_triggered(self) -> bool:
        return self._triggered

    def __bool__(self) -> bool:
        return self._triggered

    def update(self, is_down: bool) -> None:
        self._triggered = is_down and not self._is_down
        self._is_down = is_down


class RepeatingButtonInput:
    def __init__(self, delay=60, rate=5) -> None:
        self._delay = delay
        self._rate = rate
        self._triggered = False
        self._timer: int | None = None

    @property
    def is_triggered(self) -> bool:
        return self._triggered

    def __bool__(self) -> bool:
        return self._triggered

    def update(self, is_down: bool) -> None:
        if is_down:
            self._triggered = self._tick_timer()
        else:
            self._timer = None
            self._triggered = False

    def _tick_timer(self) -> bool:
        if self._timer is None:
            self._timer = self._delay
            return True
        else:
            if self._timer == 0:
                self._triggered = True
                self._timer = self._rate
                return True
            else:
                self._timer -= 1
                return False


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
        self._reset_key = ButtonInput()
        self._quit_key = ButtonInput()
        self._jump_key = ButtonInput()
        self._next_key = RepeatingButtonInput()
        self._prev_key = RepeatingButtonInput()

    def update(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False

        self._maze.update()

        keys = pg.key.get_pressed()
        self._reset_key.update(keys[pg.K_r])
        self._jump_key.update(keys[pg.K_RETURN])
        self._quit_key.update(keys[pg.K_q])
        self._next_key.update(keys[pg.K_f] or keys[pg.K_RIGHT])
        self._prev_key.update(keys[pg.K_s] or keys[pg.K_LEFT])

        if self._reset_key:
            self._maze.reset()

        if keys[pg.K_SPACE]:
            self._maze.generation_speed = 1
        else:
            self._maze.generation_speed = 0

        if self._jump_key:
            self._maze.run_to_completion()
        if self._next_key:
            self._maze.single_step_forward()
        if self._prev_key:
            self._maze.single_step_backward()
        if self._quit_key:
            self._running = False

    def draw(self) -> None:
        screen = self._screen
        screen.fill((238, 232, 213))

        self._maze.draw(screen)


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    game_loop = GameLoop()
    return game_loop.execute()
