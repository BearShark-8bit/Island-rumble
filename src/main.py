import json
import math
import sys
import pygame
import tmxhandler
import time
from pytmx.util_pygame import load_pygame


with open("./data/config.json") as config_file:
    config = json.load(config_file)


class Game:
    def __init__(self, config: dict) -> None:
        self.start_time = time.time()
        self.config = config

        self.WIN = pygame.display.set_mode(
            (self.config["SCREEN_WIDTH"], self.config["SCREEN_HEIGHT"])
        )
        self.tiles = tmxhandler.loadTileGroup(
            load_pygame("./data/tmx/tmx.tmx"), (self.config["TILE_SIZE"])
        )
        self.game = True
        self.clock = pygame.time.Clock()

        self.MS_PER_UPDATE = 1000 / self.config["FPS"]

        pygame.display.set_caption("Island rumble")
        pygame.display.set_icon(pygame.image.load("./assets/icon.png"))

    def _update(self):
        pass

    def getCurrentTime(self):
        return pygame.time.get_ticks()

    def _render(self, extrapolation):
        self.WIN.fill((135, 206, 235))

        self.tiles.update(self.getCurrentTime())
        self.tiles.draw(self.WIN)

        self._text("fps: " + str(int(self.clock.get_fps())), (0, 2), 16)

        pygame.display.update()

    def _handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game = False
                pygame.quit()
                sys.exit()

    def _text(
        self,
        text: str,
        pos: tuple,
        size: int = 24,
        color: tuple = (0, 0, 0),
        antialias=False,
    ):
        font = pygame.font.SysFont(None, size)
        img = font.render(text, antialias, color)
        self.WIN.blit(img, pos)

    def loop(self):
        previous = self.getCurrentTime()
        lag = 0.0
        while self.game:
            current = self.getCurrentTime()
            elapsed = current - previous
            previous = current
            lag += elapsed

            self._handleInput()

            while lag >= self.MS_PER_UPDATE:
                self._update()
                lag -= self.MS_PER_UPDATE

            self.tiles.update(current)

            self._render(lag / self.MS_PER_UPDATE)

            self.clock.tick(self.config["FPS"])


pygame.init()
Game(config).loop()
