from typing import Literal
from Object import Object


class ObjectList(list[Object]):
    """The ObjectList class allows for searching objects based on their properties."""

    def __init__(self, *args: Object):
        super().__init__(args)

    def search_by_props(
        self: list[Object],
        key: Literal[
            "name",
            "type",
            "x",
            "y",
            "width",
            "height",
            "rotation",
            "gid",
            "visible",
            "image",
            "properties",
        ],
        value: any = "if",
    ):
        """
        This function searches for objects in a ObjectList based on their properties, such as id or type.
        """
        filteredList = ObjectList()
        for object in self:
            if object.props[key] == value:
                filteredList.append(object)
            elif object.props[key] and value == "if":
                filteredList.append(object)
        return filteredList

    # def search_by_layerProps(self: list[Object], key: Literal[], value="if"):
    #     """
    #     This function searches for objects in a ObjectList based on their layer properties matching a given
    #     key-value pair.
    #     """
    #     filteredList = ObjectList()
    #     for object in self:
    #         if object.layerProps[key] == value:
    #             filteredList.append(object)
    #         elif object.layerProps[key] and value == "if":
    #             filteredList.append(object)
    #     return filteredList
