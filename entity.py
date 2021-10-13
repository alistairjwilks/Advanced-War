import copy
from typing import Optional, Tuple, TypeVar, TYPE_CHECKING

from game_map import GameMap

T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    gamemap: GameMap

    def __init__(
            self,
            gamemap: Optional[GameMap] = None,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            blocks_movement: bool = False
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        if gamemap:
            self.gamemap = gamemap
            gamemap.entities.add(self)

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location"""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.gamemap = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        """ Place the entity at a new location, possibly on a new gamemap """
        self.x = x
        self.y = y
        if gamemap:  # if a new map is given
            if hasattr(self, "gamemap"):  # if we are already on a map
                self.gamemap.entities.remove(self)  # remove ourself from it
            # then set current map to the given map
            self.gamemap = gamemap
            gamemap.entities.add(self)

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def move_to(self, dest_x: int, dest_y: int):
        self.x = dest_x
        self.y = dest_y


class Cursor(Entity):
    def __init__(self, x: int, y: int, gamemap: GameMap, selection: Optional[Entity] = None):
        super().__init__(x=x, y=y, char=" ", color=(1, 1, 1))
        self.selection = selection
        self.gamemap = gamemap
        gamemap.cursor = self

    pass
