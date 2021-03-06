from __future__ import annotations

import copy
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING, List

import tile_types

from components.team import Team

if TYPE_CHECKING:
    from components.ai import BaseAI, StructureAI
    from components.fighter import Fighter
    from components.structure_components import Capturable, Income, Repair, Production
    from game_map import GameMap


T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    parent: GameMap

    def __init__(
            self,
            parent: Optional[GameMap] = None,
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
        if parent:
            self.parent = parent
            parent.entities.add(self)
        self.selection = None
        self.vision = 0

    @property
    def is_visible(self):
        return self.gamemap.visible[self.x, self.y]

    @property
    def tile(self) -> tile_types.tile_dt:
        return self.gamemap.tiles[self.x, self.y]

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    @property
    def bg_color(self) -> Tuple[int, int, int]:
        if self.parent.visible[self.x, self.y]:
            return tuple(self.tile["light"]["bg"])
        else:
            return tuple(self.tile["dark"]["bg"])

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location"""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        """ Place the entity at a new location, possibly on a new gamemap """
        self.x = x
        self.y = y
        if gamemap:  # if a new map is given
            if hasattr(self, "parent"):  # possibly uninitialised
                if self.parent is self.gamemap:
                    self.gamemap.entities.remove(self)  # remove ourself from it
            # then set current map to the given map
            self.parent = gamemap
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
        self.fighter.parent = self
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
        if self.active or self.parent.engine.active_player.code != self.team.code:
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


class Structure(Entity):  # basic structure, will use components for the functionality
    def __init__(
            self,
            *,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            team: Team = None,
            name: str = "<Unnamed>",
            ai_cls: Type[StructureAI],
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            name=name,
            blocks_movement=False,
        )

        self.ai: Optional[BaseAI] = ai_cls(self)
        self.team = team
        self.capturable = None
        self.income = None
        self.repair = None
        self.passive = None

    @property
    def bg_color(self) -> Tuple[int, int, int]:
        if self.team:
            return self.team.bg_color
        return self.tile[self.is_visible]["bg"]


class City(Structure):
    def __init__(
            self,
            *,
            x: int = 0,
            y: int = 0,
            team: Team = None,
            ai_cls: Type[StructureAI],
    ):
        super().__init__(x=x, y=y, char='$', name="City")
        # components
        self.capturable = Capturable(team)
        self.capturable.entity = self
        self.income = Income()
        self.income.entity = self
        self.repair = Repair(["inf", "mec", "tire", "tread"])
        self.repair.entity = self


class ProductionBuilding(Structure):
    def __init__(
            self,
            *,
            x: int = 0,
            y: int = 0,
            team: Team = None,
            name: str = "<Unnamed>",
            ai_cls: Type[StructureAI],
            repair: List[str] = ["inf", "mec", "tire", "tread"],
            production: List[str] = ["inf", "mec", "tire", "tread", "pipe"]
    ):
        super().__init__(x=x, y=y, char='$', name=name)
        # components
        self.capturable = Capturable()
        self.income = Income()
        self.repair = Repair(repair)
        self.production = Production(production)


class ComTower(Structure):
    pass


class MissileSilo(Structure):
    pass


class Cursor(Entity):
    def __init__(self):
        super().__init__()
        self.selection = None
