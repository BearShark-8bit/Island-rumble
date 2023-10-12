import importlib
import sys
import pygame

from Player import Player


from bearsharkutils.tiledutils import load
from bearsharkutils.pygameutils.datastructures import AnimatedEntityGroup
from bearsharkutils.pygameutils import text


class Game:
    pygame.init()
    fps = 60
    screenWidth, screenHeight = 864, 512
    tileSize = (32, 32)
    margin = 40
    msPerUpdate = 1000 / fps
    clock = pygame.time.Clock()
    players: AnimatedEntityGroup = AnimatedEntityGroup()
    screen = pygame.display.set_mode(
        (
            screenWidth + margin,
            screenHeight + margin,
        ),
        pygame.RESIZABLE,
    )
    pygame.display.set_caption("Island rumble")
    pygame.display.set_icon(pygame.image.load("./assets/icon.png"))
    tiles = load("./data/tmx/tmx.tmx", (tileSize))[0]
    renderSurface = pygame.Surface((screenWidth, screenHeight))
    ground = tiles.search_by_type("ground")
    ocean = tiles.search_by_type("ocean")
    objects = load("./data/tmx/tmx.tmx", (tileSize))[1]
    spawnPoints = objects.search_by_props("type", "spawn_point")
    bullets = AnimatedEntityGroup()
    score = [0, 0]

    def __init__(self) -> None:
        self.pageOn = "game"

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

        self.game = True

        self.loop()

    def getCurrentTime(self):
        """
        Returns the number of seconds since the start of the game.

        """
        return pygame.time.get_ticks()

    def handleInput(self):
        """
        Handles input from the player
        """
        # Called when the game is on game page
        if self.pageOn == "game":
            player: Player
            for player in self.players.sprites():
                player.handle_input(self.bullets, self.getCurrentTime())

    def update(self):
        """
        Updates the game. Should be called every frame
        """
        self.bullets.update()
        self.players.update(self.bullets)

    def render(self):
        """
        Renders the game over screen
        """
        # This method is called when the game is over
        if self.pageOn == "game over screen":
            self.renderSurface.fill((0, 0, 0))
            self.screen.fill((0, 0, 0))
            winner: Player = self.players.sprites()[0]
            if self.players.sprites() and not (self.players.sprites()[0].isdead):
                text(
                    self.renderSurface,
                    f"Player on the {winner.side} side wins!",
                    68,
                    (255, 255, 255),
                    True,
                    center=(self.screenWidth / 2, self.screenHeight / 2 - 64),
                )
            else:
                text(
                    self.renderSurface,
                    f"It's a draw!",
                    68,
                    (255, 255, 255),
                    True,
                    center=(self.screenWidth / 2, self.screenHeight / 2),
                )
            text(
                self.renderSurface,
                "Press R key to restart",
                34,
                (255, 255, 255),
                True,
                center=(self.screenWidth / 2, self.screenHeight / 2 + 80),
            )

            self.players.draw(self.renderSurface)

        # This method is called when the page is on game page.
        if self.pageOn == "game":
            self.renderSurface.fill((135, 206, 235))
            self.screen.fill((0, 0, 0))

            self.tiles.updateAnimation(self.getCurrentTime())
            self.tiles.draw(self.renderSurface)

            self.bullets.updateAnimation(self.getCurrentTime())
            self.bullets.draw(self.renderSurface)

            text(
                self.renderSurface,
                "FPS: " + str(int(self.clock.get_fps())),
                18,
                (0, 0, 0),
                True,
                topright=(self.screenWidth - 3, 3),
            )

            # Toggle fullscreen mode. If the user pressing key F11 to toggle fullscreen the fullscreen is pressed.
            if self.screen.get_flags() == -2130706416:
                text(
                    self.screen,
                    "Press key F11 to toggle fullscreen",
                    16,
                    (255, 255, 255),
                    False,
                    topleft=(2, 2),
                )

            player: Player
            for player in self.players.sprites():
                if player.isdead:
                    self.renderSurface.fill((0, 0, 0))

            self.players.updateAnimation(self.getCurrentTime())
            self.players.draw(self.renderSurface)

        self.screen.blit(
            self.renderSurface,
            self.renderSurface.get_rect(
                center=(
                    self.screen.get_size()[0] / 2,
                    self.screen.get_size()[1] / 2,
                )
            ),
        )

        pygame.display.update()

    def restartGame(self):
        self.__init__()

    def pageManaging(self):
        if not (self.players.has(self.player1)) or not (self.players.has(self.player2)):
            self.pageOn = "game over screen"
            self.bullets.empty()

        else:
            self.pageOn = "game"

    def loop(self):
        previous = self.getCurrentTime()
        lag = 0.0
        while self.game:
            for e in pygame.event.get():
                # quit the game if the event is a QUIT
                if e.type == pygame.QUIT:
                    self.game = False
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_F11:
                        # Set the display mode to fullscreen or reszable mode.
                        if self.screen.get_flags() != -2130706416:
                            self.screen = pygame.display.set_mode(
                                (0, 0), pygame.FULLSCREEN
                            )
                        else:
                            self.screen = pygame.display.set_mode(
                                (
                                    self.screenWidth + self.margin,
                                    self.screenHeight + self.margin,
                                ),
                                pygame.RESIZABLE,
                            )
                    if e.key == pygame.K_ESCAPE:
                        self.screen = pygame.display.set_mode(
                            (
                                self.screenWidth + self.margin,
                                self.screenHeight + self.margin,
                            ),
                            pygame.RESIZABLE,
                        )
                    if e.key == pygame.K_r and self.pageOn == "game over screen":
                        self.restartGame()

            current = self.getCurrentTime()
            elapsed = current - previous
            previous = current
            lag += elapsed

            self.handleInput()

            while lag >= self.msPerUpdate:
                self.update()
                lag -= self.msPerUpdate

            self.pageManaging()

            self.render()

            self.clock.tick(self.fps)


if __name__ == "__main__":
    Game()
