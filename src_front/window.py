"""Opens the game window and runs the main loop."""

import pygame
from src_back import parsing
from src_back.game.gamestate import Game_state
from src_back.game.constants import Game_status
from src_front import maze_view
from src_front import entities
from src_front import hud
from src_front import menu

WIDTH = 720
HEIGHT = 800
HUD_HEIGHT = 90
MAZE_X = 40
MAZE_Y = 110
CELL = 42
FPS = 60
MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
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
    main_menu = menu.Menu(menu.MAIN_ITEMS, "PAC-MAN")
    pause_menu = menu.Menu(menu.PAUSE_ITEMS, "PAUSED")
    current = MENU

    while running:
        dt = clock.tick(FPS) / 1000.0

        # --- input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif current == MENU:
                action = main_menu.handle_event(event)
                if action == "start":
                    state.initialize_level()
                    current = PLAYING
                elif action == "quit":
                    running = False

            elif current == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_menu.index = 0
                        current = PAUSED
                    else:
                        direction = MOVEMENT_KEYS.get(event.key)
                        if direction is not None:
                            state.handle_input(direction)

            elif current == PAUSED:
                action = pause_menu.handle_event(event)
                if action == "resume":
                    current = PLAYING
                elif action == "menu":
                    current = MENU
                elif action == "quit":
                    running = False

        # --- update
        if current == PLAYING:
            elapsed += dt
            state.update_timers(dt)
            state.update_ghosts_time(dt)
            state.move_player(dt)
            state.check_pacgum_at_player()
            state.move_ghosts(dt)
            state.check_ghost_collision()

        # --- draw
        screen.fill(BACKGROUND)

        if current == MENU:
            main_menu.draw(screen)
        else:
            data = state.all_data_to_dict()
            player = data["player"]
            flashing = (player["power_time"] <= 2.0 and
                        int(elapsed * 6) % 2 == 0)

            maze_view.draw_maze(screen, data["maze"], MAZE_X, MAZE_Y, CELL)
            maze_view.draw_pacgums(screen, data["pacgums"],
                                   data["super_pacgums"],
                                   MAZE_X, MAZE_Y, CELL)

            for ghost in data["ghosts"]:
                entities.draw_ghost(screen, ghost, flashing, MAZE_X, MAZE_Y,
                                    CELL)
            entities.draw_player(screen, player, elapsed, MAZE_X, MAZE_Y,
                                 CELL)
            hud.draw_hud(screen, data, len(config.levels), HUD_HEIGHT)
            if current == PAUSED:
                menu.dim(screen)
                pause_menu.draw(screen)
        pygame.display.flip()

    pygame.quit()
