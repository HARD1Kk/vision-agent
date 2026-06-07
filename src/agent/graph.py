from typing import Optional , TypedDict


from google import genai
from langgraph.graph import END , START ,StateGraph

from PIL import Image

from agent.executor import Executor

from agent.models import Action 
from agent.llm.gemini_client import GeminiBrain

from agent.core.config import settings

from agent.screen import capture_image


class AgentState(TypedDict):
    task:str
    screenshot: Image.Image | None
    action: Optional[Action]
    step: int
    done:bool
    history:list[str]

