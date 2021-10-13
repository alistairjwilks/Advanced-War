from __future__ import annotations
from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console

from input_handlers import EventHandler

if TYPE_CHECKING:
    from entity import Entity
    from game_map import GameMap


class Engine:
    game_map: GameMap = None

    def __init__(self):
        self.event_handler: EventHandler = EventHandler(self)

    def update_fov(self) -> None:
        """ Recompute the visible area based on the current player's POV"""

        #   for each entity (in the active player's team)
        #   calculate line of sight - let the unit have a look()
        #   method? or at least a vision stat
        #   set the tiles to visible
        self.game_map.visible[:] = False
        for entity in self.game_map.entities:
            vision = 4  # entity.vision
            for i in range(-vision, vision + 1):
                for j in range(-vision, vision + 1):
                    if abs(i) + abs(j) <= vision and self.game_map.in_bounds(entity.x + i, entity.y + j):
                        try:
                            self.game_map.visible[entity.x + i, entity.y + j] = True
                        except(IndexError):
                            pass

        # no exploration in AW
        # self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        """ Now we just tell the map to render itself to our console, since it holds the entities now"""
        self.game_map.render(console)
