from enum import Enum


class Directions(Enum):
    """ this class is for initialize
    the 4 directions """
    UP = (0, -1, 1)
    DOWN = (0, 1, 4)
    LEFT = (-1, 0, 8)
    RIGHT = (1, 0, 2)


class Opposite(Enum):
    """ this class is for initialize
    each direction with there oppsite"""
    UP = "DOWN"
    DOWN = "UP"
    LEFT = "RIGHT"
    RIGHT = "LEFT"


class Cell(Enum):
    """ this class is for initialize
    the cell """
    WALL = 0
    WAY = 1
    PACGUM = 2
    SUPER_PACGUM = 3


class Game_status(Enum):
    """ this class is for mode of game  """
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    VICTORY = "victory"


class Ghost_state(Enum):
    """ this class is for mode of the ghost """
    CHASE = "chase"
    WAITING = "waiting"
    FRIGHTENED = "frightened"
    EATEN = "eaten"


class Ghost_type(Enum):
    """ this class is for type of the ghost """
    BLINKY = "blinky"
    PINKY = "pinky"
    INKY = "inky"
    CLYDE = "clyde"
