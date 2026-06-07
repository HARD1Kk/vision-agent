from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ActionType(str, Enum):
    CLICK = "click"
    TYPE = "type"
    SCROLL = "scroll"
    WAIT = "wait"
    DONE = "done"


class ScrollDirection(str, Enum):
    UP = "up"
    DOWN = "down"


class Action(BaseModel):
    """One step the agents wants to take. Coordinates normalised 0 - 1000"""

    reasoning: str
    action: ActionType

    x: Optional[int] = None
    y: Optional[int] = None
    text: Optional[str] = None
    direction: ScrollDirection | None = None
