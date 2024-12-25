"""Draw text on the screen"""

from dataclasses import dataclass
import pygame


@dataclass
class Text:
    """Text dataclass"""

    text: str
    size: int
    color: tuple[int, int, int] = (255, 255, 255)
    font: str = None


def draw_text(
    surface: pygame.Surface,
    text: Text,
    antialias: bool,
    **rectkvargs,
):
    """Draw text on the screen

    rectkvargs: center = (x, y),
    midleft = (x, y),
    midright = (x, y),
    topleft = (x, y),
    topright = (x, y),
    bottomleft = (x, y),
    bottomright = (x, y)
    """
    if text.font is None:
        font = pygame.font.SysFont(text.font, text.size)
    else:
        font = pygame.font.Font(f"./data/fonts/{text.font}.ttf", text.size)
    image = font.render(text.text, antialias, text.color)
    rect = image.get_rect(**rectkvargs)
    surface.blit(image, rect)
