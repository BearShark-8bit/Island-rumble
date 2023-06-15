import pygame
from Entity import Entity
import utils


class Player(Entity):
    def __init__(
        self, pos: tuple[int, int], image: pygame.Surface, walking: list[utils.Frame]
    ) -> None:
        super().__init__(pos, image)
        self.walkingAnim = utils.Animation(walking)
        self.waitingImg = image
        self.speedX, self.speedY = 0, 0
        self.iswalking = False
        self.previous_speedX = 0
        self.speed = 2

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

    def update(self):
        if self.speedX == -1:
            self.image = pygame.transform.flip(self.walkingAnim.current, True, False)

        elif self.speedX == 1:
            self.image = self.walkingAnim.current
        else:
            if self.previous_speedX == -1:
                self.image = pygame.transform.flip(self.waitingImg, True, False)
            else:
                self.image = self.waitingImg
        for i in range(self.speed):
            self.rect = self.rect.move(self.speedX, self.speedY)

    def updateAnimation(self, ct: int):
        self.walkingAnim.updateAnimation(ct)
