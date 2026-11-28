# 🟡 Pac-Man: How to play

## ▶️ Run
    ./pacman config.json        (Windows: pacman.exe config.json)

## 🎮 Controls
| Key | Action |
|---|---|
| Arrows / WASD | Move |
| ESC | Pause (resume, main menu, quit) |
| Enter / mouse | Choose in menus |

## 🧪 Cheats (for evaluation)
| Key | Cheat |
|---|---|
| C | Skip level |
| L | Extra life |
| F | Freeze ghosts |
| T | Turbo speed |
| I | Invincible |

## ⚙️ Configuration (config.json)
- Lines starting with `#` are comments.
- Keys: `lives`, `pacgum`, `points_per_pacgum`, `points_per_super_pacgum`,
  `points_per_ghost`, `seed`, `level_max_time`, `highscore_filename`
- `levels`: list of `{"width": W, "height": H}` (at least 10)
- Bad or missing values fall back to safe defaults.