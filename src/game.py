"""main game_state file"""

import sys
from dataclasses import dataclass
import pygame
from bearsharkutils.tiledutils import load
from bearsharkutils.pygameutils.datastructures import AnimatedEntityGroup
from player import Player

pygame.init()


@dataclass
class Text:
    """Text dataclass"""

    text: str
    size: int
    color: tuple[int, int, int]
    font: str = None


def draw_text(
    surface: pygame.Surface,
    text: Text,
    antialias: bool,
    **rectkvargs,
):
    """Draw text on the screen"""
    font = pygame.font.SysFont(text.font, text.size)
    image = font.render(text.text, antialias, text.color)
    rect = image.get_rect(**rectkvargs)
    surface.blit(image, rect)


class Game:
    """Main game_state class"""

    fps = 60
    screen_width, screen_height = 864, 512
    tile_size = (32, 32)
    margin = 40
    ms_per_update = 1000 / fps
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(
        (screen_width + margin, screen_height + margin), pygame.RESIZABLE
    )
    RENDERSURFACE = pygame.Surface((screen_width, screen_height))

    # All window setup
    pygame.display.set_caption("Island rumble")
    pygame.display.set_icon(pygame.image.load("./assets/icon.png"))

    # All Tiled data import
    tiles = load("./data/tmx/tmx.tmx", (tile_size))[0]
    ground = tiles.search_by_type("ground")
    ocean = tiles.search_by_type("ocean")
    objects = load("./data/tmx/tmx.tmx", (tile_size))[1]
    spawnPoints = objects.search_by_props("type", "spawn_point")

    # All sprite groups
    players: AnimatedEntityGroup = AnimatedEntityGroup()
    bullets = AnimatedEntityGroup()

    state = "COMBAT"
    score = [0, 0]

    players.empty()

    player1 = Player(
        spawnPoints[0].rect.center,
        ground,
        ocean,
        "left",
        players,
    )
    player2 = Player(
        spawnPoints[1].rect.center,
        ground,
        ocean,
        "right",
        players,
    )

    @classmethod
    def get_current_time(cls):
        """Get the current time"""
        return pygame.time.get_ticks()

    @classmethod
    def handle_input(cls):
        """Handle the input"""
        if cls.state == "COMBAT":
            player: Player
            for player in cls.players.sprites():
                player.handle_input(cls.bullets, cls.get_current_time())

    @classmethod
    def update(cls):
        """Update the game_state"""
        cls.bullets.update()
        cls.players.update(cls.bullets)

    @classmethod
    def render(cls):
        """Render the game_state"""
        if cls.state == "GAMEOVER":
            cls.RENDERSURFACE.fill((0, 0, 0))
            cls.screen.fill((0, 0, 0))
            winner: Player = cls.players.sprites()[0]
            if cls.players.sprites() and not cls.players.sprites()[0].isdead:
                t = Text(
                    f"Player on the {winner.side} side wins!",
                    68,
                    (255, 255, 255),
                )
                draw_text(
                    cls.RENDERSURFACE,
                    t,
                    True,
                    center=(cls.screen_width / 2, cls.screen_height / 2 - 64),
                )
            else:
                t = Text("It's a draw!", 68, (255, 255, 255))
                draw_text(
                    cls.RENDERSURFACE,
                    t,
                    True,
                    center=(cls.screen_width / 2, cls.screen_height / 2),
                )
            t = Text("Press R key to restart", 34, (255, 255, 255))
            draw_text(
                cls.RENDERSURFACE,
                t,
                True,
                center=(cls.screen_width / 2, cls.screen_height / 2 + 80),
            )

            cls.players.draw(cls.RENDERSURFACE)

        if cls.state == "COMBAT":
            cls.RENDERSURFACE.fill((135, 206, 235))
            cls.screen.fill((0, 0, 0))

            cls.tiles.updateAnimation(cls.get_current_time())
            cls.tiles.draw(cls.RENDERSURFACE)

            cls.bullets.updateAnimation(cls.get_current_time())
            cls.bullets.draw(cls.RENDERSURFACE)

            t = Text("fps: " + str(int(cls.clock.get_fps())), 18, (0, 0, 0))
            draw_text(
                cls.RENDERSURFACE,
                t,
                True,
                topright=(cls.screen_width - 3, 3),
            )

            t = Text(f"{cls.score[0]}:{cls.score[1]}", 32, (126, 172, 222), "Mainport")
            draw_text(
                cls.RENDERSURFACE,
                t,
                True,
                center=(cls.screen_width / 2, cls.screen_height / 2 - 150),
            )

            if cls.screen.get_flags() == -2130706416:
                t = Text("Press key F11 to toggle fullscreen", 16, (255, 255, 255))
                draw_text(
                    cls.screen,
                    t,
                    False,
                    topleft=(2, 2),
                )

            # player: Player
            # for player in cls.players.sprites():
            #     if player.isdead:
            #         cls.RENDERSURFACE.fill((0, 0, 0))

            cls.players.updateAnimation(cls.get_current_time())
            cls.players.draw(cls.RENDERSURFACE)

        cls.screen.blit(
            cls.RENDERSURFACE,
            cls.RENDERSURFACE.get_rect(
                center=(
                    cls.screen.get_size()[0] / 2,
                    cls.screen.get_size()[1] / 2,
                )
            ),
        )

        pygame.display.update()

    # def restart_game(cls):
    #     """Restart the game_state"""
    #     score = cls.score
    #     winner: Player = cls.players.sprites()[0]
    #     if winner.side == "left":
    #         score[0] = score[0] + 1
    #     else:
    #         score[1] = score[1] + 1
    #     cls.__init__()
    #     cls.score = score
    @classmethod
    def page_managing(cls):
        """Manage the pages"""
        if not (cls.players.has(cls.player1)) or not cls.players.has(cls.player2):
            cls.state = "GAMEOVER"
            cls.bullets.empty()
        else:
            cls.state = "COMBAT"

    @classmethod
    def loop(cls):
        """Main game_state loop"""
        game_state = True
        previous = cls.get_current_time()
        lag: float = 0.0
        while game_state:
            for e in pygame.event.get():
                # quit the game_state if the event is a QUIT
                if e.type == pygame.QUIT:
                    game_state = False
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_F11:
                        # Set the display mode to fullscreen or reszable mode.
                        if cls.screen.get_flags() != -2130706416:
                            cls.screen = pygame.display.set_mode(
                                (0, 0), pygame.FULLSCREEN
                            )
                        else:
                            cls.screen = pygame.display.set_mode(
                                (
                                    cls.screen_width + cls.margin,
                                    cls.screen_height + cls.margin,
                                ),
                                pygame.RESIZABLE,
                            )
                    if e.key == pygame.K_ESCAPE:
                        cls.screen = pygame.display.set_mode(
                            (
                                cls.screen_width + cls.margin,
                                cls.screen_height + cls.margin,
                            ),
                            pygame.RESIZABLE,
                        )
                    # if e.key == pygame.K_r and cls.state == "GAMEOVER":
                    #     cls.restart_game()

            current = cls.get_current_time()
            elapsed = current - previous
            previous = current
            lag += elapsed

            cls.handle_input()

            while lag >= cls.ms_per_update:
                cls.update()
                lag -= cls.ms_per_update

            cls.page_managing()

            cls.render()

            cls.clock.tick(cls.fps)


if __name__ == "__main__":
    Game.loop()
