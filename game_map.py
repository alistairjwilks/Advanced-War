from __future__ import annotations

from time import sleep
from typing import Iterable, Iterator, Optional, TYPE_CHECKING, Tuple

import numpy as np  # type: ignore
from tcod.console import Console

from entity import Actor, Cursor
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class GameMap:
    def __init__(self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = (), no_fog: bool = False):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.plains, order="F")

        self.engine = engine
        self.entities = set(entities)  # initialise the given entities into a set. entities belong to the map now

        self.no_fog = no_fog
        self.visible = np.full((width, height), fill_value=no_fog, order="F")  # track which tiles are visible now
        # self.explored = np.full((width, height), fill_value=False, order="F")  # track tiles we've seen - not for AW

    @property
    def actors(self) -> Iterator[Actor]:
        """ Iterate over the map's actors"""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    @property
    def units(self) -> Iterator[Actor]:
        """ Iterate over the map's actors"""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

    def get_neighbours(self, x: int, y: int) -> [(int, int)]:
        return [xy for xy in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] if self.in_bounds(*xy)]

    def get_blocking_entity_at_location(self, location_x: int, location_y: int) -> Optional[Entity]:
        for entity in self.entities:
            if (
                    entity.blocks_movement
                    and entity.x == location_x
                    and entity.y == location_y
            ):
                return entity
        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def draw(self, x: int, y: int, console: Console):
        on_visible = "light" if self.visible[x, y] else "dark"
        for entity in self.entities - {self.engine.cursor}:
            if (entity.x, entity.y) == (x, y) and entity.is_visible:
                console.print(x, y, string=entity.char, fg=entity.color, bg=entity.bg_color)
                return

        console.print(x=x, y=y,
                      string=chr(self.tiles[x, y][on_visible]["ch"]),
                      fg=tuple(self.tiles[x, y][on_visible]["fg"]),
                      bg=tuple(self.tiles[x, y][on_visible]["bg"]))

    def entity_at(self, x, y) -> Optional[Entity]:
        for entity in self.entities - {self.engine.cursor}:
            if (entity.x, entity.y) == (x, y):
                return entity

    def draw_highlighted(self, x: int, y: int, highlight_color: Tuple[int, int, int], console: Console):
        entity = self.entity_at(x, y)
        if entity and entity.is_visible:
            console.print(x, y, string=entity.char, bg=highlight_color, fg=entity.color)
        else:
            tile = self.tiles[x, y]["dark"]
            console.print(x, y, string=chr(tile["ch"]), fg=tuple(tile["fg"]), bg=highlight_color)

    def draw_inverted(self, x: int, y: int, console: Console):
        on_visible = "light" if self.visible[x, y] else "dark"
        entity = self.entity_at(x, y)
        if entity and entity.is_visible:
            console.print(x, y, string=entity.char, bg=entity.color, fg=entity.bg_color)
            return

        console.print(x=x, y=y,
                      string=chr(self.tiles[x, y][on_visible]["ch"]),
                      bg=tuple(self.tiles[x, y][on_visible]["fg"]),
                      fg=tuple(self.tiles[x, y][on_visible]["bg"]))

    def draw_selected(self, console: Console):
        selected: Entity = self.engine.cursor.selection
        if selected:
            self.draw_highlighted(selected.x, selected.y, (255, 255, 255), console)

    def quick_render(self, console: Console):
        # quickly redraw just the changes
        self.engine.render_mode = "None"
        self.engine.context.present(console)

    def flash(
            self,
            x: int,
            y: int,
            console: Console,
            char: str = "!",
            fg: Tuple[int, int, int] = (255, 255, 0),
            bg: Tuple[int, int, int] = (255, 0, 0),
            time: float = 0.2
    ):
        console.print(x=x, y=y,
                      string=char,
                      bg=bg, fg=fg)
        if self.engine.context:
            self.engine.context.present(console)
            sleep(time)
        self.render(console)

    def render(self, console: Console) -> None:
        """
        renders the map
        if a tile is Visible (True iin the visible array) its light version is shown
        otherwise show the dark version.
        later on, we will implement a fog of war toggle
        """
        # select works through the conditions and assigns the corresponding choice, like a switch statement, skipping
        # once a condition is met
        """
        # original function with shroud
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )
        """
        self.engine.update_fov()
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.no_fog or self.visible],
            choicelist=[self.tiles["light"]],
            default=self.tiles["dark"]
        )

        for entity in self.entities - {self.engine.cursor}:
            # Only show visible entities, and not the cursor
            if self.in_bounds(entity.x, entity.y):
                if self.visible[entity.x, entity.y]:
                    self.draw(entity.x, entity.y, console)
        cursor = self.engine.cursor
        path = None
        if cursor.selection and cursor.selection.fighter:

            candidate_tiles = []
            attack_tiles = []
            candidate_targets = []

            highlight_attack = (255, 200, 200)  # light red
            highlight_attack_blind = (125, 100, 100)  # dull red
            highlight_move = (209, 224, 255)  # light blue
            highlight_move_blind = (104, 112, 127)  # dull blue
            highlight_target = (255, 0, 0)  # full red

            if self.engine.render_mode == "move":
                candidate_tiles = cursor.selection.fighter.calculate_move_range()
                if cursor.selection.fighter.is_direct_fire:
                    attack_tiles = cursor.selection.fighter.attack_range()
                    candidate_targets = cursor.selection.fighter.attack_targets()
                path = cursor.selection.ai.get_path_to(cursor.x, cursor.y)
                # print("from gamemap", path)
            elif self.engine.render_mode == "attack" and not cursor.selection.fighter.attack_used and not cursor.selection.fighter.is_direct_fire:
                candidate_targets = cursor.selection.fighter.attack_targets()
                attack_tiles = cursor.selection.fighter.attack_range()
            else:
                candidate_tiles = []

            for tile in candidate_tiles:
                if self.visible[tile]:
                    self.draw_highlighted(*tile, highlight_color=highlight_move, console=console)
                else:
                    self.draw_highlighted(*tile, highlight_move_blind, console)
            if any(attack_tiles):
                for at_tile in attack_tiles:
                    if self.visible[at_tile]:
                        self.draw_highlighted(*at_tile, highlight_attack, console)
                    else:
                        self.draw_highlighted(*at_tile, highlight_attack_blind, console)
            if any(candidate_targets):
                for target in candidate_targets:
                    self.draw_highlighted(*target, highlight_target, console)

        if path and len(path) <= cursor.selection.fighter.movement:
            for tile in path:
                self.draw_highlighted(*tile, highlight_color=(255, 200, 200), console=console)

        self.draw_highlighted(cursor.x, cursor.y, (255, 255, 255), console)
        self.draw_selected(console)
