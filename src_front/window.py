"""Opens the game window and runs the main loop."""

import pygame
from src_back import parsing
from src_back.game.gamestate import Game_state
from src_back.game.constants import Game_status
from src_back.maze_loader import loader
from src_front import maze_view
from src_front import entities
from src_front import hud
from src_front import menu
from src_front import theme
from src_front import highscores
from src_front import screens
from src_front import endscreen

WIDTH = 720
HEIGHT = 800
MAZE_X = 45
MAZE_Y = 122
CELL = 42
FPS = 60
MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
HELP = "help"
SCORES = "scores"
END = "end"
BACKGROUND = theme.BG
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
    pygame.display.set_icon(pygame.image.load("assets/sprites/pacman_1.png"))
    clock = pygame.time.Clock()

    # --- setup: build the level once, before the loop ---
    config = parsing.pars_config(config_path)
    level = config.levels[0]
    maze = loader.load_maze(level.width, level.height, config.seed)
    state = Game_state(maze, level.width, level.height, set(), set(), None,
                       [], 0, 0, config.level_max_time,
                       Game_status.PLAYING, False, {}, config, [])
    state.initialize_level()

    elapsed = 0.0

    running = True
    main_menu = menu.Menu(menu.MAIN_ITEMS, "PAC-MAN")
    pause_menu = menu.Menu(menu.PAUSE_ITEMS, "PAUSED")
    end_screen = endscreen.EndScreen()
    scores = highscores.load(config.highscore_filename)
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
                elif action == "help":
                    current = HELP
                elif action == "scores":
                    current = SCORES
                elif action == "quit":
                    running = False

            elif current == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_menu.index = 0
                        current = PAUSED
                    elif event.key == pygame.K_c:
                        state.cheat_skip_level()
                    elif event.key == pygame.K_l:
                        state.cheat_add_lives()
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

            elif current in (HELP, SCORES):
                if event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_ESCAPE, pygame.K_RETURN):
                    current = MENU
                elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    current = MENU

            elif current == END:
                if end_screen.handle_event(event):
                    scores = highscores.add(scores, end_screen.name, end_screen.score)
                    highscores.save(config.highscore_filename, scores)
                    current = MENU

        # --- update
        if current == PLAYING:
            if state.game_status in (Game_status.GAME_OVER,
                                     Game_status.VICTORY):
                end_screen.start(state.game_status == Game_status.VICTORY,
                                 state.score)
                current = END
            else:
                elapsed += dt
                state.update_timers(dt)
                state.update_ghosts_time(dt)
                state.move_player(dt)
                state.check_pacgum_at_player()
                state.move_ghosts(dt)
                state.check_ghost_collision()
                state.check_level_complete()
        # --- draw
        screen.fill(BACKGROUND)

        if current == MENU:
            data = state.all_data_to_dict()
            maze_view.draw_maze(screen, data["maze"], 45, 85, 42,
                                theme.FAINT_WALL, theme.FAINT_WALL)
            main_menu.draw(screen)
            menu.draw_tagline(screen)
            menu.draw_parade(screen)
            menu.draw_leaderboard(screen, scores)
            menu.draw_hint(screen)
        elif current == HELP:
            screens.draw_help(screen)
        elif current == SCORES:
            screens.draw_scores(screen, scores)
        else:
            data = state.all_data_to_dict()
            player = data["player"]

            maze_view.draw_maze(screen, data["maze"], MAZE_X, MAZE_Y, CELL)
            maze_view.draw_pacgums(screen, data["pacgums"],
                                   data["super_pacgums"],
                                   MAZE_X, MAZE_Y, CELL)

            for ghost in data["ghosts"]:
                flashing = (ghost.get("ghost_freaid", 99.0) <= 2.0
                            and int(elapsed * 6) % 2 == 0)
                entities.draw_ghost(screen, ghost, flashing, MAZE_X, MAZE_Y,
                                    CELL)
            entities.draw_player(screen, player, elapsed, MAZE_X, MAZE_Y,
                                 CELL)
            hud.draw_hud(screen, data, len(config.levels))
            if current == PAUSED:
                menu.dim(screen)
                pause_menu.draw(screen)
            elif current == END:
                menu.dim(screen)
                end_screen.draw(screen)
        pygame.display.flip()

    pygame.quit()
