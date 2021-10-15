from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Optional

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity, Cursor


class Action:
    def __init__(self, entity: Entity) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """ Return the engine I belong to """
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()


class ActionWithDirection(Action):
    def __init__(self, entity: Entity, dx: int, dy: int):
        super().__init__(entity)
        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """ Destination of the action"""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """ Return the entity at the action's destination (if any)"""
        return self.engine.gamemap.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """ Returns actor at the destination"""
        return self.engine.gamemap.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.blocking_entity

        if not target:
            return

        if self.entity.fighter.is_in_range(target):
            print(
                f"The {self.entity.name} lays down suppressing fire at the {target.name}!"
            )
        else:
            print(f"Out of range")


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.gamemap.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not self.engine.gamemap.tiles["move"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.
        if self.engine.gamemap.get_blocking_entity_at_location(dest_x, dest_y):
            return  # blocked by another unit

        self.entity.move(self.dx, self.dy)
        self.engine.render_mode = "attack"
        self.engine.update_fov()


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.blocking_entity:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()


class MoveCursorAction(ActionWithDirection):
    # only checks inbounds
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.gamemap.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        self.entity.move(self.dx, self.dy)


class SelectAction(Action):
    def perform(self) -> None:
        cursor = self.engine.cursor
        for entity in self.engine.gamemap.entities - {cursor}:
            if (entity.x, entity.y) == (cursor.x, cursor.y):
                if cursor.selection == entity and self.engine.render_mode == "move":
                    # toggle render mode
                    self.engine.render_mode = "attack"
                else:
                    cursor.selection = entity
                    self.engine.render_mode = "move"
                return
        cursor.selection = None
        self.engine.render_mode = "none"
        return


class WaitAction(Action):
    def perform(self) -> None:
        pass


class UnitEndTurnAction(Action):
    def perform(self) -> None:
        self.entity.fighter.move_used = False
        self.entity.fighter.attack_used = False


class EndTurnAction(Action):
    def __init__(self, entity: Entity):
        super().__init__(entity)

    def perform(self) -> None:
        self.engine.handle_enemy_turns()
        self.engine.render_mode = "none"
        self.engine.cursor.selection = None


class EnemyAction(Action):
    def __init__(self, entity: Entity):
        super().__init__(entity)

    def perform(self) -> None:
        self.engine.handle_enemy_turns()
