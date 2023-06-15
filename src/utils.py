import pygame


class Frame:
    """The `Frame` class represents a single frame of an animation with an image, rectangle, and duration."""

    def __init__(self, image: pygame.Surface, duration: float) -> None:
        self.image = image
        self.rect = image.get_rect()
        self.duration = duration


class Animation:
    def __init__(self, frames: list[Frame]) -> None:
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
    frameList = []
    spritesheet = pygame.image.load(filename)
    for i in range(rows):
        frameList.append(
            Frame(
                spritesheet.subsurface(pygame.Rect(i * frameSize[0], 0, *frameSize)),
                durationsMs[i],
            )
        )

    return frameList
