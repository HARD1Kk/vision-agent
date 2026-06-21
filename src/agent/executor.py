import math
import time

import pyautogui

from agent.core.config import settings
from agent.core.logger import logger
from agent.models import Action, ActionType, ScrollDirection
from agent.utils.keyboard_utils import parse_and_validate_hotkey


class Executor:
    def execute_action(self, action: Action) -> str:
        """Execute one Action on the real screen and return a short log string"""

        if action.action == ActionType.CLICK:
            if action.x is None or action.y is None:
                logger.error("Failed CLICK: x and y coordinates are missing.")
                raise ValueError("Click action requires x and y coordinates")

            width, height = pyautogui.size()

            # 1. Auto-detect coordinate scale (0.0-1.0 vs 0-1000)
            norm_x = action.x if action.x <= 1.0 else action.x / 1000.0
            norm_y = action.y if action.y <= 1.0 else action.y / 1000.0

            # 2. Calculate raw pixel coordinates for the destination
            raw_x = int(norm_x * width)
            raw_y = int(norm_y * height)

            # 3. Apply strict screen boundaries (keeps cursor on screen without a dead zone)
            target_x = max(0, min(raw_x, width - 1))
            target_y = max(0, min(raw_y, height - 1))

            # 4. Get the starting position before moving
            start_x, start_y = pyautogui.position()

            # 5. Calculate how far it's about to move
            dx = target_x - start_x
            dy = target_y - start_y
            distance = math.hypot(dx, dy)  # Calculates straight-line pixel distance

            # 6. Execute the click
            pyautogui.click(target_x, target_y)

            # 7. Generate the detailed log string
            log_string = (
                f"Action: CLICK | "
                f"Moved: {distance:.1f}px (Δx:{dx}, Δy:{dy}) | "
                f"Destination: ({target_x}, {target_y})"
            )

            # Print to console so you can see it live (optional)
            logger.info(log_string)

            return log_string

        if action.action == ActionType.SCROLL:
            if action.direction is None:
                logger.error("Failed SCROLL: Direction is missing.")
                raise ValueError("Scroll action requires direction")
            clicks = -500 if action.direction == ScrollDirection.DOWN else 500
            pyautogui.scroll(clicks)

            log_string = f"Action: SCROLL | Direction: {action.direction.value} ({clicks} clicks)"
            logger.info(log_string)

            return f"scrolled {action.direction.value}"

        if action.action == ActionType.WAIT:
            time.sleep(settings.WAIT_SECONDS)

            log_string = f"Action: WAIT | Duration: {settings.WAIT_SECONDS}s"
            logger.info(log_string)
            return f"waited {settings.WAIT_SECONDS}s"

        if action.action == ActionType.PRESS:
            if not action.text:
                logger.error("Failed PRESS: Key name missing in 'text' field.")
                raise ValueError("Press action requires a key name in the 'text' field")

            # PyAutoGUI expects lowercase key names (e.g., 'enter' not 'Enter')
            key_to_press = action.text.strip().lower()
            pyautogui.press(key_to_press)
            logger.info(f"Action: PRESS | Key: '{key_to_press}'")
            return f"pressed '{key_to_press}'"

        if action.action == ActionType.TYPE:
            if not action.text:
                logger.error("Failed TYPE: No text provided.")
                raise ValueError("Type action requires text to type")

            # The 'interval' adds a small delay between keystrokes so the OS doesn't drop them
            pyautogui.write(action.text, interval=0.05)

            log_string = f"Action: TYPE | Text: '{action.text}'"
            logger.info(log_string)
            return f"typed '{action.text}'"
        if action.action == ActionType.HOTKEY:
            try:
                # Send the raw text to the utility file
                parsed_keys = parse_and_validate_hotkey(action.text)

                # If it survives parsing, execute it
                if parsed_keys:
                    pyautogui.hotkey(*parsed_keys)
                    logger.info(f"Action: HOTKEY | Keys: {parsed_keys}")

            except ValueError as e:
                # This catches empty strings AND invalid keys gracefully
                logger.error(f"Failed to execute HOTKEY: {e}")

        return str(ActionType.DONE.value)
