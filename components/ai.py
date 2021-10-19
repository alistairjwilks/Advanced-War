from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING
import numpy as np
import tcod

from actions import Action, AttackAction, MovementAction, WaitAction, BumpAction, UnitEndTurnAction
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor


class BaseAI(Action, BaseComponent):
    entity: Actor

    def perform(self) -> None:
        raise NotImplementedError()

    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        """
        Compute and return a path to the destination,
        otherwise return an empty list
        """

        cost = np.array(self.entity.gamemap.tiles["move"], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            # for entities on valid tiles that block us,
            if entity.blocks_movement or cost[entity.x, entity.y] == 0:
                cost[entity.x, entity.y] = 0
                # increase the cost of trying to path through another unit, to encourage flanking
                # we can set this to check the team of the entity later

        graph = tcod.path.SimpleGraph(cost=cost, cardinal=1, diagonal=0)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))  # start position
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        return [(index[0], index[1]) for index in path]


class UnitAI(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        return UnitEndTurnAction(self.entity).perform()


class TutorialEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.cursor
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = abs(dx) + abs(dy)  # manhattan distance

        # if self.engine.gamemap.visible[self.entity.x, self.entity.y]:

        self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return BumpAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
            ).perform()

        return WaitAction(self.entity).perform()

