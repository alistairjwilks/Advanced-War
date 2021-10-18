from collections import Set
from typing import Tuple, List

from components.base_component import BaseComponent

class Team(BaseComponent):
    def __init__(self,
                 name: str,
                 code: str,
                 color: Tuple[int, int, int],
                 is_light_color: bool = False # will use for yellow team, so we can see them on light colored tiles
                 ):
        self.name = name
        self.code = code
        self.color = color


red_team = Team("Orange Star", "ORN", color=(255,128,0))

blue_team = Team("Blue Moon", "BLU", color=(0,76,153))
