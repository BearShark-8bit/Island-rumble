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

    def __init__(self) -> None:
        self.pageOn = "game"

        Game.players.empty()

        self.player1 = Player(
            Game.spawnPoints[0].rect.center,
            Game.ground,
            Game.ocean,
            "left",
            Game.players,
        )
        self.player2 = Player(
            Game.spawnPoints[1].rect.center,
            Game.ground,
            Game.ocean,
            "right",
            Game.players,
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
            for player in Game.players.sprites():
                player.handle_input(Game.bullets, self.getCurrentTime())

    def update(self):
        """
        Updates the game. Should be called every frame
        """
        Game.bullets.update()
        Game.players.update(Game.bullets)

    def render(self):
        """
        Renders the game over screen
        """
        # This method is called when the game is over
        if self.pageOn == "game over screen":
            Game.renderSurface.fill((0, 0, 0))
            Game.screen.fill((0, 0, 0))
            if Game.players.sprites() and not (Game.players.sprites()[0].isdead):
                text(
                    Game.renderSurface,
                    f"Player on the {Game.players.sprites()[0].side} side wins!",
                    68,
                    (255, 255, 255),
                    True,
                    center=(Game.screenWidth / 2, Game.screenHeight / 2 - 64),
                )
            else:
                text(
                    Game.renderSurface,
                    f"It's a draw!",
                    68,
                    (255, 255, 255),
                    True,
                    center=(Game.screenWidth / 2, Game.screenHeight / 2),
                )
            text(
                self.renderSurface,
                "Press R key to restart",
                34,
                (255, 255, 255),
                True,
                center=(Game.screenWidth / 2, Game.screenHeight / 2 + 80),
            )

            Game.players.draw(Game.renderSurface)

        # This method is called when the page is on game page.
        if self.pageOn == "game":
            Game.renderSurface.fill((135, 206, 235))
            Game.screen.fill((0, 0, 0))

            Game.tiles.updateAnimation(self.getCurrentTime())
            Game.tiles.draw(Game.renderSurface)

            Game.bullets.updateAnimation(self.getCurrentTime())
            Game.bullets.draw(Game.renderSurface)

            text(
                Game.renderSurface,
                "FPS: " + str(int(Game.clock.get_fps())),
                18,
                (0, 0, 0),
                True,
                topright=(Game.screenWidth - 3, 3),
            )

            # Toggle fullscreen mode. If the user pressing key F11 to toggle fullscreen the fullscreen is pressed.
            if Game.screen.get_flags() == -2130706416:
                text(
                    Game.screen,
                    "Press key F11 to toggle fullscreen",
                    16,
                    (255, 255, 255),
                    False,
                    topleft=(2, 2),
                )

            player: Player
            for player in Game.players.sprites():
                if player.isdead:
                    Game.renderSurface.fill((0, 0, 0))

            Game.players.updateAnimation(self.getCurrentTime())
            Game.players.draw(Game.renderSurface)

        Game.screen.blit(
            Game.renderSurface,
            Game.renderSurface.get_rect(
                center=(
                    Game.screen.get_size()[0] / 2,
                    Game.screen.get_size()[1] / 2,
                )
            ),
        )

        pygame.display.update()

    def restartGame(self):
        self.__init__()

    def pageManaging(self):
        if not (Game.players.has(self.player1)) or not (Game.players.has(self.player2)):
            self.pageOn = "game over screen"
            Game.bullets.empty()

        else:
            self.pageOn = "game"

    def loop(self):
        """
        Loop indefinitely until quit
        """
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
                        if Game.screen.get_flags() != -2130706416:
                            Game.screen = pygame.display.set_mode(
                                (0, 0), pygame.FULLSCREEN
                            )
                        else:
                            Game.screen = pygame.display.set_mode(
                                (
                                    Game.screenWidth + Game.margin,
                                    Game.screenHeight + Game.margin,
                                ),
                                pygame.RESIZABLE,
                            )
                    if e.key == pygame.K_ESCAPE:
                        Game.screen = pygame.display.set_mode(
                            (
                                Game.screenWidth + Game.margin,
                                Game.screenHeight + Game.margin,
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

            Game.clock.tick(Game.fps)


if __name__ == "__main__":
    Game()
