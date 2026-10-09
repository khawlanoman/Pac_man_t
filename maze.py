from mazegenerator import MazeGenerator
from src_back.maze_loader import loader
from src_back import parsing
from src_back.game import constants




data = parsing.pars_config()
level= data.levels[0]
width = level.width
height = level.height
seed = data.seed
maze = loader.load_maze(width,height,seed)

neighbors = loader.get_valid_neighbors(maze,5,5 )

center_maze = loader.get_center_position(15,15)

ghosts_position = loader.get_corner_positions(15,15)

print(center_maze)
print(ghosts_position)
