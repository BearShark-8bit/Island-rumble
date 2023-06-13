import pygame
from typing import Literal


class TileGroup(pygame.sprite.Group):
    def __init__(self, *sprites) -> None:
        super().__init__(*sprites)

    def search_by_props(self, key: Literal["id", "type", "frames"], value="if"):
        filteredGroup = TileGroup()
        for sprite in self.sprites():
            if sprite.props[key] == value:
                filteredGroup.add(sprite)
            elif sprite.props[key] and value == "if":
                filteredGroup.add(sprite)
        return filteredGroup

    def search_by_layerProps(self, key: Literal["id", "name", "visible"], value="if"):
        filteredGroup = TileGroup()
        for sprite in self.sprites():
            if sprite.layerProps[key] == value:
                filteredGroup.add(sprite)
            elif sprite.layerProps[key] and value == "if":
                filteredGroup.add(sprite)
        return filteredGroup
