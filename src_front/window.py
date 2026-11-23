"""Opens the game window and runs the main loop."""

import pygame
import warnings
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
from src_front import sound
from src_back.game.player import PlayerState

WIDTH = 720
HEIGHT = 800
FPS = 60
PLAYER_SPEED = 5.0
TURBO_SPEED = 9.0
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


def sound_snapshot(state: Game_state) -> dict[str, int]:
    """Collect the numbers that sound effects react to."""
    return {
        "lives": state.player.lives,
        "pacgums": len(state.pacgums),
        "supers": len(state.super_pacgums),
        "ghosts_home": sum(g.state.value in ("eaten", "waiting")
                           for g in state.ghosts),
    }


def toggle_cheat(state: Game_state, name: str) -> None:
    """Switch one cheat on or off and mark the game as cheated."""
    state.cheats[name] = not state.cheats.get(name, False)
    state.cheat_mode = True


def toggle_sound(kind: str, main_menu: menu.Menu,
                 pause_menu: menu.Menu) -> None:
    """Switch music or effects, and refresh the labels in both menus."""
    sound.toggle(kind)
    music = sound.SETTINGS["music"]
    effects = sound.SETTINGS["effects"]
    main_menu.items = menu.main_items(music, effects)
    pause_menu.items = menu.pause_items(music, effects)


def load_level(state: Game_state) -> None:
    """Build the maze for state.level from the config.

    Temporary: the backend reuses the first maze on every level, so
    the frontend rebuilds it whenever the level number changes.
    """
    size = state.config.levels[state.level]
    state.width, state.height = size.width, size.height
    state.maze = loader.load_maze(size.width, size.height,
                                  state.config.seed + state.level)
    lives = state.player.lives
    state.initialize_level()
    state.player.lives = lives


def ui_offset(screen: pygame.Surface) -> tuple[int, int]:
    """Top-left corner that centres the 720 x 800 menu canvas."""
    return ((screen.get_width() - WIDTH) // 2,
            (screen.get_height() - HEIGHT) // 2)


def to_ui(event: pygame.event.Event,
          offset: tuple[int, int]) -> pygame.event.Event:
    """Return the event with its mouse position moved onto the canvas."""
    if not hasattr(event, "pos"):
        return event
    x, y = event.pos
    data = dict(event.dict, pos=(x - offset[0], y - offset[1]))
    return pygame.event.Event(event.type, data)


def game_area(screen: pygame.Surface) -> pygame.Rect:
    """The free space under the HUD card, for the maze."""
    top = hud.card_rect(screen).bottom + 12
    return pygame.Rect(16, top, screen.get_width() - 32,
                       screen.get_height() - top - 16)


def run(config_path: str) -> None:
    """Open the window and keep it open until the user closes it."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            game_window = pygame.Window.from_display_module()
            game_window.minimum_size = (WIDTH, HEIGHT)
    except (AttributeError, pygame.error):
        pass
    ui = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.display.set_caption("Pac-Man")
    try:
        pygame.display.set_icon(
            pygame.image.load("assets/sprites/pacman_1.png"))
    except (pygame.error, OSError):
        pass
    sound.init()
    sound.start_music()
    clock = pygame.time.Clock()

    # --- setup: build the level once, before the loop ---
    config = parsing.pars_config(config_path)
    level = config.levels[0]
    maze = loader.load_maze(level.width, level.height, config.seed)
    state = Game_state(maze, level.width, level.height, set(), set(),
                       PlayerState(),
                       [], 0, 0, config.level_max_time,
                       Game_status.PLAYING, False, {}, config, [])
    state.initialize_level()

    elapsed = 0.0
    built_level = 0

    running = True
    main_menu = menu.Menu(menu.main_items(True, True), "PAC-MAN")
    pause_menu = menu.Menu(menu.pause_items(True, True), "PAUSED",
                           title_y=220, items_y=325, title_size=32)
    end_screen = endscreen.EndScreen()
    scores = highscores.load(config.highscore_filename)
    current = MENU

    while running:
        dt = clock.tick(FPS) / 1000.0
        surface = pygame.display.get_surface()
        if surface is not None:
            screen = surface

        # --- input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif current == MENU:
                old = main_menu.index
                action = main_menu.handle_event(
                    to_ui(event, ui_offset(screen)))
                if main_menu.index != old:
                    sound.play("move")
                if action:
                    sound.play("select")
                if action == "start":
                    state.score = 0
                    state.level = 0
                    state.cheat_mode = False
                    state.cheats.clear()
                    state.initialize_level()
                    current = PLAYING
                elif action == "help":
                    current = HELP
                elif action in ("music", "effects"):
                    toggle_sound(action, main_menu, pause_menu)
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
                        state.cheat_mode = True
                    elif event.key == pygame.K_l:
                        state.cheat_add_lives()
                        state.cheat_mode = True
                    elif event.key == pygame.K_f:
                        toggle_cheat(state, "freeze")
                    elif event.key == pygame.K_t:
                        toggle_cheat(state, "turbo")
                    else:
                        direction = MOVEMENT_KEYS.get(event.key)
                        if direction is not None:
                            state.handle_input(direction)

            elif current == PAUSED:
                if (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_ESCAPE):
                    current = PLAYING
                else:
                    old = pause_menu.index
                    action = pause_menu.handle_event(event)
                    if pause_menu.index != old:
                        sound.play("move")
                    if action:
                        sound.play("select")
                    if action == "resume":
                        current = PLAYING
                    elif action in ("music", "effects"):
                        toggle_sound(action, main_menu, pause_menu)
                    elif action == "menu":
                        current = MENU
                    elif action == "quit":
                        running = False

            elif current in (HELP, SCORES):
                if (event.type == pygame.KEYDOWN
                        and event.key in (pygame.K_ESCAPE, pygame.K_RETURN)):
                    current = MENU
                elif (event.type == pygame.MOUSEBUTTONDOWN
                      and event.button == 1):
                    current = MENU

            elif current == END:
                if end_screen.handle_event(event):
                    scores = highscores.add(scores, end_screen.name,
                                            end_screen.score)
                    highscores.save(config.highscore_filename, scores)
                    current = MENU

        # --- update
        if current == PLAYING:
            if state.level >= len(config.levels):
                state.game_status = Game_status.VICTORY
            elif state.level != built_level:
                load_level(state)
                built_level = state.level
            if state.game_status in (Game_status.GAME_OVER,
                                     Game_status.VICTORY):
                end_screen.start(state.game_status == Game_status.VICTORY,
                                 state.score)
                current = END
            else:
                before = sound_snapshot(state)
                elapsed += dt
                state.update_timers(dt)
                if state.timer <= 0.0:
                    state.timer = config.level_max_time
                    state.rest_player()
                state.update_ghosts_time(dt)
                state.player.speed = (TURBO_SPEED if state.cheats.get("turbo")
                                      else PLAYER_SPEED)
                state.move_player(dt)
                state.check_pacgum_at_player()
                state.move_ghosts(0.0 if state.cheats.get("freeze") else dt)
                state.check_ghost_collision()
                state.check_level_complete()
                sound.react(before, sound_snapshot(state))
        frightened = current == PLAYING and any(
            g.state.value == "frightened" for g in state.ghosts
        )
        sound.set_chase(frightened)
        # --- draw
        screen.fill(BACKGROUND)

        if current in (MENU, HELP, SCORES):
            ui.fill((0, 0, 0, 0))
        if current == MENU:
            data = state.all_data_to_dict()
            ox, oy, cell = maze_view.layout(len(data["maze"][0]),
                                            len(data["maze"]),
                                            screen.get_rect())
            maze_view.draw_maze(screen, data["maze"], ox, oy, cell,
                                theme.FAINT_WALL, theme.FAINT_WALL)
            main_menu.draw(ui)
            menu.draw_tagline(ui)
            menu.draw_parade(ui)
            menu.draw_leaderboard(ui, scores)
            menu.draw_hint(ui)
            screen.blit(ui, ui_offset(screen))
        elif current == HELP:
            screens.draw_help(ui)
            screen.blit(ui, ui_offset(screen))
        elif current == SCORES:
            screens.draw_scores(ui, scores)
            screen.blit(ui, ui_offset(screen))
        else:
            data = state.all_data_to_dict()
            player = data["player"]
            ox, oy, cell = maze_view.layout(len(data["maze"][0]),
                                            len(data["maze"]),
                                            game_area(screen))

            maze_view.draw_maze(screen, data["maze"], ox, oy, cell)
            maze_view.draw_pacgums(screen, data["pacgums"],
                                   data["super_pacgums"],
                                   ox, oy, cell)

            for ghost in data["ghosts"]:
                flashing = (ghost.get("ghost_freaid", 99.0) <= 2.0
                            and int(elapsed * 6) % 2 == 0)
                entities.draw_ghost(screen, ghost, flashing, ox, oy,
                                    cell)
            entities.draw_player(screen, player, elapsed, ox, oy,
                                 cell)
            hud.draw_hud(screen, data, len(config.levels))
            if current == PAUSED:
                top = screen.get_height() // 2 - 240
                pause_menu.title_y = top + 60
                pause_menu.items_y = top + 165
                menu.dim(screen)
                menu.draw_pause_panel(screen, data["score"],
                                      min(data["level"] + 1,
                                          len(config.levels)),
                                      len(config.levels))
                pause_menu.draw(screen)
            elif current == END:
                menu.dim(screen)
                end_screen.draw(screen)
        pygame.display.flip()

    pygame.quit()
