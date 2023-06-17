import sys
import pygame
import Tiled_utils
from pytmx.util_pygame import load_pygame
from Player import Player
import Pygame_utils
from Bullet import Bullet


class Game:
    pygame.init()
    fps = 60
    screenWidth, screenHeight = 864, 512
    tileSize = (32, 32)
    margin = 40
    msPerUpdate = 1000 / fps
    clock = pygame.time.Clock()
    players: pygame.sprite.Group = pygame.sprite.Group()
    screen = pygame.display.set_mode(
        (
            screenWidth + margin,
            screenHeight + margin,
        ),
        pygame.RESIZABLE,
    )
    pygame.display.set_caption("Island rumble")
    pygame.display.set_icon(pygame.image.load("./assets/icon.png"))
    tiles = Tiled_utils.load(load_pygame("./data/tmx/tmx.tmx"), (tileSize))[0]
    renderSurface = pygame.Surface((screenWidth, screenHeight))
    ground: list[Tiled_utils.VisibleTile] = tiles.search_by_props("type", "ground")
    ocean: list[Tiled_utils.VisibleTile] = tiles.search_by_props("type", "ocean")
    objects = Tiled_utils.load(load_pygame("./data/tmx/tmx.tmx"), (tileSize))[1]
    spawnPoints = objects.search_by_props("type", "spawn_point")
    bullets = pygame.sprite.Group()

    def __init__(self) -> None:
        self.pageOn = "game"

        self.player1 = Player(
            Game.spawnPoints[0].rect.center,
            Game.ground,
            Game.ocean,
            "left",
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
        Game.players.update()

    def render(self):
        """
        Renders the game over screen
        """
        # This method is called when the game is over
        if self.pageOn == "game over screen":
            Game.renderSurface.fill((0, 0, 0))
            Game.screen.fill((0, 0, 0))

            Pygame_utils.text(
                Game.renderSurface,
                "GAME OVER",
                68,
                (255, 255, 255),
                True,
                center=(Game.screenWidth / 2, Game.screenHeight / 2),
            )
            Pygame_utils.text(
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

            bullet: Bullet
            for bullet in Game.bullets.sprites():
                bullet.updateAnimation(self.getCurrentTime())
            Game.bullets.draw(Game.renderSurface)

            player: Player
            for player in Game.players:
                player.updateAnimation(self.getCurrentTime())
            Game.players.draw(Game.renderSurface)

            Pygame_utils.text(
                Game.renderSurface,
                "FPS: " + str(int(Game.clock.get_fps())),
                18,
                (0, 0, 0),
                True,
                topright=(Game.screenWidth - 3, 3),
            )

            # Toggle fullscreen mode. If the user pressing key F11 to toggle fullscreen the fullscreen is pressed.
            if Game.screen.get_flags() == -2130706416:
                Pygame_utils.text(
                    Game.screen,
                    "Press key F11 to toggle fullscreen",
                    (0, 2),
                    16,
                    (255, 255, 255),
                    False,
                )

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
        if not (Game.players.has(self.player1)):
            self.pageOn = "game over screen"

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


Game()
