from __future__ import annotations

import math
from time import sleep
from typing import TYPE_CHECKING, Tuple, Optional, Iterable

import damage_table

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity, Cursor, Actor


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
    def __init__(self, entity: Actor, dx: int, dy: int):
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


class AttackAction(ActionWithDirection):

    def calculate_damage(self, attacker: Actor, defender: Actor, primary: str = "") -> int:
        # overall damage formula
        # (Base damage * attacker mod + luck)*(Attacker display HP / 10) * (200 - (defender + defender_terrain * defender hp))/100
        try:
            base_damage = damage_table.table[attacker.fighter.code + primary][defender.fighter.code]
        except KeyError:
            return 0
        damage = (base_damage * attacker.fighter.damage_mod + attacker.team.luck_roll())
        attacker_hp_mod = (attacker.fighter.displayed_hp / 10)
        defence_mod = (200 - (defender.fighter.defence + (
                    defender.fighter.terrain_defence * defender.fighter.displayed_hp))) / 100
        print(f"{damage} * {attacker_hp_mod} * {defence_mod}")
        return math.ceil(damage * attacker_hp_mod * defence_mod)

    def attack(self, attacker: Actor, target: Actor) -> int:
        if not target or target.team.code == attacker.team.code:
            # can't attack your own team or nothing
            return 0
        primary = ""
        damage = 0

        if attacker.fighter.is_in_range(target):
            # try both weapons on target
            if attacker.fighter.ammo > 0:
                # try to use primary weapon
                damage = self.calculate_damage(attacker, target, "_p")
            if damage > 0:
                attacker.fighter.ammo -= 1
            else:
                damage = self.calculate_damage(attacker, target)
            if damage > 0:
                target.fighter.take_damage(damage)
        return damage

    def perform(self) -> None:
        attacker: Actor = self.entity
        target: Actor = self.blocking_entity

        if not target or attacker.fighter.attack_used or target.team.code == attacker.team.code:
            # can't attack your own team
            return

        damage = self.attack(attacker, target)
        if damage > 0:
            print(
                f"The {attacker.name}({attacker.fighter.hp}) does {damage} damage to {target.name}({target.fighter.hp})"
            )
            attacker.fighter.attack_used = True
            attacker.fighter.move_used = True
            self.engine.gamemap.flash(target.x, target.y, self.engine.root_console, '*')
        if target.is_alive:
            retaliation = self.attack(target, attacker)
            if retaliation > 0:
                print(
                    f"The {target.name}({target.fighter.hp}) retaliates for {retaliation} on {attacker.name}({attacker.fighter.hp})"
                )
                self.engine.gamemap.flash(attacker.x, attacker.y, self.engine.root_console, '*')



class MoveStepAction(ActionWithDirection):

    def perform(self) -> [Action]:
        steps: [StepAction] = []
        self.engine.render_mode = "none"
        self.engine.gamemap.render(self.engine.root_console)
        self.engine.gamemap.quick_render(self.engine.root_console)
        if (self.entity.x + self.dx, self.entity.y + self.dy) in self.entity.fighter.move_range:
            cost, path = self.entity.fighter.path_cost(self.dx, self.dy)
            for step in path:
                self.engine.gamemap.draw(self.entity.x, self.entity.y, self.engine.root_console)
                steps.append(StepAction(self.entity, *step))
                if StepAction(self.entity, *step).perform():
                    continue
                else:
                    print("Ambush!")
                    self.entity.fighter.move_used = True
                    self.entity.fighter.attack_used = True
                    print(self.entity.name + " fuel:" + str(self.entity.fighter.fuel))
                    break

        self.entity.fighter.move_used = True
        # print(cost, path)
        self.entity.fighter.calculate_move_range()
        return steps


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.gamemap.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not self.engine.gamemap.tiles["move"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.

        self.entity.move(self.dx, self.dy)
        self.engine.update_fov()


class StepAction(ActionWithDirection):
    def perform(self) -> bool:
        start_x, start_y = self.entity.x, self.entity.y
        self.engine.gamemap.draw(self.entity.x, self.entity.y, self.engine.root_console)
        self.entity.gamemap.quick_render(self.engine.root_console)
        sleep(0.1)
        actor = self.entity.gamemap.get_actor_at_location(self.dx, self.dy)
        if actor and actor.team.code != self.entity.team.code:  # ambush!
            self.entity.gamemap.flash(actor.x, actor.y, self.engine.root_console)
            return False
        else:
            self.entity.x, self.entity.y = self.dx, self.dy
            self.entity.gamemap.draw(self.entity.x, self.entity.y, self.engine.root_console)
            self.entity.gamemap.draw(start_x, start_y, self.engine.root_console)
            self.entity.gamemap.quick_render(self.engine.root_console)
            return True


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.blocking_entity and self.blocking_entity.is_visible:
            return AttackAction(self.entity, self.dx, self.dy).perform()
        else:
            return MoveStepAction(self.entity, self.dx, self.dy).perform()


class MoveCursorAction(ActionWithDirection):
    # only checks inbounds
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.gamemap.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        self.entity.move(self.dx, self.dy)
        # print(self.engine.gamemap.get_neighbours(self.entity.x, self.entity.y))


class SelectAction(Action):
    def perform(self) -> None:
        cursor = self.engine.cursor
        for entity in [unit for unit in self.engine.gamemap.actors if
                       unit.active and unit.team.code == self.engine.active_player.code]:
            # only able to select from your own units
            if (entity.x, entity.y) == (cursor.x, cursor.y):

                if \
                        cursor.selection == entity and \
                                not cursor.selection.fighter.move_used and \
                                not self.engine.render_mode == "move":
                    # toggle render mode
                    self.engine.render_mode = "move"
                elif cursor.selection == entity and \
                        not cursor.selection.fighter.attack_used and \
                        not self.engine.render_mode == "attack" and \
                        not cursor.selection.fighter.is_direct_fire:
                    self.engine.render_mode = "attack"
                else:
                    cursor.selection = entity
                return
        cursor.selection = None
        return


class SelectNextAction(Action):
    # look through available unused entities and select the next one

    actorList = []

    def perform(self) -> None:
        cursor = self.engine.cursor
        if not SelectNextAction.actorList:
            # empty list evaluates to false
            SelectNextAction.actorList = [
                actor for actor in self.engine.gamemap.actors if
                actor.active and actor.team.code == self.engine.active_player.code
            ]
            if not SelectNextAction.actorList:
                return
        next_actor = SelectNextAction.actorList.pop()
        MoveCursorAction(cursor, next_actor.x - cursor.x, next_actor.y - cursor.y).perform()
        if not next_actor.fighter.move_used:
            self.engine.render_mode = "move"
        else:
            self.engine.render_mode = "attack"
        SelectAction(cursor).perform()


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
        self.engine.render_mode = "none"
        self.engine.cursor.selection = None
        self.engine.next_player()
        SelectNextAction(self.entity).perform()
        SelectNextAction(self.entity).perform()


class EnemyAction(Action):
    def __init__(self, entity: Entity):
        super().__init__(entity)

    def perform(self) -> None:
        self.engine.new_turn()
