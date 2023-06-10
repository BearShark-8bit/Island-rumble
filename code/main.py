import math
import pygame
import TmxHandler
import time

tiles = TmxHandler.loadTileGroup("./data/tmx/tmx.tmx", (32, 32))


class Game:
    pass


pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 512
TILE_SIZE = 32
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Island rumble")
pygame.display.set_icon(pygame.image.load("./textures/icon.png"))

game = True

WIN.fill((135, 206, 235))

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        game = False
