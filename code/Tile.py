import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, props: dict) -> None:
        super().__init__()
        self._rect = pygame.Rect(x, y, width, height)
        self._props = props

    def rect(self) -> pygame.Rect:
        return self._rect

    def pos(self) -> tuple:
        return self._rect.topleft

    def props(self) -> dict:
        return self._props


class VisibleTile(Tile):
    def __init__(self, pos: tuple, image: pygame.Surface, props: dict) -> None:
        super().__init__(*pos, *image.get_rect().size, props)
        self.image = image


class Frame:
    def __init__(self, image: pygame.Surface, duration: float) -> None:
        self.image = image
        self.rect = image.get_rect()
        self.duration = duration


class AnimatedVisibleTile(VisibleTile):
    def __init__(self, pos: tuple, frames: list[Frame], props: dict) -> None:
        super().__init__(pos, frames[0].image, props)
        self._lastUpdateTime = 0
        self._frameOn = 0
        self._frames = frames

    def update(self, ct) -> None:
        if ct - self._lastUpdateTime >= self._frames[self._frameOn].duration:
            self._frameOn += 1
            self._lastUpdateTime = ct
            self.image = self._frames[self._frameOn].image
