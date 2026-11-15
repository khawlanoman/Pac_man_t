"""Sound effects and music. Every function is safe to call with no audio."""

import pygame

SOUND_DIR = "assets/sounds"
MUSIC_DIR = "assets/music"

EFFECTS = {
    "chomp": 0.25,
    "power": 0.6,
    "eat_ghost": 0.7,
    "death": 0.7,
    "move": 0.4,
    "select": 0.5,
}

MUSIC_VOLUME = 0.4
DUCKED_VOLUME = 0.15
SETTINGS = {"music": True, "effects": True}

_sounds: dict[str, pygame.mixer.Sound] = {}


def init() -> None:
    """Start the mixer and load every sound; stay silent if that fails."""
    try:
        pygame.mixer.init()
    except pygame.error:
        return
    for name, volume in EFFECTS.items():
        _load(name, f"{SOUND_DIR}/{name}.wav", volume)
    _load("chase", f"{MUSIC_DIR}/chase.ogg", MUSIC_VOLUME)


def _load(name: str, path: str, volume: float) -> None:
    """Load one sound into the cache, skipping it if the file is bad."""
    try:
        sound = pygame.mixer.Sound(path)
    except (pygame.error, FileNotFoundError):
        return
    sound.set_volume(volume)
    _sounds[name] = sound


def play(name: str) -> None:
    """Play one effect once; do nothing if it failed to load."""
    if SETTINGS["effects"] and name in _sounds:
        _sounds[name].play()


def start_music() -> None:
    """Loop the main track forever."""
    if pygame.mixer.get_init() is None:
        return
    try:
        pygame.mixer.music.load(f"{MUSIC_DIR}/menu.mp3")
    except pygame.error:
        return
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    pygame.mixer.music.play(-1)


def set_chase(on: bool) -> None:
    """Turn the chase track on or off, lowering the main music under it."""
    on = on and SETTINGS["music"]
    chase = _sounds.get("chase")
    if chase is None:
        return
    playing = chase.get_num_channels() > 0
    if on and not playing:
        chase.play(loops=-1)
        pygame.mixer.music.pause()
    elif not on and playing:
        chase.stop()
        if SETTINGS["music"]:
            pygame.mixer.music.unpause
            if not pygame.mixer.music.get_busy():
                start_music()


def toggle(kind: str) -> None:
    """Switch "music" or "effects" on or off."""
    SETTINGS[kind] = not SETTINGS[kind]
    if kind == "music" and pygame.mixer.get_init is not None:
        if SETTINGS["music"]:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
            set_chase(False)


def react(before: dict, after: dict) -> None:
    """Play the effects for what changed between two snapshots."""
    if after["lives"] < before["lives"]:
        play("death")
    if after["ghosts_home"] > before["ghosts_home"]:
        play("eat_ghost")
    if after["supers"] < before["supers"]:
        play("power")
    elif after["pacgums"] < before["pacgums"]:
        play("chomp")
