import pytiles
import pytmx


def loadTileGroup(tiledMap: pytmx.TiledMap, tileSize: tuple) -> pytiles.TileGroup:
    tiledMap = tiledMap
    tileGroup = pytiles.TileGroup()
    for layer_index, layer in enumerate(tiledMap.layers):
        layerProps = vars(layer)
        for x, y, image in layer.tiles():
            props = tiledMap.get_tile_properties(x, y, layer_index)

            if props["frames"]:
                frames = []
                for frame in props["frames"]:
                    frames.append(
                        pytiles.Frame(
                            tiledMap.get_tile_image_by_gid(frame.gid), frame.duration
                        )
                    )
                tileGroup.add(
                    pytiles.AnimatedVisibleTile(
                        (x * tileSize[0], y * tileSize[1]), frames, props, layerProps
                    )
                )
            else:
                tileGroup.add(
                    pytiles.VisibleTile(
                        (x * tileSize[0], y * tileSize[1]), image, props, layerProps
                    )
                )

    return tileGroup
