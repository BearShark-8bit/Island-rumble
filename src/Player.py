import pygame
import pytiled
import utils


class Player(utils.AnimatedEntity):
    walkingAnimation = utils.Animation(
        *utils.loadSpritesheet(
            "./assets/default/player/walking.png",
            (32, 36),
            6,
            [300, 150, 100, 300, 150, 100],
        )
    )
    waitingAnimation = utils.Animation(
        utils.Frame(pygame.image.load("./assets/default/player/waiting.png"))
    )

    def __init__(
        self,
        pos: tuple[int, int],
        ground: list[pytiled.VisibleTile],
        *groups: pygame.sprite.Group | pygame.sprite.GroupSingle
    ) -> None:
        super().__init__(
            pos, [Player.waitingAnimation, Player.walkingAnimation], *groups
        )
        self.speedX, self.speedY = 0, 0
        self.iswalking = False
        self.isTouchingGround = True
        self.previous_speedX = 0
        self.speed = 2
        self.ground = ground

    def handle_input(self):
        keys = pygame.key.get_pressed()

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
            self.jump(10)

    # TODO: add gravitation
    def update(self):
        print(self.speedY)
        if not (self.speedY >= 32):
            self.speedY += 1

        if self.speedX == -1:
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

        for i in range(self.speed):
            self.rect = self.rect.move(self.speedX, 0)
            for tile in self.ground:
                if self.rect.colliderect(tile.rect):
                    self.stepBack(True, False)
            self.rect = self.rect.move(0, self.speedY)
            for tile in self.ground:
                if self.rect.colliderect(tile.rect):
                    self.stepBack(False, True)
                    self.speedY = 0
                    self.isTouchingGround = True

    def jump(self, speed):
        if self.isTouchingGround:
            self.speedY = -speed
            self.isTouchingGround = False

    def stepBack(self, x: bool, y: bool):
        if x and y:
            self.rect = self.rect.move(-self.speedX, -self.speedY)
        elif x:
            self.rect = self.rect.move(-self.speedX, 0)
        elif y:
            self.rect = self.rect.move(0, -self.speedY)
