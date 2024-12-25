"""
This module contains the Bullet class, which is a subclass of AnimatedEntity.
"""

from pygame import transform
from bearsharkutils.pygameutils.datastructures import AnimatedEntity, Animation
from bearsharkutils.pygameutils import loadSpritesheet

class Bullet(AnimatedEntity):
    """class for the bullets that the players shoot"""
    FLYINGANIMATION = Animation(
        *loadSpritesheet("./assets/default/bullet/bullet.png", (32, 32), 2, [700, 700])
    )

    XLIMIT = (-32, 864)
    SPEED = 5

    def __init__(self, pos: tuple[int, int], speed_x, *groups) -> None:
        super().__init__(pos, [Bullet.FLYINGANIMATION.copy()], *groups)
        self.speed_x = speed_x

    def update(self, *args, **kwargs) -> None:
        if self.speed_x == 0:
            self.kill()

        if self.speed_x == -1:
            self.image = transform.flip(self.animations[0].current, True, False)

        elif self.speed_x == 1:
            self.image = self.animations[0].current

        for _ in range(Bullet.SPEED):
            self.rect = self.rect.move(self.speed_x, 0)

        if (
            self.rect.topleft[0] > Bullet.XLIMIT[1]
            or self.rect.topleft[0] < Bullet.XLIMIT[0]
        ):
            self.kill()
