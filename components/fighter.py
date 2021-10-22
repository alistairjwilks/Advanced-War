import math
from collections import Set
from typing import Tuple, List

import numpy as np

from components.base_component import BaseComponent
from entity import Entity
from game_map import GameMap


class Fighter(BaseComponent):

    def __init__(self,
                 hp: int = 100,
                 movement: int = 3,
                 atk_range: int = 1,
                 vision: int = 0,
                 min_range: int = 1,
                 fuel: int = 99,
                 fuel_cost: int = 0,
                 code: str = "NIL",
                 primary_wpn: bool = False,
                 secondary_wpn: bool = False,
                 ammo: int = 0,
                 move_type: str = "NIL"
                 ):
        self.max_hp = hp
        self._hp = hp
        self.movement = movement
        self.vision = vision
        self.move_used = False  # handle units taking turns
        self.attack_used = False
        self.atk_range = atk_range
        self.min_range = min_range
        self.fuel_max = fuel
        self._fuel = fuel
        self.fuel_cost = fuel_cost
        self.code = code
        self.primary_wpn = primary_wpn
        self.secondary_wpn = secondary_wpn
        self.ammo_max = ammo
        self._ammo = ammo
        self.move_type = move_type
        self.move_range = []

    @property  # a getter
    def hp(self) -> int:
        return self._hp

    @property
    def displayed_hp(self) -> int:
        return math.ceil(self._hp / 10)

    @property
    def fuel(self) -> int:
        return self._fuel

    @property
    def ammo(self) -> int:
        return self._ammo

    @fuel.setter
    def fuel(self, value: int) -> None:
        self._fuel = max(0, min(value, self.fuel_max))

    @ammo.setter
    def ammo(self, value: int) -> None:
        self._ammo = max(0, min(value, self.ammo_max))

    @property
    def is_direct_fire(self):
        if self.min_range>1 or self.atk_range > 1:
            return False
        else:
            return True

    @hp.setter
    def hp(self, value: int) -> None:
        # keep hp between 0 and max
        self._hp = max(0, min(value, self.max_hp))

    @property
    def damage_mod(self) -> float:
        # each CO will have a set of offence modifiers for each unit, with a lookup like the damage table
        try:
            return self.entity.team.damage_mod[self.code]
        except KeyError:
            return 1.0

    @property
    def defence(self):
        try:
            return self.entity.team.defence_mod[self.code]
        except KeyError:
            return 100

    @property
    def terrain_defence(self) -> int:
        x, y = self.entity.x, self.entity.y
        return self.entity.gamemap.tiles[x, y]["defence"]

    @property
    def team_code(self)->str:
        return self.entity.team.code

    @property
    def gamemap(self) -> GameMap:
        return self.entity.gamemap

    def move(self, dx, dy) -> None:
        if (self.entity.x + dx, self.entity.y + dy) in self.move_range:
            cost, path = self.path_cost(dx, dy)
            self.entity.x += dx
            self.entity.y += dy
            self.move_used = True
            self._fuel -= cost
            # print(cost, path)
            print(self.entity.name + " fuel:" + str(self._fuel))
            self.calculate_move_range()

    def path_cost(self, dx, dy) -> (int, List[Tuple[int, int]]):
        path = self.entity.ai.get_path_to(self.entity.x + dx, self.entity.y + dy)
        # print(f"moving from {self.entity.x, self.entity.y} to {self.entity.x + dx, self.entity.y + dy}")
        # print(path)
        cost = sum(self.engine.gamemap.tiles[step[0], step[1]]["move"][self.move_type] for step in path)
        # print(cost)
        return cost, path

    def calculate_move_range(self) -> List[Tuple[int, int]]:
        candidate_tiles: List[Tuple[int, int]] = [(self.entity.x, self.entity.y)]

        if not self.move_used:  # one move per turn
            max_tiles = min(self.movement, self._fuel)
            for dx in range(-max_tiles, max_tiles + 1):
                for dy in range(-max_tiles, max_tiles + 1):
                    if abs(dx) + abs(dy) <= max_tiles:
                        if self.engine.gamemap.in_bounds(self.entity.x + dx, self.entity.y + dy):
                            if 0 < self.path_cost(dx, dy)[0] <= max_tiles:
                                candidate_tiles.append((self.entity.x + dx, self.entity.y + dy))

        self.move_range = candidate_tiles
        return self.move_range

    def is_in_range(self, target: Entity) -> bool:
        if self.min_range <= abs(self.entity.x - target.x) + abs(self.entity.y - target.y) <= self.atk_range:
            return True
        return False

    def attack_targets(self) -> List[Tuple[int, int]]:
        candidate_targets: List[Tuple[int, int]] = []
        for tile in self.attack_range():
            if self.is_direct_fire:
                for target in self.gamemap.get_neighbours(*tile):
                    actor = self.gamemap.get_actor_at_location(*target)
                    if actor and actor.team.code != self.team_code:
                        candidate_targets.append(target)
            else:
                actor = self.gamemap.get_actor_at_location(*tile)
                if actor and actor.team.code != self.team_code:
                    candidate_targets.append(tile)

        return candidate_targets

    def attack_range(self) -> List[Tuple[int, int]]:
        candidate_tiles: List[Tuple[int, int]] = []

        # show attackable targets for direct fire units
        if self.is_direct_fire:
            for tile in self.move_range:
                for neighbour in self.gamemap.get_neighbours(*tile):
                    actor = self.gamemap.get_actor_at_location(*neighbour)
                    if actor and actor.team.code != self.team_code:
                        candidate_tiles.append(tile)

        # highlight range for indirect units, as no move and fire
        else:
            for dx in range(-self.atk_range, self.atk_range + 1):
                for dy in range(-self.atk_range, self.atk_range + 1):
                    if self.min_range <= abs(dx) + abs(dy) <= self.atk_range:
                        if self.engine.gamemap.in_bounds(self.entity.x + dx, self.entity.y + dy):
                            candidate_tiles.append((self.entity.x + dx, self.entity.y + dy))
        return candidate_tiles

    def take_damage(self, damage):
        self.hp = self.hp - damage
        if self.hp == 0:
            self.die()
        # todo CO Power meter

    def die(self):
        self.entity.ai = None
        self.engine.gamemap.entities.remove(self.entity)

