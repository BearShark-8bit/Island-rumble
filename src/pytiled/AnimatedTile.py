import pygame
from VisibleTile import VisibleTile
import utils


class AnimatedTile(VisibleTile):
    """The AnimatedTile class is a subclass of VisibleTile that updates its image based on a list of frames
    and their durations."""

    def __init__(
        self,
        pos: tuple[int, int],
        frames: list[utils.Frame],
        props: dict,
        layerProps: dict,
        *groups: pygame.sprite.Group
    ) -> None:
        super().__init__(pos, frames[0].image, props, layerProps, *groups)
        self.animation = utils.Animation(*frames)

    def updateAnimation(self, ct: int) -> None:
        self.animation.updateAnimation(ct)
        self.image = self.animation.current
