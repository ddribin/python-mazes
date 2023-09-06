import math

import pygame as pg


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
        self._padding = 40
        self._cell_width = math.floor((self.width - self._padding) / self._grid_width)
        self._cell_height = math.floor(
            (self.height - self._padding) / self._grid_height
        )

    def update(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False

        self._player.width = 50
        self._player.height = 50
        key = pg.key.get_pressed()
        speed = 5
        if key[pg.K_j]:
            self._player.move_ip(-speed, 0)
        elif key[pg.K_l]:
            self._player.move_ip(speed, 0)
        if key[pg.K_i]:
            self._player.move_ip(0, -speed)
        elif key[pg.K_k]:
            self._player.move_ip(0, speed)
        if key[pg.K_r]:
            self._player = pg.Rect((300, 250, 50, 50))
        if key[pg.K_q]:
            self._running = False

    def draw(self) -> None:
        screen = self._screen
        screen.fill((0, 0, 0))

        start_x, start_y = (self._padding / 2, self._padding / 2)
        x, y = (start_x, start_y)
        fg = "white"
        cell_width = self._cell_width
        cell_height = self._cell_height
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                pg.draw.line(screen, fg, (x, y), (x + cell_width, y))
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
