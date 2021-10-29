#!/usr/bin/env python3
import tcod

import color
from components import team
from engine import Engine
from factories import unit_factories
from procgen import generate_test_map


def main() -> None:
    screen_width = 60
    screen_height = 40
    info_panel_width = 20

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    cursor = unit_factories.player
    players = [team.red_team, team.blue_team]
    engine = Engine(cursor, players)

    # gamemap = generate_empty(map_width=map_width, map_height=map_height, player=player)

    engine.gamemap = generate_test_map(
        engine=engine
    )
    cursor.place(engine.gamemap.width // 2, engine.gamemap.height // 2, engine.gamemap)
    engine.update_fov()

    engine.message_log.add_message(
        "Welcome, commander", fg=color.white
    )

    with tcod.context.new_terminal(
            screen_width,
            screen_height,
            tileset=tileset,
            title="Advanced War",
            vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        engine.root_console = root_console
        engine.context = context
        engine.render(console=root_console, context=context)
        while True:
            if engine.event_handler.handle_events():
                engine.render(console=root_console, context=context)

            context.present(root_console)


if __name__ == "__main__":
    main()
