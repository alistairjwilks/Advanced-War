from collections import Set
from typing import Tuple, List

from components.base_component import BaseComponent


class Fighter(BaseComponent):
    def __init__(self,
                 hp: int,
                 defense: int,
                 power: int,
                 movement: int = 3,
                 atk_range: int = 1,
                 vision: int = 0
                 ):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power
        self.movement = movement
        self.vision = vision
        

    @property  # a getter
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        # keep hp between 0 and max
        self._hp = max(0, min(value, self.max_hp))

    def move_range(self) -> List[Tuple[int, int]]:
        candidate_tiles: List[Tuple[int, int]] = []
        for dx in range(-self.movement, self.movement + 1):
            for dy in range(-self.movement, self.movement + 1):
                if abs(dx) + abs(dy) <= self.movement:
                    if self.engine.gamemap.in_bounds(self.entity.x + dx, self.entity.y + dy):
                        path = self.entity.ai.get_path_to(self.entity.x + dx, self.entity.y+dy)
                        path_cost = sum(self.engine.gamemap.tiles[step[0], step[1]]["move"] for step in path)
                        if 0 < path_cost <= self.movement:
                            candidate_tiles.append((self.entity.x + dx, self.entity.y + dy))

        return candidate_tiles




