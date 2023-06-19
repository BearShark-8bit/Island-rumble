from typing import Literal
from pygame import transform

from mygamedevutils.pygameutils.datastructures import AnimatedEntity, Animation
from mygamedevutils.pygameutils import loadSpritesheet


class Bullet(AnimatedEntity):
    FLYINGANIMATION = Animation(
        *loadSpritesheet("./assets/default/bullet/bullet.png", (32, 32), 2, [700, 700])
    )

    XLIMIT = (-32, 864)
    SPEED = 3

    def __init__(self, pos: tuple[int, int], speedX: Literal[-1, 1], *groups) -> None:
        super().__init__(pos, [Bullet.FLYINGANIMATION.copy()], *groups)
        self.speedX = speedX

    def update(self) -> None:
        if self.speedX == 0:
            self.kill()

        if self.speedX == -1:
            self.image = transform.flip(self.animations[0].current, True, False)

        elif self.speedX == 1:
            self.image = self.animations[0].current

        for i in range(Bullet.SPEED):
            self.rect = self.rect.move(self.speedX, 0)

        if (
            self.rect.topleft[0] > Bullet.XLIMIT[1]
            or self.rect.topleft[0] < Bullet.XLIMIT[0]
        ):
            self.kill()
