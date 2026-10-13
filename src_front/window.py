"""Opens the game window and runs the main loop."""

import pygame

WIDTH = 720
HEIGHT = 720
FPS = 60
BACKGROUND = (8, 9, 16)


def run() -> None:
    """Open the window and keep it open until the user closes it."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.quit:
                running = False

        screen.fill(BACKGROUND)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit