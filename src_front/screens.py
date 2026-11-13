"""Full pages reached from the main menu: instructions and high scores."""

import pygame

from src_front import hud, theme

PANEL = pygame.Rect(60, 100, 600, 600)

CONTROLS = [
    ("ARROWS / WASD", "MOVE"),
    ("ESC", "PAUSE"),
    ("C", "SKIP LEVEL (CHEAT)"),
    ("L", "EXTRA LIFE (CHEAT)"),
]

RULES = [
    "EAT EVERY PELLET TO CLEAR A LEVEL",
    "BIG PELLETS MAKE GHOSTS EDIBLE",
    "TOUCH A GHOST AND YOU LOSE A LIFE",
    "FINISH BEFORE THE TIMER RUNS OUT",
    "CLEAR ALL LEVELS TO WIN",
]



def draw_panel(screen: pygame.Surface, title: str) -> None:
    """Draw the rounded card with its title and the back hint."""
    pygame.draw.rect(screen, theme.SURFACE, PANEL, border_radius=theme.RADIUS_PANEL)
    pygame.draw.rect(screen, theme.BORDER, PANEL, width=theme.BORDER_WIDTH, border_radius=theme.RADIUS_PANEL)

    text = hud.font(32).render(title, True, theme.PRIMARY)
    shadow = hud.font(32).render(title, True, theme.SHADOW)
    pos = text.get_rect(center=(PANEL.centerx, PANEL.top + 60))
    screen.blit(shadow, pos.move(4, 4))
    screen.blit(text, pos)

    hint = hud.font(8).render("ESC / ENTER - BACK", True, theme.MUTED)
    screen.blit(hint, hint.get_rect(center=(PANEL.centerx, PANEL.bottom - 36)))


def draw_help(screen: pygame.Surface) -> None:
    """Draw the controls and the rules of the game."""
    draw_panel(screen, "HOW TO PLAY")
    left = PANEL.left + 50
    y = PANEL.top + 120

    head = hud.font(12).render("CONTROLS", True, theme.PRIMARY)
    screen.blit(head, (left, y))
    y += 34
    for key, action in CONTROLS:
        key_text = hud.font(10).render(key, True, theme.TEXT)
        action_text = hud.font(10).render(action, True, theme.MUTED)
        screen.blit(key_text, (left, y))
        screen.blit(action_text, (left + 200, y))
        y += 28

    y += 24
    head = hud.font(12).render("RULES", True, theme.PRIMARY)
    screen.blit(head, (left, y))
    y += 34
    for rule in RULES:
        screen.blit(hud.font(10).render(rule, True, theme.TEXT), (left, y))
        y += 28

    
def draw_scores(screen: pygame.Surface, scores: list[dict]) -> None:
    """Draw the top 10 scores, best first.

    Args:
        screen: Surface to draw on.
        scores: Entries from highscores.load(), already sorted.
    """
    draw_panel(screen, "HIGH SCORES")

    if not scores:
        empty = hud.font(12).render("NO SCORES YET", True, theme.MUTED)
        screen.blit(empty, empty.get_rect(center=PANEL.center))
        return

    left = PANEL.left + 60
    right = PANEL.right - 60
    y = PANEL.top + 120

    for title, x in (("RANK", left), ("NAME", left + 90)):
        screen.blit(hud.font(9).render(title, True, theme.MUTED), (x, y))
    head = hud.font(9).render("SCORE", True, theme.MUTED)
    screen.blit(head, head.get_rect(topright=(right, y)))
    y += 32

    for i, entry in enumerate(scores[:10]):
        colour = theme.PRIMARY if i == 0 else theme.TEXT
        rank = hud.font(12).render(f"{i + 1}.", True, theme.MUTED)
        name = hud.font(12).render(entry["name"], True, colour)
        score = hud.font(12).render(str(entry["score"]), True, colour)
        screen.blit(rank, (left, y))
        screen.blit(name, (left + 90, y))
        screen.blit(score, score.get_rect(topright=(right, y)))
        y += 36
