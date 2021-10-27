from __future__ import annotations

import copy
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING

import tile_types
from components.team import Team

if TYPE_CHECKING:
    from components.ai import BaseAI, StructureAI
    from components.fighter import Fighter
    from game_map import GameMap

T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    gamemap: GameMap

    def __init__(
            self,
            gamemap: GameMap = None,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            blocks_movement: bool = False
    ):
        self.fighter = None
        self.team = None
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.gamemap = gamemap
        if self.gamemap:
            self.gamemap.entities.add(self)
        self.selection = None
        self.vision = 0

    @property
    def is_visible(self):
        return self.gamemap.visible[self.x, self.y]

    @property
    def tile(self) -> tile_types.tile_dt:
        return self.gamemap.tiles[self.x, self.y]

    @property
    def bg_color(self) -> Tuple[int, int, int]:
        if self.gamemap.visible[self.x, self.y]:
            return tuple(self.tile["light"]["bg"])
        else:
            return tuple(self.tile["dark"]["bg"])

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
            if self.gamemap:  # if we are already on a map
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

    def is_alive(self):
        return False

    def move_by_step(self, dx, dy):
        self.move(dx, dy)


class Actor(Entity):
    def __init__(
            self,
            *,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            team: Team,
            cost: int = 0,
            name: str = "<Unnamed>",
            ai_cls: Type[BaseAI],
            fighter: Fighter,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=team.fg_color,
            name=name,
            blocks_movement=True,

        )

        self.ai: Optional[BaseAI] = ai_cls(self)
        self.cost = cost
        self.fighter = fighter
        self.fighter.entity = self
        self.vision = fighter.vision
        self.team = team

    @property
    def move_type(self) -> str:
        return self.fighter.move_type

    @property
    def is_alive(self) -> bool:
        """ return true as long as the actor can still act"""
        return bool(self.ai)

    @property
    def active(self) -> bool:
        return not (self.fighter.move_used and self.fighter.attack_used)

    @property
    def bg_color(self) -> Tuple[int, int, int]:
        if self.active or self.gamemap.engine.active_player.code != self.team.code:
            super().bg_color
        else:
            return 160, 160, 160

    def move(self, dx: int, dy: int) -> None:
        """
        Move the entity by a given amount
        Actors use the move method of their fighter, which will check terrain and use fuel
        Entity just moves directly
        """
        self.fighter.move(dx, dy)

    @property
    def is_visible(self):
        if self.team.code == self.fighter.engine.active_player.code:
            return True
        else:
            return super().is_visible


class Structure(Entity):
    def __init__(
            self,
            *,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            team: Team = None,
            name: str = "<Unnamed>",
            ai_cls: Type[StructureAI] ,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            name=name,
            blocks_movement=False,
        )

        self.ai: Optional[BaseAI] = ai_cls(self)
        self.fighter = None
        self.team = team

    @property
    def bg_color(self) -> Tuple[int, int, int]:
        if self.team:
            return self.team.bg_color
        return self.tile[self.is_visible]["bg"]


class Cursor(Entity):
    def __init__(self):
        super().__init__()
        self.selection = None
