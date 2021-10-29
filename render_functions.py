from __future__ import annotations

from typing import TYPE_CHECKING

import color
from entity import Cursor

if TYPE_CHECKING:
    from tcod import Console


def render_coordinates(
        console: Console,
        cursor: Cursor,
        position_x,
        position_y
) -> None:
    console.print(
        x=position_x, y=position_y, string=f"({cursor.x+1},{cursor.y+1})"
    )


def render_panel():
    pass



def render_bar(
        console: Console,
        current_value: int,
        max_value: int,
        total_width: int,
        position_x: int = 0,
        position_y: int = 20
) -> None:
    bar_width = int(float(current_value) / max_value * total_width)
    console.draw_rect(x=position_x, y=position_y, width=10, height=1, ch=1, bg=color.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=position_x, y=position_y, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )

    console.print(
        x=position_x + 1, y=position_y, string=f"HP: {current_value}", fg=color.bar_text
    )
