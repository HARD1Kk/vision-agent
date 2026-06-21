import base64
from io import BytesIO

from groq import Groq
from groq.types.chat import ChatCompletionMessageParam
from loguru import logger
from PIL import Image

from agent.models.action import Action
from agent.prompts.system_prompt import SYSTEM_PROMPT


class GroqBrain:
    def __init__(self, client: Groq, vision_model: str, logic_model: str):
        self.client = client

        self.vision_model = vision_model

        self.logic_model = logic_model

    def _encode_image(self, img: Image.Image) -> str:
        """Helper to convert PIL Image to Base64 for Groq/OpenAI APIs"""
        buffered = BytesIO()
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def _analyze_screen(self, base64_image: str) -> str:
        """Step 1: The 'Eyes'. Extract raw data from the image into structured text."""
        logger.info(f"Running Vision Pass using {self.vision_model}...")

        messages: list[ChatCompletionMessageParam] = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "You are an accessibility screen reader. Analyze this UI screenshot. "
                            "List all visible text, interactive buttons, input fields, and icons. "
                            "If possible, estimate their approximate x, y coordinates or relative "
                            "positions (e.g., 'top right', 'center'). Be extremely detailed but objective."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ]

        response = self.client.chat.completions.create(
            model=self.vision_model,
            messages=messages,
            temperature=0.1,
            max_tokens=1024,
        )

        screen_description = response.choices[0].message.content
        if not screen_description:
            raise ValueError("The Vision model returned an empty response.")
        logger.debug(f"Screen Description:\n{screen_description}")
        return screen_description

    def decide_action(
        self, task: str, screenshot: Image.Image, history: list[str]
    ) -> Action:
        """Step 2: The 'Brain'. Reason over the screen text and output strict JSON."""

        # 1. Get Base64 Image
        base64_image = self._encode_image(screenshot)

        # 2. Extract Text Representation of the Screen
        screen_layout_text = self._analyze_screen(base64_image)

        logger.info(f"Running Logic Pass using {self.logic_model}...")

        MAX_HISTORY = 3
        recent_history = (
            history[-MAX_HISTORY:] if len(history) > MAX_HISTORY else history
        )

        # 3. Formulate Logic Prompt

        history_text = "\n".join(f"- {h}" for h in recent_history) or "none yet"
        if len(history) > MAX_HISTORY:
            history_text = (
                f"... ({len(history) - MAX_HISTORY} older actions hidden) ...\n"
                + history_text
            )
        logger.info(f"Running Logic Pass using {self.logic_model}...")

        messages: list[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": (
                    f"{SYSTEM_PROMPT}\n\n"
                    "CRITICAL: You must return a JSON object that matches this exact schema structure:\n"
                    "{{\n"
                    '  "action": "click" | "type" | "press" | "scroll" | "wait" | "done",\n'
                    '  "reasoning": "Detailed explanation of why you are taking this action",\n'
                    "  \"text\": \"text to type, OR key to press (e.g., 'enter', 'tab', 'esc'), otherwise null\",\n"
                    '  "x": integer_coordinate_or_null,\n'
                    '  "y": integer_coordinate_or_null,\n'
                    '  "direction": "up" | "down" | null\n'
                    "}}\n\n"
                    "Ensure every single key is present in your response. Use null for unused fields."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Task: {task}\n\n"
                    f"Actions already taken:\n{history_text}\n\n"
                    f"CURRENT SCREEN STATE (Extracted by Vision AI):\n"
                    f"---\n{screen_layout_text}\n---\n\n"
                    "Based on the screen state and history, what is the exact next action to take?"
                ),
            },
        ]

        # 4. Call the Logic Model (Text Only, Strict JSON)
        response = self.client.chat.completions.create(
            model=self.logic_model,
            messages=messages,
            temperature=0.1,
            max_tokens=1024,
            response_format={"type": "json_object"},
        )

        result_string = response.choices[0].message.content
        logger.info(f"Action Output: {result_string}")

        if not result_string:
            raise ValueError("Groq returned an empty response")

        return Action.model_validate_json(result_string)
