import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(
        self, x: int, y: int, width: int, height: int, props: dict, layerProps: dict
    ) -> None:
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.props = props
        self.layerProps = layerProps

    def pos(self) -> tuple:
        return self.rect.topleft
