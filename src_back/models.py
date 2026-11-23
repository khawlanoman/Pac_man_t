from pydantic import BaseModel, Field


class Levels_check(BaseModel):
    width: int= Field(gt= 6)
    height: int= Field(gt= 6)


class Game_config(BaseModel):
    highscore_filename: str= Field(default= "data/highscores.json")
    lives: int= Field(default= 3, ge = 0)
    pacgum: int= Field(default = 42, ge = 0)
    points_per_pacgum: int = Field(default = 10, ge = 0)
    points_per_super_pacgum: int = Field(default = 20, ge = 0)
    points_per_ghost: int = Field(default= 100, ge= 0)
    seed: int = Field(default = 42 ,ge=0)
    level_max_time: float= Field(default= 90.0, ge= 1)
    levels: list[Levels_check]
