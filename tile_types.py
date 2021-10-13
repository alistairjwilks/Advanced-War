from typing import Tuple

import numpy as np  # type: ignore

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors, foreground
        ("bg", "3B"),  # background
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("move", np.int),  # movement cost for this tile.
        ("vision", np.int),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt)  # when in view
    ]
)


def new_tile(
        *,  # Enforce the use of keywords, so that parameter order doesn't matter.
        move: int,
        vision: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((move, vision, dark, light), dtype=tile_dt)


# SHROUD - unseen/unexplored tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    move=1,
    vision=1,
    dark=(ord(","), (255, 255, 255), (50, 50, 150)),
    light=(ord(","), (255, 255, 255), (200, 180, 50)),
)
wall = new_tile(
    move=0,
    vision=0,
    dark=(ord("#"), (255, 255, 255), (0, 0, 100)),
    light=(ord("#"), (255, 255, 255), (130, 110, 50)),
)
