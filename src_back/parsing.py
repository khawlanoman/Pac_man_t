import json
from pydantic import ValidationError
from .models import Game_config
from typing import Any


def pars_config(file: str) -> Any:

    try:
        with open(file, "r") as f:
            data = json.load(f)

    except json.JSONDecodeError as e:
        print("invalid json syntax:", e)
        return

    try:
        data_arr = data
        pop_list = []
        for k, v in data_arr.items():
            if k.startswith("#"):
                pop_list.append(k)

        for i in pop_list:
            data_arr.pop(i)

        t_check = Game_config.model_validate(data_arr)
        return t_check
    except ValidationError as er:
        print(f"invalid config:{er}")
