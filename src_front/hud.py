"""Draws the heads-up display: score, lives, level and timer."""

import pygame
from src_front import sprites, theme


FONT_PATH = "assets/fonts/game_font_1.TTF"
_fonts: dict[int, pygame.font.Font] = {}
MAX_LIFE_ICONS = 4


def card_rect(screen: pygame.Surface) -> pygame.Rect:
    """The HUD card: full window width minus a 16 px margin each side."""
    return pygame.Rect(16, 18, screen.get_width() - 32, 80)


def draw_lives(screen: pygame.Surface, lives: int, x: int, y: int) -> None:
    """Draw up to four Pac-Man icons, then "+N" for any extra lives."""
    icon = sprites.load("pacman_1", 22)
    for i in range(min(lives, MAX_LIFE_ICONS)):
        screen.blit(icon, (x + i * 30, y))
    if lives > MAX_LIFE_ICONS:
        extra = font(9).render(f"+{lives - MAX_LIFE_ICONS}", True,
                               theme.MUTED)
        screen.blit(extra, (x + MAX_LIFE_ICONS * 30, y + 6))


def draw_cheat_badge(screen: pygame.Surface, label: str,
                     x: int, y: int) -> None:
    """Draw a small red pill with the given label, centred on (x, y)."""
    text = font(8).render(label, True, theme.DANGER)
    pill = text.get_rect(center=(x, y)).inflate(16, 10)
    pygame.draw.rect(screen, theme.DANGER, pill, width=1,
                     border_radius=pill.height // 2)
    screen.blit(text, text.get_rect(center=pill.center))


def font(size: int) -> pygame.font.Font:
    """Return a cached font of the given size.

    Building a font object is slow enough to cause visible stutter if
    done inside the draw loop, so each size is created once and reused.
    """
    if size not in _fonts:
        try:
            _fonts[size] = pygame.font.Font(FONT_PATH, size)
        except (pygame.error, OSError):
            _fonts[size] = pygame.font.Font(None, size)
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


def draw_hud(screen: pygame.Surface, data: dict, total_levels: int) -> None:
    """Draw the HUD as a floating rounded card at the top of the window.

    Args:
        screen: Surface to draw on.
        data: The snapshot from all_data_to_dict().
        total_levels: How many levels the config defines.
    """
    card = card_rect(screen)
    pygame.draw.rect(screen, theme.SURFACE, card,
                     border_radius=theme.RADIUS_PANEL)
    pygame.draw.rect(screen, theme.BORDER, card, width=theme.BORDER_WIDTH,
                     border_radius=theme.RADIUS_PANEL)

    top = card.top + 22
    draw_label(screen, "SCORE", str(data["score"]), card.left + 28, top)
    draw_lives(screen, data["player"]["lives"], card.left + 170, top + 8)
    level = min(data["level"] + 1, total_levels)
    draw_label(screen, "LEVEL", f"{level}/{total_levels}",
               card.right + 238, top, align="center")

    seconds = max(0, int(data["timer"] + 0.999))
    clock = f"{seconds // 60}:{seconds % 60:02d}"
    colour = theme.DANGER if seconds <= 10 else theme.TEXT
    draw_label(screen, "TIME", clock, card.right - 28, top,
               align="right", colour=colour)

    if data["cheat_mode"]:
        active = [name[0].upper() for name, on in data["cheats"].items()
                  if on]
        label = " ".join(["CHEAT"] + active)
        draw_cheat_badge(screen, label, card.right - 328, card.centery)
