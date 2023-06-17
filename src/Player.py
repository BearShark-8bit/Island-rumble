import pygame
import Tiled_utils
import Pygame_utils
from Bullet import Bullet


class Player(Pygame_utils.AnimatedEntity):
    yRemoveLimit = 512

    walkingAnimation = Pygame_utils.Animation(
        *Pygame_utils.loadSpritesheet(
            "./assets/default/player/walking.png",
            (32, 36),
            6,
            [150, 75, 50, 150, 75, 50],
        )
    )
    waitingAnimation = Pygame_utils.Animation(
        Pygame_utils.Frame(pygame.image.load("./assets/default/player/waiting.png"))
    )
    speed = 2
    cooldown = 600

    def __init__(
        self,
        pos: tuple[int, int],
        ground: Tiled_utils.TileGroup,
        ocean: Tiled_utils.TileGroup,
        side,
        *groups: pygame.sprite.Group | pygame.sprite.GroupSingle
    ) -> None:
        super().__init__(
            pos, [Player.waitingAnimation, Player.walkingAnimation], *groups
        )
        self.speedX, self.speedY = 0, 0
        if side == "left":
            self.previous_speedX = 1
        self.lastTimeShooted = 0

        self.isdead = False
        self.isdying = False
        self.istouchingGround = True
        self.iswalking = False

        self.ground = ground
        self.ocean = ocean

    def handle_input(self, bulletGroup: pygame.sprite.Group, ct):
        keys = pygame.key.get_pressed()
        if not (self.isdead):
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
                self.shoot(self.previous_speedX, ct, bulletGroup)

    def update(self):
        if self.rect.topleft[1] >= Player.yRemoveLimit:
            self.kill()

        if self.isdying:
            self.death()
            self.isdying = False

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

        if not (self.isdead):
            if pygame.sprite.spritecollideany(self, self.ocean, None):
                self.isdying = True

    def jump(self, speed):
        if self.istouchingGround:
            self.speedY = -speed
            self.istouchingGround = False

    def shoot(self, speedX: int, ct, *groups):
        if ct - self.lastTimeShooted >= Player.cooldown:
            self.lastTimeShooted = ct
            Bullet((self.rect.midright[0], self.rect.midright[1]), speedX, *groups)

    def death(self):
        self.istouchingGround = True
        self.jump(15)
        self.isdead = True

    def stepBack(self, x: bool, y: bool):
        if x and y:
            self.rect = self.rect.move(-self.speedX, -self.speedY)
        elif x:
            self.rect = self.rect.move(-self.speedX, 0)
        elif y:
            self.rect = self.rect.move(0, -self.speedY)
