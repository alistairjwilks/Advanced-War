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
        ("tread", np.int),
        ("tire", np.int),
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
        move: Tuple[int, int, int, int, int, int, int, int],
        vision: int,
        defence: int,
        dark: Tuple[Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[Tuple[int, int, int], Tuple[int, int, int]],
        sym: str
) -> np.ndarray:
    """Helper function for defining individual tile types """
    dark_tile = (ord(sym), *dark)
    light_tile = (ord(sym), *light)
    return np.array((move, vision, defence, dark_tile, light_tile), dtype=tile_dt)


# movement costs
# inf, mec, tire, tread, air, sea, lander, pipe
plains = new_tile(
    move=(1, 1, 1, 2, 1, 0, 0, 0),
    vision=1,
    defence=1,
    sym=',',
    dark=((50, 50, 0), (128, 152, 144)),
    light=((229, 255, 54), (204, 228, 40)),
)

woods = new_tile(
    move=(1, 1, 2, 3, 1, 0, 0, 0),
    vision=1,
    defence=2,
    sym='"',
    dark=((64, 136, 144), (139, 157, 144)),
    light=((69, 166, 156), (205, 228, 39)),
)

mountain = new_tile(
    move=(2, 1, 0, 0, 1, 0, 0, 0),
    vision=1,
    defence=4,
    sym="^",
    dark=((150, 150, 150), (51, 51, 51)),
    light=((255, 255, 255), (150, 150, 150)),
)


def river(sym: str = '+'):
    return new_tile(
        move=(2, 1, 0, 0, 1, 0, 0, 0),
        vision=1,
        defence=0,
        sym=sym,
        dark=((120, 121, 183), (78, 59, 173)),
        light=((184, 224, 248), (112, 88, 248)),
    )


def road(sym: str = '+'):
    return new_tile(
        move=(1, 1, 1, 1, 1, 0, 0, 0),
        vision=1,
        defence=0,
        sym=sym,
        dark=((144, 144, 152), (96, 96, 120)),
        light=((187, 195, 194), (152, 160, 184)),
    )


shoal = new_tile(
    move=(1, 1, 1, 1, 1, 0, 1, 0),
    vision=1,
    defence=0,
    sym=';',
    dark=((168, 152, 120), (80, 56, 168)),
    light=((111, 91, 248), (111, 91, 248)),
)

reef = new_tile(
    move=(0, 0, 0, 0, 1, 2, 2, 0),
    vision=1,
    defence=1,
    sym='%',
    dark=((104, 80, 88), (80, 56, 168)),
    light=((104, 80, 88), (111, 91, 248)),
)


def pipe(sym: str = '+'):
    return new_tile(
        move=(0, 0, 0, 0, 0, 0, 0, 1),
        vision=1,
        defence=0,
        sym=sym,
        dark=((120, 88, 112), (120, 88, 112)),
        light=((168, 128, 128), (168, 128, 128)),
    )


""" 
neutral buildings - there will be an entity overlaid when captured, but this contains the terrain info
"""
city = new_tile(
    move=(1, 1, 1, 1, 1, 0, 0, 0),
    vision=1,
    defence=3,
    sym='$',
    dark=((112, 88, 136), (112, 88, 136)),
    light=((240, 232, 208), (165, 154, 165)),
)

base = new_tile(
    move=(1, 1, 1, 1, 1, 0, 0, 1),
    vision=1,
    defence=3,
    sym="@",
    dark=((112, 88, 136), (112, 88, 136)),
    light=((240, 232, 208), (165, 154, 165)),
)

port = new_tile(
    move=(1, 1, 1, 1, 1, 1, 1, 0),
    vision=1,
    defence=3,
    sym='&',
    dark=((112, 88, 136), (112, 88, 136)),
    light=((240, 232, 208), (165, 154, 165)),
)

airport = new_tile(
    move=(1, 1, 1, 1, 1, 0, 0, 0),
    vision=1,
    defence=3,
    sym='#',
    dark=((112, 88, 136), (112, 88, 136)),
    light=((240, 232, 208), (165, 154, 165)),
)

com_tower = new_tile(
    move=(1, 1, 1, 1, 1, 0, 0, 0),
    vision=1,
    defence=3,
    sym='|',
    dark=((112, 88, 136), (112, 88, 136)),
    light=((240, 232, 208), (165, 154, 165)),
)

lab = new_tile(
    move=(1, 1, 1, 1, 1, 0, 0, 0),
    vision=1,
    defence=3,
    sym='?',
    dark=((112, 88, 136), (112, 88, 136)),
    light=((240, 232, 208), (165, 154, 165)),
)

missile = new_tile(  # spent missile
    move=(1, 1, 1, 1, 1, 0, 0, 0),
    vision=1,
    defence=3,
    sym='.',
    dark=((112, 88, 136), (112, 88, 136)),
    light=((240, 232, 208), (165, 154, 165)),
)

headquarters = new_tile(
    move=(1, 1, 1, 1, 1, 0, 0, 0),
    vision=1,
    defence=4,
    sym='!',
    dark=((112, 88, 136), (112, 88, 136)),
    light=((240, 232, 208), (165, 154, 165)),
)
