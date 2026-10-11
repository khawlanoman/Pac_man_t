from .constants import Directions, Ghost_type, Ghost_state

class GhostState:
    def __init__(self,x:float=0.0,y:float=0.0, direction:Directions= Directions.LEFT,
                 ghost_type:Ghost_type= Ghost_type.BLINKY,state:Ghost_state= Ghost_state.SCATTER,
                 my_corner:tuple[int,int]=(0,0),
                 respawn_time:float=0.0,speed:float=4.0) -> None:

                 self.x = x 
                 self.y = y 
                 self.direction = direction
                 self.ghost_type = ghost_type
                 self.state = state
                 self.my_corner =my_corner
                 self.respawn_time = respawn_time
                 self.speed = speed
                 