from Tile import Tile
from VisibleTile import VisibleTile
from AnimatedTile import AnimatedTile
from TileGroup import TileGroup
from utils import Frame
from ObjectList import ObjectList
from Object import Object
import pytmx


def load(tiledMap: pytmx.TiledMap, tileSize: tuple) -> tuple[TileGroup, ObjectList]:
    tiledMap = tiledMap
    tileGroup = TileGroup()
    objectList = ObjectList()
    tileLayers, objectLayers = [], []

    for layer in tiledMap.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            tileLayers.append(layer)
        elif isinstance(layer, pytmx.TiledObjectGroup):
            objectLayers.append(layer)

    for layer_index, layer in enumerate(tileLayers):
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

    for layer_index, layer in enumerate(objectLayers):
        layerProps = vars(layer)
        for object in layer:
            props = vars(object)

            # if props["frames"]:
            #     frames = []
            #     for frame in props["frames"]:
            #         frames.append(
            #             Frame(tiledMap.get_tile_image_by_gid(frame.gid), frame.duration)
            #         )
            #     tileGroup.add(
            #         AnimatedTile(
            #             (x * tileSize[0], y * tileSize[1]), frames, props, layerProps
            #         )
            #     )
            objectList.append(
                Object(props["x"], props["y"], props["width"], props["height"], props)
            )

    return [tileGroup, objectList]
