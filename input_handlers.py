from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import *

if TYPE_CHECKING:
    from engine import Engine

MOVE_KEYS = {
    # Arrow keys.
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
    tcod.event.K_HOME: (-1, -1),
    tcod.event.K_END: (-1, 1),
    tcod.event.K_PAGEUP: (1, -1),
    tcod.event.K_PAGEDOWN: (1, 1),
    # Numpad keys.
    tcod.event.K_KP_1: (-1, 1),
    tcod.event.K_KP_2: (0, 1),
    tcod.event.K_KP_3: (1, 1),
    tcod.event.K_KP_4: (-1, 0),
    tcod.event.K_KP_6: (1, 0),
    tcod.event.K_KP_7: (-1, -1),
    tcod.event.K_KP_8: (0, -1),
    tcod.event.K_KP_9: (1, -1),
    # Vi keys.
    tcod.event.K_h: (-1, 0),
    tcod.event.K_j: (0, 1),
    tcod.event.K_k: (0, -1),
    tcod.event.K_l: (1, 0),
    tcod.event.K_y: (-1, -1),
    tcod.event.K_u: (1, -1),
    tcod.event.K_b: (-1, 1),
    tcod.event.K_n: (1, 1),
}

WAIT_KEYS = {
    tcod.event.K_PERIOD,
    tcod.event.K_KP_5,
    tcod.event.K_CLEAR,
}

SELECT_KEYS = {
    tcod.event.K_x
}

SELECT_NEXT_KEYS = {
    tcod.event.K_TAB
}

ACTION_KEYS = {
    tcod.event.K_SPACE
}

END_TURN_KEYS = {
    tcod.event.K_RETURN,
    tcod.event.K_KP_ENTER
}


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

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = MoveCursorAction(entity=cursor, dx=dx, dy=dy)

        elif key in SELECT_KEYS:
            # only select or unselect
            action = SelectAction(entity=cursor)

        elif key in ACTION_KEYS:
            if cursor.selection:
                # if something is selected, try an action with it
                action = BumpAction(
                    entity=cursor.selection,
                    dx=cursor.x - cursor.selection.x,
                    dy=cursor.y - cursor.selection.y
                )
            else:
                # otherwise try selecting at the cursor
                action = SelectAction(entity=cursor)

        elif key in SELECT_NEXT_KEYS:
            action = SelectNextAction(entity=cursor)

        elif key in END_TURN_KEYS:
            # add confirmation
            action = EndTurnAction(cursor)
            print("Turn ended")


        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction(cursor)

        # No valid key was pressed
        return action
