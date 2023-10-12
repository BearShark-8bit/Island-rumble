import sys

import pygame

pygame.init()

from Player import Player


from bearsharkutils.tiledutils import load
from bearsharkutils.pygameutils.datastructures import AnimatedEntityGroup
from bearsharkutils.pygameutils import text


class Game:
    # All constants
    FPS = 60
    SCREENWIDTH, SCREENHEIGHT = 864, 512
    TILESIZE = (32, 32)
    MARGIN = 40
    MSPERUPDATE = 1000 / FPS
    CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode(
        (SCREENWIDTH + MARGIN, SCREENHEIGHT + MARGIN), pygame.RESIZABLE
    )
    RENDERSURFACE = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))

    # All window setup
    pygame.display.set_caption("Island rumble")
    pygame.display.set_icon(pygame.image.load("./assets/icon.png"))

    # All Tiled data import
    tiles = load("./data/tmx/tmx.tmx", (TILESIZE))[0]
    ground = tiles.search_by_type("ground")
    ocean = tiles.search_by_type("ocean")
    objects = load("./data/tmx/tmx.tmx", (TILESIZE))[1]
    spawnPoints = objects.search_by_props("type", "spawn_point")

    # All sprite groups
    players: AnimatedEntityGroup = AnimatedEntityGroup()
    bullets = AnimatedEntityGroup()

    def __init__(self) -> None:
        self.state = "COMBAT"
        self.score = [0, 0]

        self.players.empty()

        self.player1 = Player(
            self.spawnPoints[0].rect.center,
            self.ground,
            self.ocean,
            "left",
            self.players,
        )
        self.player2 = Player(
            self.spawnPoints[1].rect.center,
            self.ground,
            self.ocean,
            "right",
            self.players,
        )

    def getCurrentTime(self):
        return pygame.time.get_ticks()

    def handleInput(self):
        if self.state == "COMBAT":
            player: Player
            for player in self.players.sprites():
                player.handle_input(self.bullets, self.getCurrentTime())

    def update(self):
        self.bullets.update()
        self.players.update(self.bullets)

    def render(self):
        if self.state == "GAMEOVER":
            self.RENDERSURFACE.fill((0, 0, 0))
            self.SCREEN.fill((0, 0, 0))
            winner: Player = self.players.sprites()[0]
            if self.players.sprites() and not (self.players.sprites()[0].isdead):
                text(
                    self.RENDERSURFACE,
                    f"Player on the {winner.side} side wins!",
                    68,
                    (255, 255, 255),
                    True,
                    center=(self.SCREENWIDTH / 2, self.SCREENHEIGHT / 2 - 64),
                )
            else:
                text(
                    self.RENDERSURFACE,
                    f"It's a draw!",
                    68,
                    (255, 255, 255),
                    True,
                    center=(self.SCREENWIDTH / 2, self.SCREENHEIGHT / 2),
                )
            text(
                self.RENDERSURFACE,
                "Press R key to restart",
                34,
                (255, 255, 255),
                True,
                center=(self.SCREENWIDTH / 2, self.SCREENHEIGHT / 2 + 80),
            )

            self.players.draw(self.RENDERSURFACE)

        if self.state == "COMBAT":
            self.RENDERSURFACE.fill((135, 206, 235))
            self.SCREEN.fill((0, 0, 0))

            self.tiles.updateAnimation(self.getCurrentTime())
            self.tiles.draw(self.RENDERSURFACE)

            self.bullets.updateAnimation(self.getCurrentTime())
            self.bullets.draw(self.RENDERSURFACE)

            text(
                self.RENDERSURFACE,
                "FPS: " + str(int(self.CLOCK.get_fps())),
                18,
                (0, 0, 0),
                True,
                topright=(self.SCREENWIDTH - 3, 3),
            )

            # Toggle fullscreen mode. If the user pressing key F11 to toggle fullscreen the fullscreen is pressed.
            if self.SCREEN.get_flags() == -2130706416:
                text(
                    self.SCREEN,
                    "Press key F11 to toggle fullscreen",
                    16,
                    (255, 255, 255),
                    False,
                    topleft=(2, 2),
                )

            # player: Player
            # for player in self.players.sprites():
            #     if player.isdead:
            #         self.RENDERSURFACE.fill((0, 0, 0))

            self.players.updateAnimation(self.getCurrentTime())
            self.players.draw(self.RENDERSURFACE)

        self.SCREEN.blit(
            self.RENDERSURFACE,
            self.RENDERSURFACE.get_rect(
                center=(
                    self.SCREEN.get_size()[0] / 2,
                    self.SCREEN.get_size()[1] / 2,
                )
            ),
        )

        pygame.display.update()

    def restartGame(self):
        score = self.score
        self.__init__()
        self.score = score

    def pageManaging(self):
        if not (self.players.has(self.player1)) or not (self.players.has(self.player2)):
            self.state = "GAMEOVER"
            self.bullets.empty()
        else:
            self.state = "COMBAT"

    def loop(self):
        game = True
        previous = self.getCurrentTime()
        lag: float = 0.0
        while game:
            for e in pygame.event.get():
                # quit the game if the event is a QUIT
                if e.type == pygame.QUIT:
                    game = False
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_F11:
                        # Set the display mode to fullscreen or reszable mode.
                        if self.SCREEN.get_flags() != -2130706416:
                            self.SCREEN = pygame.display.set_mode(
                                (0, 0), pygame.FULLSCREEN
                            )
                        else:
                            self.SCREEN = pygame.display.set_mode(
                                (
                                    self.SCREENWIDTH + self.MARGIN,
                                    self.SCREENHEIGHT + self.MARGIN,
                                ),
                                pygame.RESIZABLE,
                            )
                    if e.key == pygame.K_ESCAPE:
                        self.SCREEN = pygame.display.set_mode(
                            (
                                self.SCREENWIDTH + self.MARGIN,
                                self.SCREENHEIGHT + self.MARGIN,
                            ),
                            pygame.RESIZABLE,
                        )
                    if e.key == pygame.K_r and self.state == "GAMEOVER":
                        self.restartGame()

            current = self.getCurrentTime()
            elapsed = current - previous
            previous = current
            lag += elapsed

            self.handleInput()

            while lag >= self.MSPERUPDATE:
                self.update()
                lag -= self.MSPERUPDATE

            self.pageManaging()

            self.render()

            self.CLOCK.tick(self.FPS)


if __name__ == "__main__":
    game = Game()
    game.loop()
