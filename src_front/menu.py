"""The main menu screen."""

import pygame

from src_front import hud
from src_front import hud
from src_front import sprites
from src_front import theme

MAIN_ITEMS = [
    ("START GAME", "start"),
    ("HIGH SCORES", "scores"),
    ("INSTRUCTIONS", "help"),
    ("QUIT", "quit"),
]

PAUSE_ITEMS = [
    ("RESUME", "resume"),
    ("MAIN MENU", "menu"),
    ("QUIT", "quit"),
]


def dim(screen: pygame.Surface, alpha: int = 190) -> None:
    """Darken the whole screen, for drawing a modal over the game.

    Args:
        screen: Surface to darken.
        alpha: 0 is invisible, 255 is opaque.
    """
    veil = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    veil.fill((6, 7, 12, alpha))
    screen.blit(veil, (0, 0))

def draw_tagline(screen: pygame.Surface) -> None:
    """Draw the line under the title."""
    text = hud.font(12).render("GHOSTS! MORE GHOSTS!", True, theme.MUTED)
    screen.blit(text, text.get_rect(center=(screen.get_width() // 2, 174)))


def draw_parade(screen: pygame.Surface) -> None:
    """draw the four ghosts followed by pacman"""
    x = 213
    for name in ("ghost_blinky", "ghost_pinky", "ghost_inky", "ghost_clyde"):
        screen.blit(sprites.load(name, 40), (x, 224))
        x += 54
    screen.blit(sprites.load("pacman_2", 40), (x + 24, 224))


def draw_leaderboard(screen: pygame.Surface, scores: list[dict]) -> None:
    """Draw the best three scores in a rounded card.

    Args:
        screen: Surface to draw on.
        scores: Entries from highscores.load(), best first.
    """
    card = pygame.Rect(0, 530, 360, 136)
    card.centerx = screen.get_width() // 2
    pygame.draw.rect(screen, theme.SURFACE, card, border_radius=theme.RADIUS_PANEL)
    pygame.draw.rect(screen, theme.BORDER, card, width=theme.BORDER_WIDTH, border_radius=theme.RADIUS_PANEL)
    head = hud.font(9).render("BEST", True, theme.MUTED)
    screen.blit(head, head.get_rect(center=(card.centerx, card.top + 26)))

    if not scores:
        empty = hud.font(9).render("No scores yet", True, theme.MUTED)
        screen.blit(empty, empty.get_rect(center=card.center))
        return

    for i, entry in enumerate(scores[:3]):
        y = card.top + 52 + i * 26
        colour = theme.PRIMARY if i == 0 else theme.TEXT
        rank = hud.font(11).render(f"{i + 1}.", True, theme.MUTED)
        name = hud.font(11).render(entry["name"], True, colour)
        score = hud.font(11).render(str(entry["score"]), True, colour)
        screen.blit(rank, (card.left + 30, y))
        screen.blit(name, (card.left + 70, y))
        screen.blit(score, score.get_rect(topright=(card.right - 30, y)))



def draw_hint(screen: pygame.Surface) -> None:
    """draw the controls reminder at the bottom"""
    text = hud.font(8).render("ARROWS / MOUSE - ENTER - Q TO QUIT", True, theme.MUTED)
    screen.blit(text, text.get_rect(center=(screen.get_width() // 2, 760)))



class Menu:
    """A menu driven by both keyboard and mouse."""

    def __init__(self, items: list[tuple[str, str]], title: str,
             title_y: int = 124, items_y: int = 322) -> None:
        """Build a menu.

        Args:
            items: Pairs of (label, action name).
            title: Heading shown above the list.
            title_y: Vertical centre of the title, in pixels.
            items_y: Vertical centre of the first item, in pixels.
        """
        self.items = items
        self.title = title
        self.title_y = title_y
        self.items_y = items_y
        self.index = 0
        self.rects: list[pygame.Rect] = []

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Translate one event into an action name.

        Args:
            event: One pygame event.

        Returns:
            The chosen action, or None if nothing was chosen.
        """

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.index = (self.index - 1) % len(self.items)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.index = (self.index + 1) % len(self.items)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.items[self.index][1]
            elif event.key == pygame.K_ESCAPE:
                return "quit"
            elif event.key == pygame.K_h:
                return "help"
            elif event.key == pygame.K_q:
                return "quit"

        elif event.type == pygame.MOUSEMOTION:
            hovered = self._item_at(event.pos)
            if hovered is not None:
                self.index = hovered

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = self._item_at(event.pos)
            if clicked is not None:
                return self.items[clicked][1]

        return None

    def _item_at(self, pos: tuple[int, int]) -> int | None:
        """Return the index of the item under `pos`, if any."""
        for i, rect in enumerate(self.rects):
            if rect.collidepoint(pos):
                return i
        return None

    def draw(self, screen: pygame.Surface) -> None:
        """Paint the title and the list of choices."""
        center = screen.get_width() // 2
        self.rects = []

        title_font = hud.font(56)
        shadow = title_font.render(self.title, True, theme.SHADOW)
        title = title_font.render(self.title, True, theme.PRIMARY)
        pos = title.get_rect(center=(center, self.title_y))
        screen.blit(shadow, pos.move(5, 6))
        screen.blit(title, pos)

        for i, (label, _) in enumerate(self.items):
            selected = i == self.index
            colour = theme.PRIMARY if selected else theme.MUTED
            text = hud.font(20).render(label, True, colour)
            rect = text.get_rect(center=(center, self.items_y + i * 50))
            screen.blit(text, rect)
            self.rects.append(rect.inflate(80, 20))
            if selected:
                cursor = sprites.load("pacman_1", 28)
                screen.blit(cursor, (rect.left - 46, rect.centery - 14))
