from __future__ import annotations

from typing import TYPE_CHECKING

import entity_factories
import tile_types
from components import team

if TYPE_CHECKING:
    from engine import Engine

from game_map import GameMap


def generate_aw_map(
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

    entity_factories.tank(team.red_team).spawn(aw_map, x=4, y=4)
    entity_factories.tank(team.red_team).spawn(aw_map, x=4, y=5)
    entity_factories.tank(team.red_team).spawn(aw_map, x=4, y=6)
    entity_factories.rocket(team.red_team).spawn(aw_map, x=3, y=5)

    entity_factories.tank(team.blue_team).spawn(aw_map, x=13, y=4)
    entity_factories.tank(team.blue_team).spawn(aw_map, x=13, y=5)
    entity_factories.tank(team.blue_team).spawn(aw_map, x=13, y=6)
    return aw_map
