from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING
import numpy as np
import tcod

from actions import Action, AttackAction, MovementAction, WaitAction, BumpAction, UnitEndTurnAction
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor, Structure


class BaseAI(Action, BaseComponent):
    entity: Actor

    def perform(self) -> None:
        raise NotImplementedError()

    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        """
        Compute and return a path to the destination,
        otherwise return an empty list
        """

        cost = np.array(self.entity.gamemap.tiles["move"][self.entity.move_type], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            # for entities on valid tiles that block us, and we can see them
            if entity.blocks_movement and \
                    entity.team and \
                    not entity.team.code == self.entity.team.code and \
                    entity.is_visible:
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


class StructureAI(BaseAI):
    def __init__(self, entity: Structure):
        super().__init__(entity)

    def perform(self) -> None:
        pass # do nothing for now