"""Opens the game window and runs the main loop."""

import pygame
from src_back import parsing
from src_back.game.gamestate import Game_state
from src_back.game.constants import Game_status
from src_front import maze_view
from src_front import entities

WIDTH = 720
HEIGHT = 720
FPS = 60
BACKGROUND = (8, 9, 16)


def run(config_path: str) -> None:
    """Open the window and keep it open until the user closes it."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man")
    clock = pygame.time.Clock()

    # --- setup: build the level once, before the loop ---
    config = parsing.pars_config(config_path)
    level = config.levels[0]
    state = Game_state(None, level.width, level.height, set(), set(), None,
                       [], 0, 0, config.level_max_time,
                       Game_status.PLAYING, False, {}, config, [])
    state.initialize_level()

    elapsed = 0.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        elapsed += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND)
        # --- draw: read her state, draw it ---
        data = state.all_data_to_dict()

        maze_view.draw_maze(screen, data["maze"], 40, 40, 42)
        maze_view.draw_pacgums(screen, data["pacgums"], data["super_pacgums"],
                               40, 40, 42)
        player = data["player"]
        flashing = (player["power_time"] <= 2.0 and int(elapsed * 6) % 2 == 0)
        for ghost in data["ghosts"]:
            entities.draw_ghost(screen, ghost, flashing, 40, 40, 42)
        entities.draw_player(screen, player, elapsed, 40, 40, 42)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
