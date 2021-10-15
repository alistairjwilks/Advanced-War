from collections import Set
from typing import Tuple, List

from components.base_component import BaseComponent
from entity import Entity


class Fighter(BaseComponent):
    def __init__(self,
                 hp: int,
                 defense: int,
                 power: int,
                 movement: int = 3,
                 atk_range: int = 1,
                 vision: int = 0,
                 min_range: int = 1,
                 fuel: int = 99
                 ):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power
        self.movement = movement
        self.vision = vision
        self.move_used = False  # handle units taking turns
        self.attack_used = False
        self.atk_range = atk_range
        self.min_range = min_range
        self.fuel_max = fuel
        self.fuel_remaining = fuel

    @property  # a getter
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        # keep hp between 0 and max
        self._hp = max(0, min(value, self.max_hp))

    def move(self, dx, dy) -> None:
        if (self.entity.x + dx, self.entity.y + dy) in self.move_range():
            self.entity.x += dx
            self.entity.y += dy
            self.move_used = True
            self.fuel_remaining -= self.path_cost(dx, dy)
            print(self.entity.name + " fuel:"+str(self.fuel_remaining))

    def path_cost(self, dx, dy) -> int:
        path = self.entity.ai.get_path_to(self.entity.x + dx, self.entity.y + dy)
        return sum(self.engine.gamemap.tiles[step[0], step[1]]["move"] for step in path)

    def move_range(self) -> List[Tuple[int, int]]:
        candidate_tiles: List[Tuple[int, int]] = [(self.entity.x, self.entity.y)]

        if self.move_used:  # one move per turn
            return candidate_tiles
        move_range = min(self.movement, self.fuel_remaining)
        for dx in range(-move_range, move_range + 1):
            for dy in range(-move_range, move_range + 1):
                if abs(dx) + abs(dy) <= move_range:
                    if self.engine.gamemap.in_bounds(self.entity.x + dx, self.entity.y + dy):
                        if 0 < self.path_cost(dx, dy) <= move_range:
                            candidate_tiles.append((self.entity.x + dx, self.entity.y + dy))

        return candidate_tiles

    def is_in_range(self, target: Entity) -> bool:
        if self.min_range <= abs(self.entity.x - target.x) + abs(self.entity.y - target.y) <= self.atk_range:
            return True
        return False

    def attack_range(self) -> List[Tuple[int, int]]:
        candidate_tiles: List[Tuple[int, int]] = []
        for dx in range(-self.atk_range, self.atk_range + 1):
            for dy in range(-self.atk_range, self.atk_range + 1):
                if self.min_range <= abs(dx) + abs(dy) <= self.atk_range:
                    if self.engine.gamemap.in_bounds(self.entity.x + dx, self.entity.y + dy):
                        candidate_tiles.append((self.entity.x + dx, self.entity.y + dy))
        return candidate_tiles
