"""Draws the heads-up display: score, lives, level and timer."""

import pygame

TEXT = (234, 238, 252)
MUTED = (128, 139, 176)
DANGER = (255, 94, 94)
PANEL = (16, 18, 30)

_fonts: dict[int, pygame.font.Font] = {}


def font(size: int) -> pygame.font.Font:
    """Return a cached font of the given size.

    Building a font object is slow enough to cause visible stutter if
    done inside the draw loop, so each size is created once and reused.
    """
    if size not in _fonts:
        _fonts[size] = pygame.font.SysFont("dejavusansmono", size, bold=True)
    return _fonts[size]


def draw_label(screen: pygame.Surface, title: str, value: str,
               x: int, y: int, align: str = "left") -> None:
    """Draw a small caption with a larger value beneath it.

    Args:
        screen: Surface to draw on.
        title: The caption, e.g. "SCORE".
        value: The value shown below it.
        x: Horizontal anchor in pixels.
        y: Top of the caption in pixels.
        align: "left", "center" or "right", relative to x.
    """
    cap = font(13).render(title, True, MUTED)
    val = font(22).render(value, True, TEXT)

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


def draw_hud(screen: pygame.Surface, data: dict,
             total_levels: int, height: int) -> None:
    """Draw the HUD strip across the top of the window.

    Args:
        screen: Surface to draw on.
        data: The snapshot from all_data_to_dict().
        total_levels: How many levels the config defines.
        height: Height of the strip in pixels.
    """
    width = screen.get_width()
    pygame.draw.rect(screen, PANEL, pygame.Rect(0, 0, width, height))

    pad = 28
    draw_label(screen, "SCORE", str(data["score"]), pad, 14)

    level = data["level"] + 1
    draw_label(screen, "LEVEL", f"{level} / {total_levels}",
               width // 2, 14, align="center")

    seconds = max(0, int(data["timer"] + 0.999))
    colour = DANGER if seconds <= 10 else TEXT
    clock = font(20).render(f"{seconds // 60}:{seconds % 60:02d}", True,
                            colour)
    rect = clock.get_rect(center=(width // 2, 72))
    screen.blit(clock, rect)
