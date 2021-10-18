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

def generate_dungeon(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        engine: Engine,
) -> GameMap:
    """
    Generate a new dungeon map of interconnected rectangular rooms.
    """
    dungeon = GameMap(
        engine=engine,
        width=map_width,
        height=map_height,
        entities=[]
    )
    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)

        # check the other rooms we have made to see if they intersect
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # invalid room placement, so move on
        # otherwise continue and build the room

        # dig the room out of the rock map
        dungeon.tiles[new_room.inner] = tile_types.plains

        if len(rooms) == 0:
            # place player in the starting room
            # Entity.spawn(entity_factories.player, gamemap=dungeon, x=20, y=20)
            Entity.spawn(entity_factories.infantry(team.blue_team), gamemap=dungeon, x=20, y=20)
            Entity.spawn(entity_factories.infantry(team.red_team), gamemap=dungeon, x=21, y=21)
            dungeon.tiles[21, 20] = tile_types.woods
        else:
            # dig out a tunnel connecting this to the previous room
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.plains

        rooms.append(new_room)

    return dungeon
