from typing import Set, Iterable, Any

import tcod
from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.entities = entities
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

            self.update_fov()  # update the fov before the next action

    def update_fov(self) -> None:
        """ Recompute the visible area based on the current player's POV"""
        # will need to be updated to draw for multiple units, and for the taxicab movement mechanic
        # self.game_map.visible[:] = compute_fov(
        #     self.game_map.tiles["vision"],
        #     (self.player.x, self.player.y),
        #     radius=4,
        #     algorithm=tcod.FOV_DIAMOND
        # )

        # for each entity in the (active) player's team
        #   calculate line of sight - let the unit have a look()
        #   method? or at least a vision stat
        # set the tiles to visible
        self.game_map.visible[:] = False
        for entity in self.entities:
            # self.game_map.visible[entity.x,entity.y] = True
            vision = 4  # entity.vision
            for i in range(-vision, vision + 1):
                for j in range(-vision, vision + 1):
                    if (abs(i) + abs(j) <= vision and
                            self.game_map.in_bounds(entity.x + i, entity.y + i)):
                        self.game_map.visible[entity.x + i, entity.y + j] = True

        # no exploration in AW
        # self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            # visible entities only
            if self.game_map.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()
