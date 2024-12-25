"""main game_state file"""

import sys
import time as tm
import pygame
from bearsharkutils.tiledutils import load
from bearsharkutils.pygameutils.datastructures import AnimatedEntityGroup
from player import Player
from drawtext import draw_text, Text

pygame.init()

FPS = 60
screen_width, screen_height = 864, 512
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Island rumble")
pygame.display.set_icon(pygame.image.load("./assets/icon.png"))

tiles = load("./data/tmx/tmx.tmx", (32, 32))[0]
spawnPoints = load("./data/tmx/tmx.tmx", (32, 32))[1].search_by_props(
    "type", "spawn_point"
)

players: AnimatedEntityGroup = AnimatedEntityGroup()
bullets = AnimatedEntityGroup()

state: str = "COMBAT"
score = [0, 0]

player_config = {
    "ground": tiles.search_by_type("ground"),
    "ocean": tiles.search_by_type("ocean"),
    "groups": [players],
}

player1 = Player(
    pos=spawnPoints[0].rect.center,
    side="left",
    **player_config,
)
player2 = Player(
    pos=spawnPoints[1].rect.center,
    side="right",
    **player_config,
)


def time():
    """Get the current time"""
    return int(round(tm.time() * 1000))


def handle_input():
    """Handle the input"""
    if state == "COMBAT":
        player: Player
        for player in players.sprites():
            player.handle_input(bullets, time())


def update():
    """Update the game_state"""
    bullets.update()
    players.update(bullets)
    return page_managing()


def render():
    """Render the game_state"""
    if state == "GAMEOVER":
        screen.fill((0, 0, 0))
        screen.fill((0, 0, 0))
        winner: Player = players.sprites()[0]
        if players.sprites() and not players.sprites()[0].isdead:
            draw_text(
                screen,
                Text(
                    f"Player on the {winner.side} side wins!",
                    68,
                ),
                True,
                center=(screen_width / 2, screen_height / 2 - 64),
            )
        else:
            draw_text(
                screen,
                Text("It's a draw!", 68),
                True,
                center=(screen_width / 2, screen_height / 2),
            )

        draw_text(
            screen,
            Text("Press R key to restart", 34),
            True,
            center=(screen_width / 2, screen_height / 2 + 80),
        )

        players.draw(screen)

    if state == "COMBAT":
        screen.fill((135, 206, 235))

        tiles.updateAnimation(time())
        tiles.draw(screen)

        bullets.updateAnimation(time())
        bullets.draw(screen)

        draw_text(
            screen,
            Text("fps: " + str(int(clock.get_fps())), 18, (0, 0, 0)),
            True,
            topright=(screen_width - 3, 3),
        )

        draw_text(
            screen,
            Text(f"{score[0]}:{score[1]}", 32, (126, 172, 222)),
            True,
            center=(screen_width / 2, screen_height / 2 - 150),
        )

        players.updateAnimation(time())
        players.draw(screen)

    pygame.display.update()


# def restart_game():
#     """Restart the game_state"""
#     score = .score
#     winner: Player = .players.sprites()[0]
#     if winner.side == "left":
#         score[0] = score[0] + 1
#     else:
#         score[1] = score[1] + 1
#     .__init__()
#     .score = score


def page_managing():
    """Manage the pages"""
    if not (players.has(player1)) or not players.has(player2):
        bullets.empty()
        return "GAMEOVER"
    return "COMBAT"


if __name__ == "__main__":
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        handle_input()

        state: str = update()

        render()

        clock.tick(FPS)
