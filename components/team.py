from collections import Set
from typing import Tuple, List

from components.base_component import BaseComponent

class Team(BaseComponent):
    def __init__(self,
                 name: str,
                 code: str,
                 fg_color: Tuple[int, int, int],
                 bg_color: Tuple[int, int, int],
                 is_light_color: bool = False # will use for yellow team, so we can see them on light colored tiles
                 ):
        self.name = name
        self.code = code
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.is_light_color = is_light_color


red_team = Team("Orange Star", "ORN", fg_color=(255, 128, 0), bg_color=(153, 76, 0))

blue_team = Team("Blue Moon", "BLU", fg_color=(0, 0, 204), bg_color=(0, 51, 102))

green_team = Team("Green Earth", "GRN", fg_color=(0, 204, 0), bg_color=(0, 153, 76))

black_team = Team("Black Hole", "BLK", fg_color=(32, 32, 32), bg_color=(102, 0, 51))
