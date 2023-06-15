import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], image: pygame.Surface) -> None:
        super().__init__()

        self.image = image
        self.rect = image.get_rect(bottomleft=pos)
        self.rect.bottomleft = (
            self.rect.bottomleft[0] - self.rect.size[0] / 2,
            self.rect.bottomleft[1],
        )

    def update():
        pass

    def updateAnimation(*args):
        pass
