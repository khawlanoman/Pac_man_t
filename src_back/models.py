from pydantic import BaseModel, Field, model_validator
from typing import Self, Dict, Any, List


class Levels_check(BaseModel):
    """  this class model is for  handle the width and height of levels """
    width: int = 15
    height: int = 15

    @model_validator(mode='after')
    def check_levles(self) -> Self:
        """ this method is for handel  the size of width and hieght"""
        if self.width < 9:
            print(f"Error : width= {self.width} < 9; using default 9")
            self.width = 9

        if self.height < 9:
            print(f"Error : height= {self.height} < 9; using default 9")
            self.height = 9
        return self


class Game_config(BaseModel):
    """ this class is for check all the data """
    highscore_filename: str = Field(default="data/highscores.json")
    lives: int = 3
    pacgum: int = 10
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 20
    points_per_ghost: int = 100
    seed: int = 42
    level_max_time: float = 90.0
    levels: list[Levels_check]

    @model_validator(mode='before')
    def check_levles_before(cls, data: Dict[str, int | float
                            | str | List[Levels_check]]) -> Any:
        """ this method for  check the levels before  take the data  """
        levels = data.get("levels")
        if levels is None:
            print("Error: levels are missing")

        elif not isinstance(levels, list):
            print("Error: levels must be a list")

        elif len(levels) < 10:
            print(f"Error: levels = {len(levels)} < 10")
            levels_def = []
            for _ in range(10):
                levels_def.append(Levels_check(width=15, height=15))
            data["levels"] = levels_def
        return data

    @model_validator(mode='after')
    def check_validate(self) -> Self:
        """ this method for  check the all data  """
        if self.lives < 3:
            print(f"Error : lives= {self.lives} < 3; using default 3")
            self.lives = 3

        if self.pacgum < 5:
            print(f"Error : pacgum= {self.pacgum} < 5; using default 5")
            self.pacgum = 5

        if self.points_per_pacgum < 10:
            print(f"Error : points_per_pacgum= {self.points_per_pacgum}",
                  "< 10; using default 10")
            self.points_per_pacgum = 10

        if self.points_per_super_pacgum < 20:
            print("Error : points_per_super_pacgum=",
                  f"{self.points_per_super_pacgum} < 20; using default 20")
            self.points_per_super_pacgum = 20

        if self.points_per_ghost < 100:
            print(f"Error : points_per_ghost= {self.points_per_ghost}",
                  " < 100; using default 100")
            self.points_per_super_pacgum = 100

        if self.seed < 1:
            print(f"Error : seed= {self.seed} < 1; using default 42")
            self.seed = 42

        if self.level_max_time < 60:
            print(f"Error : level_max_time= {self.level_max_time}",
                  " < 60 s; using default 90")
            self.level_max_time = 90

        return self
