from collections import Set

from components.base_component import BaseComponent
from components.team import Team
from entity import Actor


class Repair(BaseComponent):
    def __init__(self, can_repair=None):
        if can_repair is None:
            can_repair = []

        self.can_repair = can_repair

    def perform(self):
        unit: Actor = self.engine.gamemap.unit_at(self.entity.x, self.entity.y)
        if unit.team.code == self.entity.team.code and unit.fighter.move_type in self.can_repair:
            self.resupply(unit)
            if unit.fighter.hp and unit.fighter.hp < 100:
                self.repair(unit)

    def repair(self, unit: Actor):
        if unit.fighter.hp < unit.fighter.max_hp:
            hp_repaired = max(20, unit.fighter.max_hp - unit.fighter.hp)
            repair_cost = min(unit.cost * hp_repaired / 100, unit.team.funds)
            hp_repaired = min(20, int((repair_cost / unit.cost) * 100))
            unit.fighter.hp += hp_repaired
            unit.team.funds -= repair_cost

    def resupply(self, unit):
        unit.fighter.fuel = 99
        unit.fighter.ammo = 9


class Capturable(BaseComponent):
    def __init__(self, team: Team = None):
        self.team = team
        self.capture_points = 20

    def capture(self, captor: Actor):


    pass


class Production(BaseComponent):
    pass


class Passive(BaseComponent):
    pass


class Income(BaseComponent):
    pass
