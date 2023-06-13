from VisibleTile import VisibleTile
from structures import Frame


class AnimatedTile(VisibleTile):
    def __init__(
        self, pos: tuple, frames: list[Frame], props: dict, layerProps: dict
    ) -> None:
        super().__init__(pos, frames[0].image, props, layerProps)
        self._lastUpdateTime = 0
        self._frameOn = 0
        self._frames = frames

    def update(self, ct) -> None:
        if ct - self._lastUpdateTime >= self._frames[self._frameOn].duration:
            self._frameOn += 1
            if self._frameOn >= len(self._frames):
                self._frameOn = 0
            self._lastUpdateTime = ct
            self.image = self._frames[self._frameOn].image
