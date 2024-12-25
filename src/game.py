"""Main game file"""

import sys
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


def handle_input():
    """Handle the input"""
    if state == "COMBAT":
        player: Player
        for player in players.sprites():
            player.handle_input(bullets, pygame.time.get_ticks())


def update():
    """Update the game_state"""
    bullets.update()
    players.update(bullets)
    return page_managing()


def render():
    """Render the game_state"""
    if state == "GAMEOVER":
        screen.fill((0, 0, 0))
        winner: Player = players.sprites()[0]
        draw_text(
            screen,
            Text(
                f"Player on the {winner.side} side wins!",
                68,
            ),
            True,
            center=(screen_width / 2, screen_height / 2 - 64),
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

        tiles.updateAnimation(pygame.time.get_ticks())
        tiles.draw(screen)

        bullets.updateAnimation(pygame.time.get_ticks())
        bullets.draw(screen)

        draw_text(
            screen,
            Text(f"{score[0]}:{score[1]}", 32, (126, 172, 222)),
            True,
            center=(screen_width / 2, screen_height / 2 - 150),
        )

        players.updateAnimation(pygame.time.get_ticks())
        players.draw(screen)

    pygame.display.update()


def restart_game():
    """Restart the game_state"""
    global state, player1, player2
    winner: Player = players.sprites()[0]
    if winner.side == "left":
        score[0] = score[0] + 1
    else:
        score[1] = score[1] + 1

    players.empty()
    bullets.empty()

    state = "COMBAT"

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


def page_managing():
    """Manage the pages"""
    if not (players.has(player1)) or not players.has(player2):
        bullets.empty()
        return "GAMEOVER"
    return "COMBAT"


while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r and state == "GAMEOVER":
                restart_game()

    handle_input()

    state: str = update()

    render()

    clock.tick(FPS)
