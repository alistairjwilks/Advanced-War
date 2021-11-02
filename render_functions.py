from __future__ import annotations

from typing import TYPE_CHECKING

import color
from entity import Cursor, Actor

if TYPE_CHECKING:
    from tcod import Console, console


def render_quick_info(
        console: Console,
        cursor: Cursor,
        position_x,
        position_y
) -> None:
    console.print(
        x=position_x, y=position_y-1, string=f"({cursor.x + 1},{cursor.y + 1})"
    )

    render_stats(console, cursor.selection, position_x, position_y)


def render_unit_panel(
        console: Console,
        cursor: Cursor,
):
    """ Side info panel """
    console.draw_rect(x=40, y=0, width=20, height=40, ch=1, bg=color.light_grey)
    actor = cursor.parent.get_actor_at_location(cursor.x, cursor.y)
    if actor and actor.is_visible:
        col = actor.team.bg_color
    else:
        col = color.white
    console.draw_rect(x=41, y=1, width=18, height=9, ch=1, bg=col)


    if actor and actor.is_visible:
        pass


def render_stats(
        console: Console,
        actor: Actor,
        position_x: int = 0,
        position_y: int = 0
) -> None:
    if actor:
        stats = f"{actor.name} |HP:{actor.fighter.displayed_hp}|FUEL:{actor.fighter.fuel}|"
        if actor.fighter.ammo_max > 0:
            stats += f"AMMO:{actor.fighter.ammo}"
        console.print(
            x=position_x, y=position_y, string=stats, fg=actor.team.fg_color
        )
