from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

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
        self.tiles = np.full((width, height), fill_value=tile_types.mountain, order="F")

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

    def get_actor_at_location(self, x:int, y:int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y ==y:
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
                console.print(x, y, string=entity.char, fg=entity.color, bg=tuple(self.tiles[x, y][on_visible]["bg"]))
                return
        else:
            console.print(x=x, y=y,
                          string=chr(self.tiles[x, y][on_visible]["ch"]),
                          fg=tuple(self.tiles[x, y][on_visible]["fg"]),
                          bg=tuple(self.tiles[x, y][on_visible]["bg"]))

    def draw_inverted(self, x: int, y: int, console: Console):
        on_visible = "light" if self.visible[x, y] else "dark"
        for entity in self.entities - {self.engine.cursor}:
            if (entity.x, entity.y) == (x, y):
                console.print(x, y, string=entity.char, bg=entity.color, fg=tuple(self.tiles[x, y][on_visible]["bg"]))
                return

            console.print(x=x, y=y,
                          string=chr(self.tiles[x, y][on_visible]["ch"]),
                          bg=tuple(self.tiles[x, y][on_visible]["fg"]),
                          fg=tuple(self.tiles[x, y][on_visible]["bg"]))

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
                console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)
        cursor = self.engine.cursor

        if cursor.selection:
            candidate_tiles = cursor.selection.fighter.move_range()
            for tile in candidate_tiles:
                self.draw_inverted(*tile, console)

            if (cursor.x, cursor.y) in candidate_tiles:
                self.draw(cursor.x, cursor.y, console)
            else:
                self.draw_inverted(cursor.x, cursor.y, console)
        else:
            self.draw_inverted(cursor.x, cursor.y, console)



