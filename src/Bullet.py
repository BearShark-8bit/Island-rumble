from typing import Any, Literal
import Pygame_utils as utils
import pygame
import random

from Pygame_utils import Animation


class Bullet(utils.AnimatedEntity):
    flyingAnimation = Animation(
        *utils.loadSpritesheet(
            "./assets/default/bullet/bullet.png", (32, 32), 2, [700, 700]
        )
    )

    xRemoveLimit = (-32, 864)
    speed = 3

    def __init__(self, pos: tuple[int, int], speedX: Literal[-1, 1], *groups) -> None:
        super().__init__(pos, [Bullet.flyingAnimation], *groups)
        self.speedX = speedX

    def update(self) -> None:
        if self.speedX == 0:
            self.kill()

        if self.speedX == -1:
            self.image = pygame.transform.flip(self.animations[0].current, True, False)

        elif self.speedX == 1:
            self.image = self.animations[0].current

        for i in range(Bullet.speed):
            self.rect = self.rect.move(self.speedX, 0)

        if (
            self.rect.topleft[0] > Bullet.xRemoveLimit[1]
            or self.rect.topleft[0] < Bullet.xRemoveLimit[0]
        ):
            self.kill()
