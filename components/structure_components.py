from collections import Set
from typing import TYPE_CHECKING, Optional

from entity import Entity, Actor
from components.base_component import BaseComponent
from components.team import Team


class Repair(BaseComponent):
    def __init__(self, can_repair=None):
        if can_repair is None:
            can_repair = []

        self.can_repair = can_repair

    def perform(self):
        unit: Actor = self.engine.gamemap.unit_at(self.parent.x, self.parent.y)
        if unit:
            if unit.team.code == self.parent.team.code and unit.fighter.move_type in self.can_repair:
                unit.fighter.resupply()
                unit.fighter.repair(20)


class Capturable(BaseComponent):
    def __init__(self, team: Team = None):
        self.team = team
        self.capture_points = 20

    def capture(self, captor: Optional[Actor]):
        pass


class Production(BaseComponent):
    pass


class Passive(BaseComponent):
    pass


class Income(BaseComponent):
    pass
