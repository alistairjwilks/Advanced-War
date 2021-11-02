from __future__ import annotations

import queue
from queue import Queue
from typing import TYPE_CHECKING, Iterable

from tcod.context import Context
from tcod.console import Console

import render_functions
from components import team
from components.team import Team
from input_handlers import EventHandler, MainGameEventHandler
from render_functions import render_stats
from message_log import MessageLog
if TYPE_CHECKING:
    from entity import Actor, Cursor
    from game_map import GameMap



class Engine:
    gamemap: GameMap = None
    root_console: Console = None
    context: Context = None

    def __init__(self, player: Cursor, players: Iterable[Team], render_mode: str = "none"):
        self.cursor = player
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.mouse_location = (0,0)
        self.render_mode = render_mode
        self.player_list = players
        self.remaining_players = queue.Queue(maxsize=len(players))
        for player in players:
            self.remaining_players.put(player)
        self.active_player: Team = self.remaining_players.get()
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

    def render(self, console: Console) -> None:
        """ Now we just tell the map to render itself to our console, since it holds the entities now"""
        console.clear()
        self.gamemap.render(console)
        render_functions.render_unit_panel(console, self.cursor)

        render_functions.render_quick_info(console, self.cursor, 0, console.height - 1)
        self.message_log.render(
            console,
            x=40,
            y=35,
            width=20,
            height=5
        )



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
