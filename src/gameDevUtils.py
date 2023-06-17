import pygame
from copy import copy


class Frame:
    """The `Frame` class represents a single frame of an animation with an image, rectangle, and duration."""

    def __init__(self, image: pygame.Surface, duration: int = 0) -> None:
        self.image = image
        self.rect = image.get_rect()
        self.duration = duration


class Animation:
    def __init__(self, *frames: Frame) -> None:
        self.lastUpdateTime: int = 0
        self.frameOn: int = 0
        self.frames: list[Frame] = frames
        self.current = frames[0].image

    def updateAnimation(self, ct: int) -> None:
        if ct - self.lastUpdateTime >= self.frames[self.frameOn].duration:
            self.frameOn += 1
            if self.frameOn >= len(self.frames):
                self.frameOn = 0
            self.lastUpdateTime = ct
            self.current = self.frames[self.frameOn].image

    def copy(self):
        return copy(self)


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], image: pygame.Surface, *groups) -> None:
        super().__init__(*groups)

        self.image = image
        self.rect = self.image.get_rect(center=pos)


class AnimatedEntity(Entity):
    def __init__(
        self, pos: tuple[int, int], animations: list[Animation], *groups
    ) -> None:
        self.animations = animations
        super().__init__(pos, animations[0].current, *groups)

    def updateAnimation(self, ct: int):
        for animation in self.animations:
            animation.updateAnimation(ct)


class AnimatedEntityGroup(pygame.sprite.Group):
    def __init__(self, *sprites: list[AnimatedEntity]) -> None:
        super().__init__(*sprites)

    def updateAnimation(self, ct):
        entity: AnimatedEntity
        for entity in self.sprites():
            if isinstance(entity, AnimatedEntity):
                entity.updateAnimation(ct)


def loadSpritesheet(
    filename: str, frameSize: tuple[int, int], rows: int, durationsMs: list[int]
) -> list[Frame]:
    """
    @brief Load spritesheet and return list of Frames. This is a convenience function for loading spritesheet and creating a list of Frame objects.
    @param filename Name of the file to load. Must be a path to an image file
    @param frameSize Tuple of x and y dimensions of each frame
    @param rows Number
    @param durationsMs
    """
    frameList: list[Frame] = []
    spritesheet = pygame.image.load(filename)
    for i in range(rows):
        frameList.append(
            Frame(
                spritesheet.subsurface(pygame.Rect(i * frameSize[0], 0, *frameSize)),
                durationsMs[i],
            )
        )

    return frameList


def text(
    surf: pygame.Surface,
    text: str,
    size: int,
    color: tuple,
    antialias: bool,
    **rectkvargs
):
    font = pygame.font.SysFont(None, size)
    img = font.render(text, antialias, color)
    rect = img.get_rect(**rectkvargs)
    surf.blit(img, rect)
