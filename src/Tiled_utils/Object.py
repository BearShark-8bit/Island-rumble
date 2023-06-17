import pygame


class Object:
    def __init__(self, x: int, y: int, w: int, h: int, props: dict) -> None:
        self.rect = pygame.Rect(x, y, w, h)
        self.props = props
