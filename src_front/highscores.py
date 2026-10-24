"""Loads and saves the high score table."""

import json
import os

MAX_NAME = 10
MAX_ENTRIES = 10


def clean_name(raw: str) -> str:
    """Reduce typed input to a legal player name.

    Keeps only ASCII letters, digits and spaces, caps the length at
    ten characters and trims the ends. An empty result becomes a
    placeholder so the table never grows a nameless row.

    Args:
        raw: Whatever the player typed.

    Returns:
        A name safe to store and display.
    """
    kept = [c for c in raw if (c.isascii() and (c.isalnum() or c == " "))]
    return "".join(kept)[:MAX_NAME].strip() or "PLAYER"


def load(path: str) -> list[dict]:
    """Read the table from disk, tolerating any damage.

    A missing file is normal on a first run. Anything else - bad JSON,
    wrong structure, rows with missing fields - is skipped rather than
    raised, because a broken score file must never stop the game.

    Args:
        path: Path to the JSON file.

    Returns:
        Valid entries, best first, at most ten.
    """
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as handle:
            raw = json.load(handle)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(raw, list):
        return []

    entries = []
    for row in raw:
        if not isinstance(row, dict):
            continue
        name = row.get("name")
        score = row.get("score")
        if not isinstance(name, str):
            continue
        if isinstance(score, bool) or not isinstance(score, int):
            continue
        if score < 0:
            continue
        entries.append({"name": clean_name(name), "score": score})
    entries.sort(key=lambda e: e["score"], reverse=True)
    return entries[:MAX_ENTRIES]


def save(path: str, entries: list[dict]) -> bool:
    """Write the table to disk.

    Args:
        path: Path to the JSON file.
        entries: The entries to store.

    Returns:
        True on success. Failure is reported, never raised.
    """
    try:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(entries, handle, indent=2)
    except OSError:
        return False
    return True


def add(entries: list[dict], name: str, score: int) -> list[dict]:
    """Insert a score and return the new top ten.

    Args:
        entries: The current table.
        name: Raw player input; cleaned before storing.
        score: Final score; negatives are clamped to zero.

    Returns:
        A new list, best first, at most ten long.
    """
    updated = entries + [{"name": clean_name(name), "score": max(0, score)}]
    updated.sort(key=lambda e: e["score"], reverse=True)
    return updated[:MAX_ENTRIES]


def qualifies(entries: list[dict], score: int) -> bool:
    """Whether `score` earns a place in the table."""
    if len(entries) < MAX_ENTRIES:
        return True
    return score > entries[-1]["score"]

