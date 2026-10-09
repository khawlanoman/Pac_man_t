from pydantic import BaseModel, Field

class Levels_check(BaseModel):
    width: int = Field(gt=6)
    height: int = Field(gt=6)


class Game_config(BaseModel):
    highscore_filename: str
    lives: int = Field(ge=0)
    pacgum: int = Field(ge=0)
    points_per_pacgum: int = Field(ge=0)
    points_per_super_pacgum: int = Field(ge=0)
    points_per_ghost: int = Field(ge=0)
    seed: int
    level_max_time:float = Field(ge=1)
    levels: list[Levels_check]
    