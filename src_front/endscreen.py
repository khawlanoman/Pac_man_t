"""End screen for game over and victory: final score and name entry."""

import pygame

from src_front import highscores, hud, theme

PANEL = pygame.Rect(0, 0, 480, 450)
FIELD = pygame.Rect(0, 0, 340, 64)


class EndScreen:
    """Shows the final score and lets the player type a name."""
    def __init__(self) -> None:
        self.won = False
        self.score = 0
        self.name = ""

    def start(self, won: bool, score: int) -> None:
        """Reset the screen for a new ending."""
        self.won = won
        self.score = score
        self.name = ""

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Edit the name. Return True when the player presses Enter."""
        if event.type != pygame.KEYDOWN:
            return False
        if event.key == pygame.K_RETURN:
            return True
        if event.key == pygame.K_BACKSPACE:
            self.name = self.name[:-1]
        elif (len(self.name) < highscores.MAX_NAME
              and event.unicode.isascii() and event.unicode.isalnum()):
            self.name += event.unicode.upper()
        return False

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the panel, the result, the score and the name field."""
        cx = screen.get_width() // 2
        panel = PANEL.copy()
        panel.center = screen.get_rect().center
        accent = theme.SUCCESS if self.won else theme.DANGER

        pygame.draw.rect(screen, theme.SURFACE, panel,
                            border_radius=theme.RADIUS_PANEL)
        pygame.draw.rect(screen, accent, panel, width=2,
                            border_radius=theme.RADIUS_PANEL)

        title = "YOU WON!" if self.won else "GAME OVER"
        sub = "CONGRATULATIONS!" if self.won else "BETTER LUCK NEXT TIME!"
        self._text(screen, title, 34, accent, cx, panel.top + 66)
        self._text(screen, sub, 9, theme.TEXT, cx, panel.top + 108)
        self._text(screen, "FINAL SCORE", 9, theme.MUTED, cx, panel.top + 145)
        self._text(screen, str(self.score), 40, theme.PRIMARY, cx, panel.top + 190)
        self._text(screen, "ENTER YOUR NAME", 9, theme.MUTED, cx, panel.top + 250)

        field = FIELD.copy()
        field.center = (cx, panel.top + 305)
        pill = field.height // 2
        pygame.draw.rect(screen, theme.BG, field, border_radius=pill)
        pygame.draw.rect(screen, theme.PRIMARY, field, width=2,
                            border_radius=pill)

        blink = "_" if pygame.time.get_ticks() // 500 % 2 == 0 else " "
        self._text(screen, self.name + blink, 20, theme.TEXT, cx, field.centery)
        self._text(screen, "ENTER - SAVE", 8, theme.MUTED, cx, panel.bottom - 36)


    def _text(self, screen: pygame.Surface, text: str, size: int,
              colour: tuple[int, int, int], x: int, y: int) -> None:
        """Draw one line of text centred on (x, y)."""
        surface = hud.font(size).render(text, True, colour)
        screen.blit(surface, surface.get_rect(center=(x, y)))
