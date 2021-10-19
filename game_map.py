from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING, Tuple

import numpy as np  # type: ignore
from tcod.console import Console

from entity import Actor, Cursor
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class GameMap:
    def __init__(self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.plains, order="F")

        self.engine = engine
        self.entities = set(entities)  # initialise the given entities into a set. entities belong to the map now

        self.visible = np.full((width, height), fill_value=False, order="F")  # track which tiles are visible now
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
            if (entity.x, entity.y) == (x, y):
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
        if entity:
            console.print(x, y, string=entity.char, bg=highlight_color, fg=entity.color)
        else:
            tile = self.tiles[x, y]["dark"]
            console.print(x, y, string=chr(tile["ch"]), fg=tuple(tile["fg"]), bg=highlight_color)

    def draw_inverted(self, x: int, y: int, console: Console):
        on_visible = "light" if self.visible[x, y] else "dark"
        entity = self.entity_at(x, y)
        if entity:
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
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible],
            choicelist=[self.tiles["light"]],
            default=self.tiles["dark"]
        )

        for entity in self.entities - {self.engine.cursor}:
            # Only show visible entities, and not the cursor
            if self.visible[entity.x, entity.y]:
                self.draw(entity.x, entity.y, console)
        cursor = self.engine.cursor

        if cursor.selection and cursor.selection.fighter:
            if self.engine.render_mode == "move" and not cursor.selection.fighter.move_used:
                highlight = (209, 224, 255)
                candidate_tiles = cursor.selection.fighter.move_range()
            elif self.engine.render_mode == "attack" and not cursor.selection.fighter.attack_used:
                highlight = (255, 200, 200)
                candidate_tiles = cursor.selection.fighter.attack_range()
            else:
                candidate_tiles = []

            for tile in candidate_tiles:
                self.draw_highlighted(*tile, highlight_color=highlight, console=console)

        self.draw_highlighted(cursor.x, cursor.y, (255, 255, 255), console)
        self.draw_selected(console)
