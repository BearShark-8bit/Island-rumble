import pygame


class Frame:
    def __init__(self, image: pygame.Surface, duration: float) -> None:
        self.image = image
        self.rect = image.get_rect()
        self.duration = duration
