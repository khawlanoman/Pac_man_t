"""Loads and caches sprite images."""

import os

import pygame

SPRITE_DIR = os.path.join("assets", "sprites")

_cache: dict[tuple[str, int], pygame.Surface] = {}


def load(name: str, size: int) -> pygame.Surface:
    """Return the sprite scaled to size, or a placeholder if it is missing."""
    key = (name, size)
    if key not in _cache:
        try:
            image = pygame.image.load(f"assets/sprites/{name}.png")
            image = pygame.transform.smoothscale(image.convert_alpha(),
                                                 (size, size))
        except (pygame.error, OSError):
            image = _placeholder(size)
        _cache[key] = image
    return _cache[key]


def _placeholder(size: int) -> pygame.Surface:
    """Return a pink circle, so a missing sprite is visible but harmless."""
    image = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(image, (255, 0, 255), (size // 2, size // 2),
                       size // 2)
    return image
