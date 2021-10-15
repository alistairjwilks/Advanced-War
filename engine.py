from __future__ import annotations
from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console

from input_handlers import EventHandler

if TYPE_CHECKING:
    from entity import Actor, Cursor
    from game_map import GameMap


class Engine:
    gamemap: GameMap = None

    def __init__(self, player: Cursor):
        self.cursor = player
        self.event_handler: EventHandler = EventHandler(self)


    def update_fov(self) -> None:
        """ Recompute the visible area based on the current player's POV"""

        #   for each entity (in the active player's team)
        #   calculate line of sight - let the unit have a look()
        #   method? or at least a vision stat
        #   set the tiles to visible - replace with tcod path stuff
        self.gamemap.visible[:] = False
        for entity in self.gamemap.entities:
            vision = entity.vision
            for i in range(-vision, vision + 1):
                for j in range(-vision, vision + 1):
                    if abs(i) + abs(j) <= vision and self.gamemap.in_bounds(entity.x + i, entity.y + j):
                        try:
                            self.gamemap.visible[entity.x + i, entity.y + j] = True
                        except(IndexError):
                            pass

        # no exploration in AW
        # self.gamemap.explored |= self.gamemap.visible

    def render(self, console: Console, context: Context) -> None:
        """ Now we just tell the map to render itself to our console, since it holds the entities now"""
        self.gamemap.render(console)
        # skip printing the player, we use a cursor inside of the map

    def handle_enemy_turns(self) -> None:
        for entity in set(self.gamemap.actors) - {self.cursor}:
            if entity.ai:
                entity.ai.perform()

