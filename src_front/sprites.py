"""Loads and caches sprite images."""

import os

import pygame

SPRITE_DIR = os.path.join("assets", "sprites")

_cashe: dict[tuple[str, int], pygame.Surface] = {}


def load(name: str, size: int) -> pygame.Surface:
    """Return a sprite scaled to `size` pixels square.

    Images are loaded and scaled once, then cached. Scaling inside the
    draw loop would redo this work 60 times a second.

    Args:
        name: File name without extension, e.g. "pacman_0".
        size: Target width and height in pixels.

    Returns:
        The scaled surface, with transparency preserved.
    """

    key = (name, size)
    if key in _cashe:
        return _cashe[key]

    path = os.path.join(SPRITE_DIR, f"{name}.png")
    image = pygame.image.load(path).convert_alpha()
    scaled = pygame.transform.scale(image, (size, size))
    _cashe[key] = scaled
    return scaled
