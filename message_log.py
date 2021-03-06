from typing import List, Reversible, Tuple, Iterable
import textwrap

import tcod

import color


class Message:
    def __init__(self, text: str, fg:Tuple[int,int,int]):
        self.plain_text=text
        self.fg = fg
        self.count=1

    @property
    def full_text(self) -> str:
        """ Full text of the message, including count"""
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"
        return self.plain_text


class MessageLog:
    def __init__(self) -> None:
        self.messages: List[Message] = []

    def add_message(
            self, text: str, fg: Tuple[int, int, int] = color.white, *, stack: bool=True,
    ) -> None:
        """
        stack allows a message to be joined and counted along with another of the same text
        """
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def render(
            self, console: tcod.Console, x: int, y:int, width:int, height:int
    ) -> None:
        """ draws out the log into a rectangular area of the console"""
        self.render_messages(console, x, y, width, height, self.messages)

    @staticmethod
    def wrap(string: str, width:int) -> Iterable[str]:
        """ Return a wrapped text message"""
        for line in string.splitlines():
            yield from textwrap.wrap(
                line, width, expand_tabs=True
            )

    @classmethod
    def render_messages(
            cls,
            console: tcod.Console,
            x: int,
            y: int,
            w: int,
            h: int,
            messages: Reversible[Message],
    )-> None:
        """ Render messages Last to First"""
        y_offset = h-1
        for message in reversed(messages):
            for line in reversed(list(cls.wrap(message.full_text, w))):
                console.print(x=x,y=y+y_offset, string = line, fg=message.fg)
                y_offset -= 1
                if y_offset < 0:
                    return # no more room