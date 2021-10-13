#!/usr/bin/env python3
import tcod

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

    engine = Engine()

    # game_map = generate_empty(map_width=map_width, map_height=map_height, player=player)

    engine.game_map = generate_dungeon(
        map_width=map_width,
        map_height=map_height,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        max_rooms=max_rooms,
        engine=engine
    )

    player = Cursor(x=int(map_width / 2), y=int(map_height / 2), gamemap=engine.game_map, selection=None)

    engine.update_fov()

    with tcod.context.new_terminal(
            screen_width,
            screen_height,
            tileset=tileset,
            title="Advanced War",
            vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)
            engine.event_handler.handle_events()

            context.present(root_console)


if __name__ == "__main__":
    main()
