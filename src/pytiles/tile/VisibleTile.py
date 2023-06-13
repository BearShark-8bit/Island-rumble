import pygame
from Tile import Tile


class VisibleTile(Tile):
    def __init__(
        self, pos: tuple, image: pygame.Surface, props: dict, layerProps: dict
    ) -> None:
        super().__init__(*pos, *image.get_rect().size, props, layerProps)
        self.image = image
