from mazegenerator import MazeGenerator
from src_back.maze_loader import loader
from src_back import parsing
from src_back.game import constants
from src_back.game.gamestate import Game_state

from src_back.game.constants import Game_status



data = parsing.pars_config()
level= data.levels[0]
width = level.width
height = level.height
seed = data.seed
maze = loader.load_maze(width,height,seed)

# neighbors = loader.get_valid_neighbors(maze,5,5 )

center_maze = loader.get_center_position(width, height)

corner_position = loader.get_corner_positions(width, height)

super_pacgums = loader.place_super_pacgums(width, height)
ghosts_place = loader.place_ghosts(width, height)
place_pacgum= loader.place_pacgums(maze, 100, corner_position, 42)


count = 0
for row in maze:
    for cell in row:
        if cell == 15:
            count+=1

def print_maze(maze: MazeGenerator, place_pacgum:set,corner_position:list,center_maze) -> None:
    grid = maze.maze
    height = len(grid)
    width = len(grid[0])

   
    print("+" + "---+" * width)

    for y in range(height):

        line = "|"

        for x in range(width):
            if (x,y) ==  center_maze:
                cell = " @ "
    
            elif (x,y) in ghosts_place:
                cell = " G "
            elif (x,y) in place_pacgum:
                cell = " . "
            elif (x,y) in super_pacgums:
                cell = " & "
            else:
                cell = "   "


            if grid[y][x] & 2:
                line += cell + "|"
            else:
                line += cell + " "

        print(line)

        line = "+"

        for x in range(width):
            if grid[y][x] & 4:
                line += "---+"
            else:
                line += "   +"

        print(line)

count_levels = len(data.levels)
maze_grid= MazeGenerator(size=(width,height),perfect=False,seed=seed)
print_maze(maze_grid,place_pacgum,corner_position,center_maze)

game_state =  Game_state(maze, width, height, place_pacgum, super_pacgums, center_maze,
                        ghosts_place,0,count_levels, data.level_max_time,Game_status.PLAYING,
                        False,{},data,[])


game_state.initialize_level()