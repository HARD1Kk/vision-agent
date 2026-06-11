import base64
from io import BytesIO

import pyautogui
from PIL import Image

from agent.core.config import settings


def capture_image() -> Image.Image:
    """Capture the full primary screen and downscale it."""
    ss_width = settings.SCREENSHOT_WIDTH
    screenshot = pyautogui.screenshot()  # PIL image of whole screen

    # Resize once during capture to save memory immediately
    if screenshot.width > ss_width:
        ratio = ss_width / screenshot.width
        new_height = int(screenshot.height * ratio)
        # LANCZOS provides the sharpest text retention when downscaling
        screenshot = screenshot.resize((ss_width, new_height), Image.Resampling.LANCZOS)

    return screenshot


def encode_image(img: Image.Image) -> str:
    """Convert PIL Image to Base64 and compress for vision models."""
    # Drop the alpha channel if it exists
    if img.mode != "RGB":
        img = img.convert("RGB")

    buffered = BytesIO()
    # Save as JPEG with 85 quality for massive file size reduction
    img.save(buffered, format="JPEG", quality=85)

    return base64.b64encode(buffered.getvalue()).decode("utf-8")
