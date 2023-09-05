import pygame


class GameLoop:
    def __init__(self) -> None:
        self._running = True
        self.width = 800
        self.height = 600

    def execute(self) -> int:
        pygame.init()
        pygame.display.set_caption("Maze Game")
        self._screen = pygame.display.set_mode((self.width, self.height), vsync=True)
        self.init()

        # Main loop
        while self._running:
            self.update()

            self._screen.fill((0, 0, 0))
            self.draw()
            pygame.display.update()

        pygame.quit()
        return 0

    def init(self) -> None:
        self._player = pygame.Rect((300, 250, 50, 50))

    def update(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

        self._player.width = 50
        self._player.height = 50
        key = pygame.key.get_pressed()
        if key[pygame.K_j]:
            self._player.move_ip(-1, 0)
        elif key[pygame.K_l]:
            self._player.move_ip(1, 0)
        if key[pygame.K_i]:
            self._player.move_ip(0, -1)
        elif key[pygame.K_k]:
            self._player.move_ip(0, 1)
        if key[pygame.K_r]:
            self._player = pygame.Rect((300, 250, 50, 50))
        if key[pygame.K_q]:
            self._running = False

    def draw(self) -> None:
        self._player = pygame.draw.rect(self._screen, (255, 0, 0), self._player)


def main() -> int:
    game_loop = GameLoop()
    return game_loop.execute()
