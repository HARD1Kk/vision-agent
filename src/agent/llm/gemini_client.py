from typing import cast

from google import genai
from google.genai import types
from PIL import Image

from agent.core.config import settings
from agent.core.logger import logger
from agent.models.action import Action
from agent.prompts.system_prompt import SYSTEM_PROMPT


class GeminiBrain:
    def __init__(self, client: genai.Client, model: str):
        self.client = client
        self.model = model

    def decide_action(
        self, task: str, screenshot: Image.Image, history: list[str]
    ) -> Action:
        """Send task + history + screenshot to gemini and return one strcutred action"""
        history_text = "\\n".join(f"- {h}" for h in history) or "none yet"

        response = self.client.models.generate_content(
            model=settings.MODEL,
            contents=[
                f"Task: {task}\n\nActions already taken (most recent last):\n{history_text}",
                screenshot,
            ],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=Action,
            ),
        )
        parsed = response.parsed
        logger.info(parsed)
        if parsed is None:
            raise ValueError("Gemini returned no parsed response")

        return cast(Action, parsed)


if __name__ == "__main__":
    from pathlib import Path

    from google import genai
    from PIL import Image

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    brain = GeminiBrain(client, model=settings.MODEL)

    task = "Open Settings"
    screenshot_path = Path("ss/image.png")
    screenshot = Image.open(screenshot_path)
    history = []

    try:
        screenshot = Image.open(screenshot_path)
    except Exception as exc:
        print(f"Failed to open screenshot: {exc}")
        raise SystemExit(1)

    try:
        action = brain.decide_action(
            task=task,
            screenshot=screenshot,
            history=history,
        )

        print("\n=== Action ===")
        print(action.model_dump_json(indent=2))

    except Exception as exc:
        print(f"Failed to decide action: {exc}")
        raise SystemExit(1)
