from __future__ import annotations

import numpy as np

import entity_factories
import tile_types
import tcod
import random

from typing import List, Iterator, Tuple, TYPE_CHECKING

from components import team

if TYPE_CHECKING:
    from engine import Engine

from entity import Entity, Cursor
from game_map import GameMap


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        """ Measured from the top left corner"""
        self.x1 = x
        self.x2 = x + width
        self.y1 = y
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """
    return the inner area of this room as a 2d array index
        for the dungeon generation, our rectangular room includes a solid wall on the outside,
        the slice will return x1 <= a < x2, so our inner function is the floor space in the room
        """
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """ return true if this room intersects another"""
        return (
                self.x1 < other.x2
                and self.x2 >= other.x1
                and self.y1 <= other.y2
                and self.y2 >= other.y1
        )


def tunnel_between(
        start: Tuple[int, int],
        end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """ Return an L-shaped tunnel between two points"""

    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50-50
        corner_x, corner_y = x2, y1  # horizontal first
    else:
        corner_x, corner_y = x1, y2

    # generate the coordinates for the tunnel
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_aw_map(
        engine: Engine
) -> GameMap:
    """ generate a hardcoded test map"""
    aw_map = GameMap(
        engine=engine,
        width=20,
        height=10,
        entities=[]
    )

    for i in range(aw_map.width):
        aw_map.tiles[i, 0] = tile_types.mountain
        aw_map.tiles[i, 1:3] = tile_types.woods
        aw_map.tiles[i, aw_map.height - 1] = tile_types.mountain

    entity_factories.tank(team.red_team).spawn(aw_map, x=4, y=4)
    entity_factories.tank(team.red_team).spawn(aw_map, x=4, y=5)
    entity_factories.tank(team.red_team).spawn(aw_map, x=4, y=6)

    entity_factories.tank(team.blue_team).spawn(aw_map, x=7, y=4)
    entity_factories.tank(team.blue_team).spawn(aw_map, x=7, y=5)
    entity_factories.tank(team.blue_team).spawn(aw_map, x=7, y=6)
    return aw_map
