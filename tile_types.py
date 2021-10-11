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
        ("move", np.bool),  # True if this tile can be walked over.
        ("vision", np.bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
    ]
)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    move: int,
    vision: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((move, vision, dark), dtype=tile_dt)


floor = new_tile(
    move=1, vision=1, dark=(ord(","), (255, 255, 255), (50, 50, 150)),
)
wall = new_tile(
    move=0, vision=0, dark=(ord("#"), (255, 255, 255), (0, 0, 100)),
)
