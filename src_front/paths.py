"""Finds asset files, both from source and inside a packaged build."""

import os
import sys


def asset(*parts: str) -> str:
    """Return the full path of a file inside the assets folder.

    Args:
        *parts: Path pieces under assets/, e.g. "sprites", "pacman_1.png".

    Returns:
        An absolute path that works from any folder and in a
        PyInstaller build.
    """
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base = getattr(sys, "_MEIPASS", root)
    return os.path.join(base, "assets", *parts)
