from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import *

if TYPE_CHECKING:
    from engine import Engine


class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self) -> bool:
        for event in tcod.event.wait():
            action = self.dispatch(event)
            did_action = False
            if action is None:
                continue

            action.perform()
            did_action = True
            #            self.engine.handle_enemy_turns()

            self.engine.update_fov()  # ?
            return did_action

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym
        cursor = self.engine.cursor

        if key == tcod.event.K_UP:
            action = MoveCursorAction(entity=cursor, dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = MoveCursorAction(entity=cursor, dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = MoveCursorAction(entity=cursor, dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = MoveCursorAction(entity=cursor, dx=1, dy=0)

        elif key == tcod.event.K_RETURN:
            action = SelectAction(entity=cursor)

        elif key == tcod.event.K_x:
            if cursor.selection:
                action = BumpAction(
                    entity=cursor.selection,
                    dx=cursor.x - cursor.selection.x,
                    dy=cursor.y - cursor.selection.y
                )

        elif key == tcod.event.K_v:
            action = EndTurnAction(cursor)
            print("Turn ended")


        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        # No valid key was pressed
        return action
