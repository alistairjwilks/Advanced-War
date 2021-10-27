from __future__ import annotations

import csv
from typing import TYPE_CHECKING

import numpy as np

from maps import map_key

from factories import unit_factories, structure_factories
import tile_types
from components import team

if TYPE_CHECKING:
    from engine import Engine

from game_map import GameMap


def generate_test_map(
        engine: Engine
) -> GameMap:
    """ generate a hardcoded test map"""
    aw_map = GameMap(
        engine=engine,
        width=20,
        height=10,
        entities=[],
        no_fog=False
    )

    for i in range(aw_map.width):
        aw_map.tiles[i, 0] = tile_types.mountain
        aw_map.tiles[i, 1:3] = tile_types.woods
        aw_map.tiles[i, aw_map.height - 1] = tile_types.mountain

    aw_map.tiles[5, 5] = tile_types.city

    structure_factories.team_city(team.red_team).spawn(aw_map, x=5, y=5)

    unit_factories.tank(team.red_team).spawn(aw_map, x=4, y=4)
    unit_factories.tank(team.red_team).spawn(aw_map, x=4, y=5)
    unit_factories.tank(team.red_team).spawn(aw_map, x=4, y=6)
    unit_factories.artillery(team.red_team).spawn(aw_map, x=3, y=5)

    unit_factories.tank(team.blue_team).spawn(aw_map, x=13, y=4)
    unit_factories.tank(team.blue_team).spawn(aw_map, x=13, y=5)
    unit_factories.tank(team.blue_team).spawn(aw_map, x=13, y=6)
    return aw_map


def read_map_awbw(engine: Engine, filename="maps/test.csv") -> GameMap:
    with open(filename, "r") as f:
        data = list(csv.reader(f, delimiter=","))

    data = np.array(data)
    height, width = len(data), len(data[0])
    print(height, width)

    aw_map = GameMap(
        engine=engine,
        width=width,
        height=height,
        entities=[],
        no_fog=False
    )

    for i in range(width):
        for j in range(height):
            aw_map.tiles[i][j] = map_key.key[data[j, i]]

    print(aw_map.tiles["dark"]["ch"])
    return aw_map
