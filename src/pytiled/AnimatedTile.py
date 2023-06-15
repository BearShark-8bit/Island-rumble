from VisibleTile import VisibleTile
import utils


# TODO:use Animation object here
class AnimatedTile(VisibleTile):
    """The AnimatedTile class is a subclass of VisibleTile that updates its image based on a list of frames
    and their durations."""

    def __init__(
        self, pos: tuple, frames: list[utils.Frame], props: dict, layerProps: dict
    ) -> None:
        super().__init__(pos, frames[0].image, props, layerProps)
        self._lastUpdateTime = 0
        self._frameOn = 0
        self._frames = frames

    def updateAnimation(self, ct) -> None:
        if ct - self._lastUpdateTime >= self._frames[self._frameOn].duration:
            self._frameOn += 1
            if self._frameOn >= len(self._frames):
                self._frameOn = 0
            self._lastUpdateTime = ct
            self.image = self._frames[self._frameOn].image
