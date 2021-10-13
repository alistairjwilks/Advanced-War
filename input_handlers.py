from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction, MoveCursorAction


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_UP:
            action = MoveCursorAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = MoveCursorAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = MoveCursorAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = MoveCursorAction(dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        # No valid key was pressed
        return action
