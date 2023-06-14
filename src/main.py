import sys
import pygame
from loadTileGroup import loadTileGroup
from pytmx.util_pygame import load_pygame


class Game:
    fps = 60
    screenWidth, screenHeight = 864, 512
    tileSize = (32, 32)
    margin = 40
    ms_per_update = 1000 / fps

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(
            (
                Game.screenWidth + Game.margin,
                Game.screenHeight + Game.margin,
            ),
            pygame.RESIZABLE,
        )
        pygame.display.set_caption("Island rumble")
        pygame.display.set_icon(pygame.image.load("./assets/icon.png"))

        self.renderSurface = pygame.Surface((Game.screenWidth, Game.screenHeight))
        self.clock = pygame.time.Clock()

        self.tiles = loadTileGroup(load_pygame("./data/tmx/tmx.tmx"), (Game.tileSize))

        self.game = True

    def getCurrentTime(self):
        return pygame.time.get_ticks()

    def _text(
        self,
        surf: pygame.Surface,
        text: str,
        pos: tuple,
        size: int = 24,
        color: tuple = (0, 0, 0),
        antialias=False,
    ):
        font = pygame.font.SysFont(None, size)
        img = font.render(text, antialias, color)
        surf.blit(img, pos)

    def _handleInput(self):
        pass

    def _update(self):
        pass

    def _render(self, extrapolation: float):
        self.renderSurface.fill((135, 206, 235))
        self.screen.fill((0, 0, 0))

        self.tiles.update(self.getCurrentTime())
        self.tiles.draw(self.renderSurface)

        self._text(
            self.renderSurface,
            "FPS: " + str(int(self.clock.get_fps())),
            pygame.Surface((48, 0)).get_rect(topright=(Game.screenWidth, 3)).topleft,
            18,
            antialias=False,
        )

        if self.screen.get_flags() == -2130706416:
            self._text(
                self.screen,
                "Press key F11 to toggle fullscreen",
                (0, 2),
                16,
                (255, 255, 255),
                False,
            )

        self.screen.blit(
            self.renderSurface,
            self.renderSurface.get_rect(
                center=(
                    self.screen.get_size()[0] / 2,
                    self.screen.get_size()[1] / 2,
                )
            ),
        )

        pygame.display.update()

    def loop(self):
        previous = self.getCurrentTime()
        lag = 0.0
        while self.game:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.game = False
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_F11:
                        if self.screen.get_flags() != -2130706416:
                            self.screen = pygame.display.set_mode(
                                (0, 0), pygame.FULLSCREEN
                            )
                        else:
                            self.screen = pygame.display.set_mode(
                                (
                                    Game.screenWidth + Game.margin,
                                    Game.screenHeight + Game.margin,
                                ),
                                pygame.RESIZABLE,
                            )
                    if e.key == pygame.K_ESCAPE:
                        self.screen = pygame.display.set_mode(
                            (
                                Game.screenWidth + Game.margin,
                                Game.screenHeight + Game.margin,
                            ),
                            pygame.RESIZABLE,
                        )

            current = self.getCurrentTime()
            elapsed = current - previous
            previous = current
            lag += elapsed

            self._handleInput()

            while lag >= self.ms_per_update:
                self._update()
                lag -= self.ms_per_update

            self.tiles.update(current)

            self._render(lag / self.ms_per_update)

            self.clock.tick(Game.fps)


pygame.init()
Game().loop()
