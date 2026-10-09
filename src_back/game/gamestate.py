from constants import PlayerState,Ghost_state
from  models import Game_config
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

    def 