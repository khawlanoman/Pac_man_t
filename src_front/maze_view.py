"""Draws maze cells from their wall bitmask."""

import pygame

WALL_COLOUR = (62, 104, 232)
WALL_WIDTH = 4


def draw_cell(screen: pygame.Surface, mask: int,
              x: int, y: int, size: int) -> None:
    """Draw the walls of one cell.

    Args:
        screen: Surface to draw on.
        mask: The cell's wall bits (1 top, 2 right, 4 bottom, 8 left).
        x: Pixel position of the cell's left edge.
        y: Pixel position of the cell's top edge.
        size: Cell width and height in pixels.
    """
    top_left = (x, y)
    top_right = (x + size, y)
    bottom_left = (x, y + size)
    bottom_right = (x + size, y + size)

    if mask & 1:
        pygame.draw.line(screen, WALL_COLOUR, top_left, top_right, WALL_WIDTH)
    if mask & 2:
        pygame.draw.line(screen, WALL_COLOUR, top_right, bottom_right,
                         WALL_WIDTH)
    if mask & 4:
        pygame.draw.line(screen, WALL_COLOUR, bottom_left, bottom_right,
                         WALL_WIDTH)
    if mask & 8:
        pygame.draw.line(screen, WALL_COLOUR, top_left, bottom_left,
                         WALL_WIDTH)
