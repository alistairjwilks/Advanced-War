#!/usr/bin/env python3
import tcod

import entity
import tile_types
from engine import Engine
from entity import Cursor
import entity_factories
from procgen import generate_dungeon


def main() -> None:
    screen_width = 45
    screen_height = 35

    map_width = 45
    map_height = 35

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    player = entity_factories.player

    engine = Engine(player)

    # gamemap = generate_empty(map_width=map_width, map_height=map_height, player=player)

    engine.gamemap = generate_dungeon(
        map_width=map_width,
        map_height=map_height,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        max_rooms=max_rooms,
        engine=engine
    )
    player.place(21,21,engine.gamemap)
    engine.update_fov()

    with tcod.context.new_terminal(
            screen_width,
            screen_height,
            tileset=tileset,
            title="Advanced War",
            vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        engine.render(console=root_console, context=context)
        while True:
            if engine.event_handler.handle_events():
                engine.render(console=root_console, context=context)

            context.present(root_console)


if __name__ == "__main__":
    main()
