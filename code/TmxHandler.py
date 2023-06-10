import Tile
import pygame
from pytmx import TiledMap


def loadTileGroup(filename: str, TileSize: tuple) -> pygame.sprite.Group:
    tmx_data = TiledMap(filename)
    output = pygame.sprite.Group()
    for layer_index, layer in enumerate(tmx_data.layers):
        for x, y, imageTuple in layer.tiles():
            props = tmx_data.get_tile_properties(x, y, layer_index)
            image = pygame.image.load(imageTuple[0])

            if props["frames"]:
                frames = []
                for frame in props["frames"]:
                    image = pygame.image.load(
                        tmx_data.get_tile_image_by_gid(frame.gid)[0]
                    )
                    frames.append(Tile.Frame(image, frame.duration))
                output.add(
                    Tile.AnimatedVisibleTile(
                        (x * TileSize[0], y * TileSize[1]), frames, props
                    )
                )
            else:
                output.add(
                    Tile.VisibleTile((x * TileSize[0], y * TileSize[1]), image, props)
                )

    return output
