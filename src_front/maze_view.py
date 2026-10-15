"""Draws maze cells from their wall bitmask."""

import pygame

WALL_COLOUR = (62, 104, 232)
WALL_WIDTH = 4
PACGUM_COLOUR = (255, 222, 173)
SUPER_COLOUR = (255, 186, 74)


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


def draw_maze(screen: pygame.Surface, maze: list[list[int]],
              origin_x: int, origin_y: int, size: int) -> None:
    """Draw every cell of the maze.

    Args:
        screen: Surface to draw on.
        maze: Grid of wall bitmasks, indexed maze[y][x].
        origin_x: Pixel x of the maze's left edge.
        origin_y: Pixel y of the maze's top edge.
        size: Cell width and height in pixels.
    """
    for y, row in enumerate(maze):
        for x, mask in enumerate(row):
            draw_cell(screen, mask,
                      origin_x + x * size,
                      origin_y + y * size,
                      size)


def cell_center(cx: int, cy: int, origin_X: int, origin_Y: int,
                size: int) -> tuple[int, int]:
    """Return the pixel at the centre of cell (cx, cy)."""
    return (origin_X + cx * size + size // 2,
            origin_Y + cy * size + size // 2)


def draw_pacgums(screen: pygame.Surface,
                 pacgums: list[list[bool]],
                 super_pacgums: list[tuple[int, int]],
                 origin_x: int, origin_y: int, size: int) -> None:
    """Draw the remaining pellets.

    Args:
        screen: Surface to draw on.
        pacgums: Cell coordinates of ordinary pellets.
        super_pacgums: Cell coordinates of power pellets.
        origin_x: Pixel x of the maze's left edge.
        origin_y: Pixel y of the maze's top edge.
        size: Cell width and height in pixels.
    """
    small = max(2, size // 10)
    big = max(4, size // 4)

    for cx, cy in pacgums:
        pygame.draw.circle(
            screen, PACGUM_COLOUR,
            cell_center(cx, cy, origin_x, origin_y, size),
            small
        )
    for cx, cy in super_pacgums:
        pygame.draw.circle(
            screen, SUPER_COLOUR,
            cell_center(cx, cy, origin_x, origin_y, size),
            big)
