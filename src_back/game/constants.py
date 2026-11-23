from enum import Enum


class Directions(Enum):
    UP = (0, -1, 1)
    DOWN = (0, 1, 4)
    LEFT = (-1, 0, 8)
    RIGHT = (1, 0, 2)


class Opposite(Enum):
    UP = "DOWN"
    DOWN = "UP"
    LEFT = "RIGHT"
    RIGHT = "LEFT"


class Cell(Enum):
    WALL = 0
    WAY = 1
    PACGUM = 2
    SUPER_PACGUM = 3


class Game_status(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    VICTORY = "victory"


class Ghost_state(Enum):
    CHASE = "chase"
    WAITING = "waiting"
    FRIGHTENED = "frightened"
    EATEN = "eaten"


class Ghost_type(Enum):
    BLINKY = "blinky"
    PINKY = "pinky"
    INKY = "inky"
    CLYDE = "clyde"
