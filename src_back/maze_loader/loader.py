from mazegenerator import MazeGenerator
from src_back.game.constants import Directions
from random import Random
from ..game import constants
from typing import List, Set, Tuple, Any


def load_maze(width: int, height: int, seed: int) -> Any:
    """this function load the maze from mazegenerator"""
    grid = MazeGenerator(size=(width, height), perfect=False, seed=seed)
    return grid.maze


def has_wall(maze: List[List[int]], x: int, y: int,
             direction: Directions) -> bool:
    """this function is check if the  cell has
    the walls is return true or false"""
    cell_bit = maze[y][x]
    dire_bit = direction.value[2]
    return (cell_bit & dire_bit) != 0


def can_move(maze: List[List[int]], x: int, y: int,
             direction: Directions | None) -> bool:
    """this function is check if the cell has the
    wall in this direction  to can move or not """
    if direction is None:
        return False
    width = len(maze[0])
    height = len(maze)

    dx = direction.value[0]
    dy = direction.value[1]
    nx = x + dx
    ny = y + dy

    if nx < 0 or nx >= width or ny < 0 or ny >= height:
        return False
    opposite = constants.Opposite[direction.name].value
    oppo = Directions[opposite]
    if has_wall(maze, nx, ny, oppo):
        return False
    if has_wall(maze, x, y, direction):
        return False
    return True


def get_valid_neighbors(maze: List[List[int]], x: int,
                        y: int) -> list[Tuple[int, int]]:
    """this function is for check the neighbors"""
    neighbors_valid = []
    for d in Directions:
        dx = d.value[0]
        dy = d.value[1]
        if can_move(maze, x, y, d):
            neighbors_valid.append((x+dx, y+dy))
    return neighbors_valid


def get_center_position(maze: List[List[int]], width: int,
                        height: int) -> Tuple[int, int]:
    """ take the first pacman position  in the center of maze"""
    center_x = width // 2
    center_y = height // 2

    if maze[center_y][center_x] == 15:
        neighbors = ((0, 1), (-1, 0), (1, 0), (0, -1))
        valid_neighbors = []

        for i in neighbors:
            nx, ny = center_x + i[0], center_y + i[1]
            if maze[ny][nx] != 15:
                valid_neighbors.append((nx, ny))
            else:
                continue
        return (valid_neighbors[0])
    return (center_x, center_y)


def get_corner_positions(width: int, height: int) -> List[Tuple[int, int]]:
    """ this method for the corner of maze
    for the position of super pacgums """
    positions = [(0, 0),
                 (width - 1, 0),
                 (0, height - 1),
                 (width - 1, height - 1)]
    return positions


def place_super_pacgums(width: int, height: int) -> List[Tuple[int, int]]:
    """ this method for  the position of super
    pacgums by  get_corner_positions"""
    list_place = get_corner_positions(width, height)

    return list_place


def place_ghosts(width: int, height: int) -> List[Tuple[int, int]]:
    """  this method for ghost positions """
    positions = [(0, 0),
                 (width - 1, 0),
                 (0, height - 1),
                 (width - 1, height - 1)]
    return positions


def place_pacgums(maze: List[List[int]], count: int, exclude_po: List[list],
                  seed: int) -> Set[Tuple[int, int]]:
    """ this method for  distribution
    the pacgums inside the maze'"""

    width = len(maze[0])
    height = len(maze)

    places = []

    for y in range(height - 1):
        for x in range(width - 1):
            if maze[y][x] == 15:
                continue
            elif (x, y) in exclude_po:
                continue
            places.append((x, y))
    if count > len(places):
        print("error pacgum number ")
        count = len(places)

    rendom_gen = Random(seed)
    rendom_gen.shuffle(places)
    pacgums = set(places[0: count])
    return pacgums
