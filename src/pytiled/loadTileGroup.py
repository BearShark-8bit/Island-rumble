from Tile import Tile
from VisibleTile import VisibleTile
from AnimatedTile import AnimatedTile
from TileGroup import TileGroup
from Frame import Frame


def loadTileGroup(tiledMap, tileSize: tuple) -> TileGroup:
    """
    This function loads a tile group from a Tiled map and returns it.

    :param tiledMap: A TiledMap object, which is a representation of a Tiled map file in Python
    :param tileSize: The tileSize parameter is a tuple that contains the width and height of each tile
    in the tiled map
    :return: an instance of the `TileGroup` class which is an instance of `pygame.sprite.Group` class.
    """
    tiledMap = tiledMap
    tileGroup = TileGroup()
    for layer_index, layer in enumerate(tiledMap.layers):
        layerProps = vars(layer)
        for x, y, image in layer.tiles():
            props = tiledMap.get_tile_properties(x, y, layer_index)

            if props["frames"]:
                frames = []
                for frame in props["frames"]:
                    frames.append(
                        Frame(tiledMap.get_tile_image_by_gid(frame.gid), frame.duration)
                    )
                tileGroup.add(
                    AnimatedTile(
                        (x * tileSize[0], y * tileSize[1]), frames, props, layerProps
                    )
                )
            else:
                tileGroup.add(
                    VisibleTile(
                        (x * tileSize[0], y * tileSize[1]), image, props, layerProps
                    )
                )

    return tileGroup
