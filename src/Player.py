from typing import Literal
import pygame
import Tiled_utils
import gameDevUtils
from Bullet import Bullet
from copy import copy


class Player(gameDevUtils.AnimatedEntity):
    yRemoveLimit = 512

    walkingAnimation = gameDevUtils.Animation(
        *gameDevUtils.loadSpritesheet(
            "./assets/default/player/walking.png",
            (32, 36),
            6,
            [150, 75, 50, 150, 75, 50],
        )
    )
    waitingAnimation = gameDevUtils.Animation(
        gameDevUtils.Frame(pygame.image.load("./assets/default/player/waiting.png"))
    )
    speed = 2
    cooldown = 600

    def __init__(
        self,
        pos: tuple[int, int],
        ground: Tiled_utils.TileGroup,
        ocean: Tiled_utils.TileGroup,
        side: Literal["left", "right"],
        *groups: pygame.sprite.Group | pygame.sprite.GroupSingle
    ) -> None:
        super().__init__(
            pos,
            [Player.waitingAnimation.copy(), Player.walkingAnimation.copy()],
            *groups
        )
        self.speedX, self.speedY = 0, 0
        if side == "left":
            self.previous_speedX = 1
        else:
            self.previous_speedX = -1
        self.lastTimeShooted = 0

        self.side = side

        self.isdead = False
        self.istouchingGround = True
        self.iswalking = False

        self.ground = ground.copy()
        self.ocean = ocean.copy()
        self.myBullets = pygame.sprite.Group()

    def handle_input(self, bulletGroup: pygame.sprite.Group, ct):
        keys = pygame.key.get_pressed()
        if not (self.isdead):
            if self.side == "left":
                if keys[pygame.K_a]:
                    self.previous_speedX = self.speedX
                    self.speedX = -1
                    self.iswalking = True

                elif keys[pygame.K_d]:
                    self.previous_speedX = self.speedX
                    self.speedX = 1
                    self.iswalking = True

                else:
                    self.speedX = 0
                    self.iswalking = False

                if keys[pygame.K_w]:
                    self.jump(15)

                if keys[pygame.K_x]:
                    self.shoot(self.previous_speedX, ct, bulletGroup, self.myBullets)

    def update(self, bullets: pygame.sprite.Group):
        if self.rect.topleft[1] >= Player.yRemoveLimit:
            self.kill()

        if not (self.speedY >= 32):
            self.speedY += 1

        if not (self.istouchingGround):
            self.animations[1].frameOn = 0

            if self.previous_speedX == -1:
                self.image = pygame.transform.flip(
                    self.animations[0].current, True, False
                )
            else:
                self.image = self.animations[0].current

        elif self.speedX == -1:
            self.image = pygame.transform.flip(self.animations[1].current, True, False)

        elif self.speedX == 1:
            self.image = self.animations[1].current
        else:
            self.animations[1].frameOn = 0

            if self.previous_speedX == -1:
                self.image = pygame.transform.flip(
                    self.animations[0].current, True, False
                )
            else:
                self.image = self.animations[0].current

        for i in range(Player.speed):
            if not (self.isdead):
                self.rect = self.rect.move(self.speedX, 0)

            if pygame.sprite.spritecollideany(self, self.ground, None):
                self.stepBack(True, False)

        self.rect = self.rect.move(0, self.speedY)

        if pygame.sprite.spritecollideany(self, self.ground, None):
            self.stepBack(False, True)
            self.speedY = 0
            self.istouchingGround = True
        else:
            self.istouchingGround = False

        if pygame.sprite.spritecollideany(self, self.ocean, None):
            self.die()

        enemyBullets = bullets.copy()
        enemyBullets.remove(self.myBullets.sprites())

        if enemyBullets.sprites():
            if pygame.sprite.spritecollideany(self, enemyBullets.sprites(), None):
                self.die()

    def jump(self, speed):
        if self.istouchingGround:
            self.speedY = -speed
            self.istouchingGround = False

    def shoot(self, speedX: int, ct, *groups):
        if (
            ct - self.lastTimeShooted >= Player.cooldown
            and len(self.myBullets.sprites()) < 3
        ):
            self.lastTimeShooted = ct
            if self.previous_speedX == 1:
                Bullet(
                    (self.rect.midright[0] + 8, self.rect.midright[1] + 4),
                    speedX,
                    *groups
                )
            elif self.previous_speedX == -1:
                Bullet(
                    (self.rect.midleft[0] - 8, self.rect.midleft[1] + 4),
                    speedX,
                    *groups
                )

    def die(self):
        self.istouchingGround = True
        self.jump(15)
        self.isdead = True
        self.ocean.empty()
        self.ground.empty()

    def stepBack(self, x: bool, y: bool):
        if x and y:
            self.rect = self.rect.move(-self.speedX, -self.speedY)
        elif x:
            self.rect = self.rect.move(-self.speedX, 0)
        elif y:
            self.rect = self.rect.move(0, -self.speedY)
