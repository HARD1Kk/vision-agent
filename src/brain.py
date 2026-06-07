from typing import List, Literal, Optional

from google import genai
from google.genai import types
from PIL import Image
from pydantic import BaseModel

from config import settings


class Action(BaseModel):
    """One step the agents wants to take. Coordinates normalised 0 - 1000"""

    reasoning: str
    action: Literal["click", "type", "scroll", "wait", "done"]

    x: Optional[int] = None
    y: Optional[int] = None
    text: Optional[str] = None
    direction: Optional[Literal["up", "down"]] = None


SYSTEM_INSTRUCTION = (
    "You control a Windows computer to accomplish the user's task. You are given "
    "the task and a screenshot. Decide the SINGLE next actionthat makes progress. \\n"
    "Coordinates x and y are normalized 0-1000 (0,0 = top-left, 1000,1000 = bottom-right).\\n"
    "Actions: click (set x,y to the element center), type (text into the focused "
    "field), scroll (direction up/down), wait (let an app open, then look again), "
    "done (task complete) . \\n"
    "To open an app: click the taskbar Search icon, type theapp name, click the top "
    "result. Prefer typing the name over hunting for tiles. If Search is already open, "
    "do not click the icon again - just type. \\n"
    "You are given the actions you have ALREADY taken. Do NOTrepeat an action that "
    "worked. If your last action had no visible effect, try adifferent approach. "
    "Return the 'done' action when the task is visibly accomplished."
)


def decide_action(
    client: genai.Client, task: str, screenshot: Image.Image, history: List[str]) -> Action:
    """Send task + history + screenshot to gemini and return one strcutred action"""
    history_text = "\\n".join(f"- {h}" for h in history) or "none yet"

    response = client.models.generate_content(
        model=settings.MODEL,
        contents=[
            f"Task: {task}Actions already taken (most recent last):\\n{history_text}",
            screenshot,
        ],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=Action,
        ),
    )
    return response.parsed
