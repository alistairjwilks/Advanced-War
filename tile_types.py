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

move_dt = np.dtype(
    [
        ("inf", np.int),
        ("mec", np.int),
        ("tire", np.int),
        ("tread", np.int),
        ("air", np.int),
        ("sea", np.int),
        ("lander", np.int),
        ("pipe", np.int),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("move", move_dt),  # movement costs for this tile.
        ("vision", np.int),  # True if this tile doesn't block FOV.
        ("defence", np.int),  # defence stars for the terrain
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt)  # when in view
    ]
)


def new_tile(
        *,  # Enforce the use of keywords, so that parameter order doesn't matter.
        move: Tuple[int, int, int, int, int],
        vision: int,
        defence: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((move, vision, defence, dark, light), dtype=tile_dt)


# movement costs
    # inf, mec, tire, tread, air, sea, lander, pipe
plains = new_tile(
    move=(1, 1, 2, 1, 1, 0, 0, 0),
    vision=1,
    defence=1,
    dark=(ord(","), (50, 50, 0), (100, 100, 0)),
    light=(ord(","), (229, 255, 54), (200, 200, 0)),
)

woods = new_tile(
    move=(1, 1, 3, 2, 1, 0, 0, 0),
    vision=1,
    defence=2,
    dark=(ord("\""), (0, 153, 0), (0, 51, 0)),
    light=(ord("\""), (0, 220, 0), (0, 153, 0)),
)

mountain = new_tile(
    move=(2, 1, 0, 0, 1, 0, 0, 0),
    vision=1,
    defence=3,
    dark=(ord("^"), (150, 150, 150), (51, 51, 51)),
    light=(ord("^"), (255, 255, 255), (150, 150, 150)),
)
