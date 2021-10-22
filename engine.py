from __future__ import annotations

import queue
from queue import Queue
from typing import TYPE_CHECKING, Iterable

from tcod.context import Context
from tcod.console import Console

from components import team
from components.team import Team
from input_handlers import EventHandler

if TYPE_CHECKING:
    from entity import Actor, Cursor
    from game_map import GameMap


class Engine:
    gamemap: GameMap = None

    def __init__(self, player: Cursor, players: Iterable[Team], render_mode: str = "none"):
        self.cursor = player
        self.event_handler: EventHandler = EventHandler(self)
        self.render_mode = render_mode
        self.player_list = players
        self.remaining_players = queue.Queue(maxsize=len(players))
        for player in players:
            self.remaining_players.put(player)
        self.active_player :Actor = self.remaining_players.get()
        # self.remaining_players.put(self.active_player)
        print(self.active_player.name)


    def update_fov(self) -> None:
        """ Recompute the visible area based on the current player's POV"""

        #   for each entity (in the active player's team)
        #   calculate line of sight - let the unit have a look()
        #   method? or at least a vision stat
        #   set the tiles to visible - replace with tcod path stuff
        if self.gamemap.no_fog:
            return
        self.gamemap.visible[:] = False
        for actor in [actor for actor in self.gamemap.actors if actor.team.code == self.active_player.code]:
            vision = actor.vision
            for i in range(-vision, vision + 1):
                for j in range(-vision, vision + 1):
                    if abs(i) + abs(j) <= vision and self.gamemap.in_bounds(actor.x + i, actor.y + j):
                        try:
                            self.gamemap.visible[actor.x + i, actor.y + j] = True
                        except(IndexError):
                            pass

        # no exploration in AW
        # self.gamemap.explored |= self.gamemap.visible

    def render(self, console: Console, context: Context) -> None:
        """ Now we just tell the map to render itself to our console, since it holds the entities now"""
        self.gamemap.render(console)
        # skip printing the player, we use a cursor inside of the map

    def next_player(self):
        print(self.active_player.name)
        ending_player = self.active_player
        self.active_player = self.remaining_players.get()
        self.remaining_players.put(ending_player)
        self.new_turn(self.active_player)
        print(self.active_player.name)

    def new_turn(self, player: Team) -> None:
        for entity in [entity for entity in set(self.gamemap.actors) if entity.team.code == player.code]:
            if entity.ai:
                entity.ai.perform()
