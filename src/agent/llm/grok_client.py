import base64
from io import BytesIO

from groq import Groq
from PIL import Image

from agent.models.action import Action
from agent.prompts.system_prompt import SYSTEM_PROMPT
from agent.screen import encode_image


class GroqBrain:
    def __init__(self, client: Groq, model: str):
        self.client = client
        self.model = model

    def _encode_image(self, img: Image.Image) -> str:
        """Helper to convert PIL Image to Base64 for Groq/OpenAI APIs"""
        buffered = BytesIO()
        # Convert to RGB to avoid issues with alpha channels (transparency)
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def decide_action(
        self, task: str, screenshot: Image.Image, history: list[str]
    ) -> Action:
        """Send task + history + screenshot to Groq and return one structured action"""

        history_text = "\n".join(f"- {h}" for h in history) or "none yet"
        base64_image = encode_image(screenshot)

        # Groq Vision models expect a specific message structure for images
        # Re-structured payload to force Groq to include 'reasoning' and all required keys
        messages = [
            {
                "role": "system",
                "content": (
                    f"{SYSTEM_PROMPT}\n\n"
                    "CRITICAL: You must return a JSON object that matches this exact schema structure:\n"
                    "{{\n"
                    # 1. Add "press" to the action list
                    '  "action": "click" | "type" | "press" | "scroll" | "wait" | "done",\n'
                    '  "reasoning": "Detailed explanation of why you are taking this action",\n'
                    # 2. Update the text field instructions
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
                "content": [
                    {
                        "type": "text",
                        "text": f"Task: {task}\n\nActions already taken:\n{history_text}",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            },
        ]

        # Call the Groq API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,  # Low temperature is best for agentic decision making
            max_tokens=1024,
            # Force the model to return valid JSON
            response_format={"type": "json_object"},
        )

        result_string = response.choices[0].message.content

        if not result_string:
            raise ValueError("Groq returned an empty response")

        # Parse the JSON string directly into your Pydantic model
        # Assuming your Action class inherits from pydantic.BaseModel
        return Action.model_validate_json(result_string)
