import pygame
from Tile import Tile


class VisibleTile(Tile):
    """The VisibleTile class is a subclass of Tile that initializes with a position, image, properties, and layer properties."""

    def __init__(
        self,
        pos: tuple,
        image: pygame.Surface,
        props: dict,
        layerProps: dict,
        *groups: pygame.sprite.Group
    ) -> None:
        super().__init__(*pos, *image.get_rect().size, props, layerProps, *groups)
        self.image = image
