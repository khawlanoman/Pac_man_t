"""Draws the player and the ghosts."""

import math

import pygame

from src_front.maze_view import cell_center

PLAYER_COLOUR = (255, 214, 0)

GHOST_COLOURS = {
    "blinky": (255, 74, 74),
    "pinky": (255, 146, 205),
    "inky": (76, 221, 237),
    "clyde": (255, 168, 62),
}

GHOST_FRIGHTENED = (46, 68, 214)
EYE_WHITE = (248, 250, 255)


def draw_player(screen: pygame.Surface, px: float, py: float,
                origin_x: int, origin_y: int, size: int) -> None:
    """Draw the player as a yellow circle.

    Args:
        screen: Surface to draw on.
        px: Player x in cell units (may be fractional).
        py: Player y in cell units.
        origin_x: Pixel x of the maze's left edge.
        origin_y: Pixel y of the maze's top edge.
        size: Cell width and height in pixels.
    """
    cx = origin_x + px * size + size / 2
    cy = origin_y + py * size + size / 2
    pygame.draw.circle(screen,
                       PLAYER_COLOUR, (cx, cy),
                       size / 2)


def draw_ghost(screen: pygame.Surface, ghost: dict,
               origin_x: int, origin_y: int, size: int) -> None:
    """Draw one ghost as a coloured dome with eyes.

    Args:
        screen: Surface to draw on.
        ghost: One entry from the snapshot's "ghosts" list.
        origin_x: Pixel x of the maze's left edge.
        origin_y: Pixel y of the maze's top edge.
        size: Cell width and height in pixels.
    """
    cx = origin_x + ghost["x"] * size + size / 2
    cy = origin_y + ghost["y"] * size + size / 2

    if ghost["state"] == "frightened":
            colour = GHOST_FRIGHTENED
    else:
         colour = GHOST_COLOURS.get(ghost["ghosts_type"], (200, 200, 200))

    radius = int(size * 0.36)
    pygame.draw.circle(screen, colour, (int(cx), int(cy)), radius)

    eye = max(2, size // 12)
    for size in (-1, 1):
        pygame.draw.circle(screen, EYE_WHITE,
                           (int(cx + size * radius * 0.4),
                            int(cy - radius / 4)),
                           eye)