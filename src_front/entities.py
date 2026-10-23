"""Draws the player and the ghosts."""


import pygame

from src_front import sprites

PLAYER_COLOUR = (255, 214, 0)
MOUTH_FPS = 10
ROTATION = {"right": 0, "up": 90, "left": 180, "down": 270}

GHOST_COLOURS = {
    "blinky": (255, 74, 74),
    "pinky": (255, 146, 205),
    "inky": (76, 221, 237),
    "clyde": (255, 168, 62),
}

GHOST_FRIGHTENED = (46, 68, 214)
EYE_WHITE = (248, 250, 255)
SPRITE_SCALE_PLAYER = 0.7
SPRITE_SCALE_GHOSTS = 0.85


def draw_player(screen: pygame.Surface, player: dict, elapsed: float,
                origin_x: int, origin_y: int, size: int) -> None:
    """Draw the player sprite, animated and facing its direction.

    Args:
        screen: Surface to draw on.
        player: The snapshot's "player" dict.
        elapsed: Seconds since the game started, driving the chomp.
        origin_x: Pixel x of the maze's left edge.
        origin_y: Pixel y of the maze's top edge.
        size: Cell width and height in pixels.
    """
    frame = int(elapsed * MOUTH_FPS) % 3
    image = sprites.load(f"pacman_{frame}", int(size * SPRITE_SCALE_PLAYER))

    angle = ROTATION.get(player["direction"], 0)
    if angle:
        image = pygame.transform.rotate(image, angle)

    cx = origin_x + player["x"] * size + size / 2
    cy = origin_y + player["y"] * size + size / 2
    screen.blit(image, image.get_rect(center=(int(cx), int(cy))))


def draw_ghost(screen: pygame.Surface, ghost: dict, flashing: bool,
               origin_x: int, origin_y: int, size: int) -> None:
    """Draw one ghost sprite for its current state."""
    state = ghost["state"]
    if state == "eaten":
        name = "ghost_eaten"
    elif state == "frightened":
        name = "ghost_flash" if flashing else "ghost_frightened"
    else:
        name = f"ghost_{ghost['ghosts_type']}"

    image = sprites.load(name, int(size * SPRITE_SCALE_GHOSTS))
    cx = origin_x + ghost["x"] * size + size / 2
    cy = origin_y + ghost["y"] * size + size / 2
    screen.blit(image, image.get_rect(center=(cx, cy)))
