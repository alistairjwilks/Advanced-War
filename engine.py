from typing import Set, Iterable, Any

import tcod
from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    def __init__(self, event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            #self.update_fov()  # now only update fov if the action demands it

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
