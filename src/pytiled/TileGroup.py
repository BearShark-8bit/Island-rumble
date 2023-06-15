import pygame
from typing import Literal
from AnimatedTile import AnimatedTile


class TileGroup(pygame.sprite.Group):
    """The TileGroup class is a subclass of pygame.sprite.Group that allows searching for sprites based on
    their properties and layer properties."""

    def __init__(self, *sprites) -> None:
        super().__init__(*sprites)

    def search_by_props(self, key: Literal["id", "type", "frames"], value="if"):
        """
        This function searches for sprites in a TileGroup based on their properties, such as id, type, or
        frames.
        """
        filteredGroup = TileGroup()
        for sprite in self.sprites():
            if sprite.props[key] == value:
                filteredGroup.add(sprite)
            elif sprite.props[key] and value == "if":
                filteredGroup.add(sprite)
        return filteredGroup

    def search_by_layerProps(
        self,
        key: Literal["name", "opacity", "visible", "data", "properties"],
        value="if",
    ):
        """
        This function searches for sprites in a TileGroup based on their layer properties matching a given
        key-value pair.
        """
        filteredGroup = TileGroup()
        for sprite in self.sprites():
            if sprite.layerProps[key] == value:
                filteredGroup.add(sprite)
            elif sprite.layerProps[key] and value == "if":
                filteredGroup.add(sprite)
        return filteredGroup

    def updateAnimation(self, ct):
        for tile in self.sprites():
            if isinstance(tile, AnimatedTile):
                tile.updateAnimation(ct)
