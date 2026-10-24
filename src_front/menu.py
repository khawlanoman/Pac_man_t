"""The main menu screen."""

import pygame

from src_front import hud

ACCENT = (255, 214, 10)
MUTED = (128, 139, 176)

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


class Menu:
    """A menu driven by both keyboard and mouse."""

    def __init__(self, items: list[tuple[str, str]], title: str) -> None:
        """Build a menu.

        Args:
            items: Pairs of (label, action name).
            title: Heading shown above the list.
        """
        self.items = items
        self.title = title
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

        title = hud.font(44).render(self.title, True, ACCENT)
        screen.blit(title, title.get_rect(center=(center, 140)))

        for i, (label, _) in enumerate(self.items):
            colour = ACCENT if i == self.index else MUTED
            text = hud.font(22).render(label, True, colour)
            rect = text.get_rect(center=(center, 300 + i * 56))
            screen.blit(text, rect)
            self.rects.append(rect.inflate(40, 20))

            if i == self.index:
                pygame.draw.polygon(screen, ACCENT, [
                    (rect.left - 30, rect.centery - 8),
                    (rect.left - 30, rect.centery + 8),
                    (rect.left - 16, rect.centery),
                ])
