import logging
from dataclasses import dataclass

import pygame as pg

from . import utils
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


@dataclass(slots=True)
class JoystickState:
    a_button: bool = False
    b_button: bool = False
    x_button: bool = False
    y_button: bool = False
    l_button: bool = False
    r_button: bool = False
    plus_button: bool = False
    dpad_left: bool = False
    dpad_right: bool = False
    dpad_up: bool = False
    dpad_down: bool = False
    lstick_horizontal: float = 0.0
    lstick_vertical: float = 0.0


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
        pg.joystick.init()
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

        self._reset_button = ButtonInput()
        self._jump_button = ButtonInput()
        self._next_button = RepeatingButtonInput()
        self._prev_button = RepeatingButtonInput()
        self._joystick_state = JoystickState()
        self._joysticks: dict[int, pg.joystick.JoystickType] = {}
        self._max_analog_speed = 100.0 ** (1.0 / 4)

    def update(self) -> None:
        joystick_state = self._joystick_state

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False

            if event.type == pg.JOYBUTTONDOWN or event.type == pg.JOYBUTTONUP:
                down = event.type == pg.JOYBUTTONDOWN
                if event.button == 0:
                    joystick_state.a_button = down
                elif event.button == 1:
                    joystick_state.b_button = down
                elif event.button == 2:
                    joystick_state.x_button = down
                elif event.button == 3:
                    joystick_state.y_button = down
                elif event.button == 6:
                    joystick_state.plus_button = down
                elif event.button == 9:
                    joystick_state.l_button = down
                elif event.button == 10:
                    joystick_state.r_button = down
                elif event.button == 13:
                    joystick_state.dpad_left = down
                elif event.button == 14:
                    joystick_state.dpad_right = down
                elif event.button == 11:
                    joystick_state.dpad_up = down
                elif event.button == 12:
                    joystick_state.dpad_down = down

            if event.type == pg.JOYAXISMOTION:
                if event.axis == 0:
                    joystick_state.lstick_horizontal = event.value
                elif event.axis == 1:
                    joystick_state.lstick_vertical = event.value

            if event.type == pg.JOYDEVICEADDED:
                joy = pg.joystick.Joystick(event.device_index)
                self._joysticks[joy.get_instance_id()] = joy
                self.logger.info("Joystick %d connected", joy.get_instance_id())

            if event.type == pg.JOYDEVICEREMOVED:
                if event.instance_id in self._joysticks:
                    del self._joysticks[event.instance_id]
                    self.logger.info("Joystick %d disconnected", event.instance_id)
                else:
                    self.logger.error(
                        "Tried to disconnect Joystick %d, "
                        "but couldn't find it in the joystick list",
                        event.instance_id,
                    )

        self._maze.update()

        keys = pg.key.get_pressed()
        self._reset_key.update(keys[pg.K_r])
        self._reset_button.update(joystick_state.plus_button)
        self._jump_key.update(keys[pg.K_RETURN])
        self._jump_button.update(joystick_state.a_button)
        self._quit_key.update(keys[pg.K_q])
        self._next_key.update(keys[pg.K_f] or keys[pg.K_RIGHT])
        self._next_button.update(joystick_state.r_button)
        self._prev_key.update(keys[pg.K_s] or keys[pg.K_LEFT])
        self._prev_button.update(joystick_state.l_button)

        if self._reset_key or self._reset_button:
            self._maze.reset()

        if keys[pg.K_l] or keys[pg.K_SPACE] or joystick_state.dpad_right:
            self._maze.generation_velocity = 100
        elif keys[pg.K_j] or joystick_state.dpad_left:
            self._maze.generation_velocity = -100
        else:
            self.update_analog_speed(joystick_state.lstick_horizontal)
        if self._jump_key or self._jump_button:
            self._maze.run_to_completion()
        if self._next_key or self._next_button:
            self._maze.single_step_forward()
        if self._prev_key or self._prev_button:
            self._maze.single_step_backward()
        if self._quit_key:
            self._running = False

    def update_analog_speed(self, lstick_horizontal: float) -> None:
        dir = utils.fsign(lstick_horizontal)
        speed = abs(lstick_horizontal)
        scaled = 0
        if speed > 0.30:
            remapped_speed = utils.fremap(0.1, 1.0, 0.0, self._max_analog_speed, speed)
            scaled = round(remapped_speed**4.0)
        analog_speed = dir * scaled
        self._maze.generation_velocity = analog_speed

    def draw(self) -> None:
        screen = self._screen
        screen.fill((238, 232, 213))

        self._maze.draw(screen)


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    game_loop = GameLoop()
    return game_loop.execute()
