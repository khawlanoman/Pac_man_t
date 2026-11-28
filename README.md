*This project has been created as part of the 42 curriculum by khnoman, aayat.*

# 🟡  👻 Pac_Man 🟡  👻


## Description


Pac-Man is a recreation of the classic arcade game developed in Python. The player navigates through a maze, collects pac-gums, and avoids ghosts to complete each level. The game includes multiple levels, AI-controlled ghosts, collision detection, score tracking, and a highscore system.

### Features

+ Player Movement: Control Pac-Man with the arrow keys or WASD and navigate through the maze.

+ Ghost AI: Four ghosts: they chase Pac-Man with a greedy algorithm and run away when frightened

    + Blinky

    + Pinky

    + Inky

    + Clyde

+ Ghost States: Ghosts can switch between Chase, Frightened, Eaten, and Waiting states.

+ Pac-Gums: Collect Pac-Gums to increase your score.

+ Super Pac-Gums: Placed in the 4 corners; they temporarily frighten ghosts, allowing Pac-Man to eat them.

+ Multiple Levels: Progress through 10 levels. Level 1 uses the fixed seed from the config, every next level is a new random maze.

+ Level Timer: Each level has a time limit (90 s by default). When it runs out, Pac-Man loses a life and the timer restarts.

+ Scoring System: Earn points by collecting Pac-Gums and Super Pac-Gums and eating frightened ghosts. The score never decreases.

+ Lives System: Start with three lives.

+ Highscore: Track and display the best game scores.

+ Game States: Menu, Playing, Paused, Game Over, and Victory.

+ Cheats: Extra options to help the evaluation:

    | Key | Cheat |
    |-----|-------|
    | C   | Skip the current level |
    | L   | Add an extra life |
    | F   | Freeze / unfreeze the ghosts |
    | T   | Turbo speed on / off |
    | I   | Invincible on / off |

## Instructions

### Requirements
- Python 3.10 or later
- `pip` and `make`

### Installation
1. Clone the repository:

2.   Install the required dependencies (this also installs the assigned maze generator from the `.whl` file at the root):

        -   make install

### Execution
1. Run the game using:

    -   make run

    or directly:

    -   python3 pac-man.py config.json

### Controls

| Key | Action |
|-----|--------|
| Arrows / WASD | Move |
| ESC | Pause (resume, main menu, quit) |
| Enter / mouse | Choose in menus |

### Other Makefile rules

| Rule | What it does |
|------|--------------|
| `make debug` | Run the game with `pdb` |
| `make lint` | `flake8` + `mypy` with the subject flags |
| `make lint-strict` | `flake8` + `mypy --strict` |
| `make clean` | Remove caches |
| `make package` | Build the standalone game into `dist/` (PyInstaller) |

### Packaged build
The packaged game is available on itch.io (private link): **<add your itch.io link here>**

To rebuild it: `make package`, then run `./pacman config.json` from the `dist/` folder.
The build uses `pacman.spec` at the root of the repository, and `HOW_TO_PLAY.md` is shipped inside the package.


### Configuration

The game takes exactly one argument: a JSON configuration file.

- Lines starting with `#` are comments and are ignored.
- Unknown keys are ignored.
- Missing or invalid values are replaced by a safe default, a clear message is printed, and the game continues.

Example:

```
{
    # number of lives at the start
    "lives": 3,
    "pacgum": 10,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 20,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90,
    "highscore_filename": "data/highscores.json",
    "levels": [
        {"width": 16, "height": 15},
        {"width": 18, "height": 18}
    ]
}
```

The default configuration includes:

| Key                       | Meaning                          | Default Value          |
|---------------------------|----------------------------------|------------------------|
| `lives`                   | number of lives                  | 3                      |
| `pacgum`                  | pac-gums per level               | 10                     |
| `points_per_pacgum`       | pac-gum score                    | 10                     |
| `points_per_super_pacgum` | super pac-gum score              | 20                     |
| `points_per_ghost`        | eaten ghost score                | 100                    |
| `seed`                    | seed of the first level          | 42                     |
| `level_max_time`          | level time in seconds            | 90                     |
| `highscore_filename`      | where highscores are saved (.json) | `data/highscores.json` |
| `levels`                  | list of `{"width", "height"}`, at least 10 levels, minimum size 9 x 9 | 10 levels of 15 x 15 |


### Highscore

The highscore system keeps track of player performance.

It is designed to:

Record completed game scores.

Compare scores to identify the highest results.

Display the leaderboard.

The scoring system rewards players for collecting Pac-Gums, collecting Super Pac-Gums, and eating frightened ghosts.

How it works:

- Scores are stored in a JSON file (`highscore_filename` in the config, `data/highscores.json` by default). The folder is created if it does not exist.
- The table is loaded when the game starts and saved when a game ends (win or lose), after the player types a name.
- Only the top 10 scores are kept, sorted from best to worst.
- Names: max 10 characters, letters, digits and spaces only. Scores are non-negative integers.
- A missing, empty or broken file never stops the game: invalid rows are skipped and the game starts with what is valid.
- The best scores are shown on the main menu, and the full top 10 on the High Scores page.

Why JSON: it is part of the Python standard library, easy to read and edit by hand during the evaluation, and the table is small, so a database would add complexity for no benefit.

### Maze Generation

The game uses the A-Maze-ing maze generation project to generate the game mazes.

Maze generation is responsible for creating the maze structure and defining the available paths and walls.

The generated maze is represented as a grid, where each cell contains information about its surrounding walls.

How we use the assigned package (`mazegenerator` 2.1.0, from another group, used as-is):

- The package is shipped as `mazegenerator-2.1.0-py3-none-any.whl` at the root of the repository; `make install` installs it with pip through `requirements.txt`.
- Each level calls `MazeGenerator(size=(width, height), perfect=False, seed=seed)` and reads `.maze`. `perfect=False` adds loops, so Pac-Man can escape the ghosts.
- Each cell is a number with 4 wall bits: `1` up, `2` right, `4` down, `8` left. A cell equal to `15` is fully closed (the "42" pattern drawn by the generator) and is drawn as a solid block.
- Our loader (`src_back/maze_loader/loader.py`) adapts to this format: `can_move()` checks the wall bit of the current cell and the opposite wall of the next cell.
- Level 1 uses the `seed` from the config; the other levels use a random seed.


## Implementation

- **Game loop**: runs at 60 FPS. Each frame reads the events, updates the game, then draws the whole screen and calls `display.flip()`.
- **Movement**: positions are in tiles; `speed x dt` makes the speed the same on any computer. A new direction is stored and applied when Pac-Man reaches the centre of a tile and there is no wall.
- **Ghosts**: at each tile they choose the open direction (no U-turn) that is closest to Pac-Man (Manhattan distance), a greedy algorithm. When frightened they choose the direction that moves them away. An eaten ghost goes back to its corner, waits, then chases again.
- **Collisions**: a ghost touches Pac-Man when their distance is under half a tile.
- **Screens**: a small state machine (menu, playing, paused, help, scores, end) decides which events to handle and what to draw.
- **Config**: validated with `pydantic` models; invalid values are replaced by defaults.
- **Assets**: all files are loaded through one helper (`src_front/paths.py`), so the game also works from another folder and inside the PyInstaller build.
- **Sound**: effects are played by comparing the game state before and after each update (lives, pac-gums, ghosts). If there is no audio device, the game runs silently.


## General Software Architecture

```
pac-man.py                 reads the argument, turns every error into a clear message
├── src_front/             everything the player sees and touches (pygame)
│   ├── window.py          main loop, input, screen switching
│   ├── maze_view.py       draws walls and pac-gums
│   ├── entities.py        draws Pac-Man and the ghosts
│   ├── hud.py             score, lives, level, timer
│   ├── menu.py, screens.py, endscreen.py   menus, help, scores, name entry
│   ├── highscores.py      load / save the top 10
│   ├── sound.py, sprites.py, theme.py, paths.py
└── src_back/              game rules (no pygame)
    ├── parsing.py, models.py      config reading and validation
    ├── maze_loader/loader.py      maze generator + walls + placements
    └── game/
        ├── gamestate.py   Game_state: maze, player, ghosts, score, timers
        ├── player.py      PlayerState
        ├── ghost.py       GhostState
        └── constants.py   enums: directions, ghost states, game status
```

- `window.py` creates one `Game_state` and calls its methods every frame (`move_player`, `move_ghosts`, `check_ghost_collision`, ...).
- To draw, the front reads a snapshot dictionary from `Game_state.all_data_to_dict()`. The front never changes the rules, and the back never imports pygame.


## Project Management

The work was split by layer: the front-end (`src_front`, Makefile, README, assets, packaging) and the back-end (`src_back`, configuration, maze loader). We tracked tasks, tested each feature against the subject, and logged the bugs we found and fixed.

All documents (timeline, team organisation, choices, risks, test plan, blocking points) are in [[project_management/]([project_management/).


## Resources

[pac_mac logic ](https://www.geekslop.com/old-school/2020/the-logic-and-programming-behind-pac-man-all-the-crazy-cool-stuff-you-ever-wanted-to-know-about-how-the-classic-pac-man-game-works-under-the-hood)   
[Greedy algorithm](https://plainenglish.io/python/greedy-algorithm-in-python-4b66e250d088)   
[pygame-ce documentation](https://pyga.me/docs/)   
[pydantic documentation](https://docs.pydantic.dev/)   
[PyInstaller documentation](https://pyinstaller.org/)

### Ai usage
-  Understanding programming concepts and algorithms (game loop, greedy ghost movement, how pygame draws).
-  All AI suggestions were tested and reviewed by us before being kept.