"""Opens the game window and runs the main loop."""

import pygame
from src_back import parsing
from src_back.game.gamestate import Game_state
from src_back.game.constants import Game_status
from src_front import maze_view
from src_front import entities
import src_front.hud as hud

WIDTH = 720
HEIGHT = 800
HUD_HEIGHT = 90
MAZE_X = 40
MAZE_Y = 110
CELL = 42
FPS = 60
BACKGROUND = (8, 9, 16)
MOVEMENT_KEYS = {
    pygame.K_UP: "up",
    pygame.K_w: "up",
    pygame.K_DOWN: "down",
    pygame.K_s: "down",
    pygame.K_LEFT: "left",
    pygame.K_a: "left",
    pygame.K_RIGHT: "right",
    pygame.K_d: "right",
}


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
            elif event.type == pygame.KEYDOWN:
                direction = MOVEMENT_KEYS.get(event.key)
                if direction is not None:
                    state.handle_input(direction)
        state.update_timers(dt)
        state.update_ghosts_time(dt)
        state.move_player(dt)
        state.check_pacgum_at_player()
        state.move_ghosts(dt)
        state.check_ghost_collision()

        screen.fill(BACKGROUND)
        # --- draw: read her state, draw it ---
        data = state.all_data_to_dict()

        maze_view.draw_maze(screen, data["maze"], MAZE_X, MAZE_Y, CELL)
        maze_view.draw_pacgums(screen, data["pacgums"], data["super_pacgums"],
                               MAZE_X, MAZE_Y, CELL)
        player = data["player"]
        flashing = (player["power_time"] <= 2.0 and int(elapsed * 6) % 2 == 0)
        for ghost in data["ghosts"]:
            entities.draw_ghost(screen, ghost, flashing, 40, 40, 42)
        entities.draw_player(screen, player, elapsed, 40, 40, 42)
        hud.draw_hud(screen, data, len(config.levels), HUD_HEIGHT)
        pygame.display.flip()

    pygame.quit()
