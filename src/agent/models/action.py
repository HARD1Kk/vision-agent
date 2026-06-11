from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ActionType(str, Enum):
    CLICK = "click"
    TYPE = "type"
    SCROLL = "scroll"
    WAIT = "wait"
    DONE = "done"
    PRESS = "press"


class ScrollDirection(str, Enum):
    UP = "up"
    DOWN = "down"


class Action(BaseModel):
    """One step the agents wants to take. Coordinates normalised 0 - 1000"""

    reasoning: str
    action: ActionType
    reasoning: str = "No reasoning provided."
    x: float | None = None
    y: float | None = None
    text: Optional[str] = None
    direction: ScrollDirection | None = None
