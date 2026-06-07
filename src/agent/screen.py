import pyautogui
from PIL import Image

from agent.core.config import settings


def capture_image() -> Image.Image:
    """Capture the full primary screen and downscale it for the vision model"""
    ss_width = settings.SCREENSHOT_WIDTH
    screenshot = pyautogui.screenshot()  # PIL image of whole scren

    if screenshot.width > ss_width:
        ratio = ss_width / screenshot.width
        new_height = int(screenshot.height * ratio)
        screenshot = screenshot.resize((ss_width, new_height))
    return screenshot


print(pyautogui.size())
