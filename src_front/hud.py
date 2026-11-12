"""Draws the heads-up display: score, lives, level and timer."""

import pygame
from src_front import sprites, theme


FONT_PATH = "assets/fonts/game_font_1.TTF"
CARD = pygame.Rect(16, 18, 688, 80)
_fonts: dict[int, pygame.font.Font] = {}


def font(size: int) -> pygame.font.Font:
    """Return a cached font of the given size.

    Building a font object is slow enough to cause visible stutter if
    done inside the draw loop, so each size is created once and reused.
    """
    if size not in _fonts:
        _fonts[size] = pygame.font.Font(FONT_PATH, size)
    return _fonts[size]


def draw_label(screen: pygame.Surface, title: str, value: str,
               x: int, y: int, align: str = "left",
               colour: tuple[int, int, int] = theme.TEXT) -> None:
    """Draw a small caption with a larger value beneath it.

    Args:
        screen: Surface to draw on.
        title: The caption, e.g. "SCORE".
        value: The value shown below it.
        x: Horizontal anchor in pixels.
        y: Top of the caption in pixels.
        align: "left", "center" or "right", relative to x.
    """
    cap = font(9).render(title, True, theme.MUTED)
    val = font(18).render(value, True, colour)

    for surface, offset in [(cap, 0), (val, 22)]:
        rect = surface.get_rect()
        if align == "center":
            rect.centerx = x
        elif align == "right":
            rect.right = x
        else:
            rect.left = x
        rect.top = y + offset
        screen.blit(surface, rect)


def draw_lives(screen: pygame.Surface, lives: int, x: int, y: int) -> None:
    """Draw one small Pac-Man icon per remaining life."""
    icon = sprites.load("pacman_1", 22)
    for i in range(lives):
        screen.blit(icon, (x + i * 30, y))


def draw_hud(screen: pygame.Surface, data: dict, total_levels: int) -> None:
    """Draw the HUD as a floating rounded card at the top of the window.

    Args:
        screen: Surface to draw on.
        data: The snapshot from all_data_to_dict().
        total_levels: How many levels the config defines.
    """
    pygame.draw.rect(screen, theme.SURFACE, CARD,
                     border_radius=theme.RADIUS_PANEL)
    pygame.draw.rect(screen, theme.BORDER, CARD, width=theme.BORDER_WIDTH,
                     border_radius=theme.RADIUS_PANEL)

    top = CARD.top + 22
    draw_label(screen, "SCORE", str(data["score"]), CARD.left + 28, top)
    draw_lives(screen, data["player"]["lives"], CARD.left + 170, top + 8)
    draw_label(screen, "LEVEL", f"{data['level'] + 1}/{total_levels}",
               CARD.left + 450, top, align="center")

    seconds = max(0, int(data["timer"] + 0.999))
    clock = f"{seconds // 60}:{seconds % 60:02d}"
    colour = theme.DANGER if seconds <= 10 else theme.TEXT
    draw_label(screen, "TIME", clock, CARD.right - 28, top,
                align="right", colour=colour)
