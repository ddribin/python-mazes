import pygame as pg

from .game_maze import GameMaze


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
        self._maze = GameMaze(24, 18, self.width, self.height, 40, 40)
        self._last_step_down = False

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
        if key[pg.K_RIGHT]:
            if not self._last_step_down:
                self._maze.single_step()
            self._last_step_down = True
        else:
            self._last_step_down = False
        if key[pg.K_q]:
            self._running = False

    def draw(self) -> None:
        screen = self._screen
        screen.fill((255, 255, 255))

        self._maze.draw(screen)


def main() -> int:
    game_loop = GameLoop()
    return game_loop.execute()
