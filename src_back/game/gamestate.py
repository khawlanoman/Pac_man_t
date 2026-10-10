from constants import PlayerState,Ghost_state, Ghost_type
from  models import Game_config
from random import randint
from maze_loader import loader
class Game_state:

    def __init__(self,maze:list[list[int]],width:int,height:int,pacgums:set[tuple[int,int]],
                 super_pacgums:set[tuple[int,int]],player:PlayerState,
                 ghosts:list[GhostState],score:int, level:int, timer:float,game_status:Game_state,
                 cheat_mode:bool, cheats:dict[str,bool],config:Game_config, highscores:liar[dict]) -> None:

                 self.maze = maze
                 self.width = width
                 self.height = height
                 self.pacgums = pacgums
                 self.super_pacgums =super_pacgums
                 self.player = player
                 self.ghosts = ghosts
                 self.score = score
                 self.level = level
                 self.timer = timer
                 self.game_status = game_status
                 self.cheat_mode = cheat_mode
                 self.cheats = cheats
                 self.config = config
                 self.highscores = highscores

    def initialize_level(self) -> None:
        exclude_po = []
        player_position = loader.get_center_position(self.width, self.height)
        ghosts_position = loader.place_ghosts(self.width, self.height)
        super_pacgums = loader.place_super_pacgums(self.width,self.height)
        exclude_po.extend(player_position)
        exclude_po.extend(ghosts_position)
        exclude_po.extend(super_pacgums)

        if self.level == 0:
            level_seed = self.config.seed
        else:
            level_seed = randint(1, 100)
        
        self.maze = loader.load_maze(self.width,self.height, level_seed)

        self.pacgums = loader.place_pacgums(self.maze,self.config.pacgum,exclude_po,level_seed)
        self.super_pacgums = loader.place_super_pacgums(self.width,self.height)
        
        player = PlayerState(player_position[0],player_position[1],
                             Directions.RIGHT,None,self.config.lives,self.config.score )

        blinky_ghost = GhostState(ghosts_position[0][0].ghosts_position[0][1],Directions.LEFT,
                                  Ghost_type.BLINKY,Ghost_state.SCATTER,ghosts_position[0])
        
        plinky_ghost = GhostState(ghosts_position[1][0].ghosts_position[1][1],Directions.LEFT,
                                  Ghost_type.PINKY,Ghost_state.SCATTER,ghosts_position[1])
        
        inky_ghost = GhostState(ghosts_position[2][0].ghosts_position[2][1],Directions.LEFT,
                                Ghost_type.INKY,Ghost_state.SCATTER,ghosts_position[2])
        
        clyde_ghost = GhostState(ghosts_position[3][0].ghosts_position[3][1],Directions.LEFT,
                                Ghost_type.CLYDE,Ghost_state.SCATTER,ghosts_position[3])
