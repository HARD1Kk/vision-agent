import time

import pyautogui

from agent.core.config import settings
from agent.models import Action, ActionType, ScrollDirection


class Executor:
    def execute_action(self, action: Action) -> str:
        """Execute one Action on the real screen and return a short log string"""

        if action.action == ActionType.CLICK:
            if action.x is None or action.y is None:
                raise ValueError("Click action requires x and y coordinates")

            width, height = pyautogui.size()

            # 1. Auto-detect coordinate scale (0.0-1.0 vs 0-1000)
            # If the number is less than or equal to 1.0, it's a decimal percentage.
            # If it's greater, the model gave us the 0-1000 scale we asked for.
            norm_x = action.x if action.x <= 1.0 else action.x / 1000.0
            norm_y = action.y if action.y <= 1.0 else action.y / 1000.0

            # 2. Calculate raw pixel coordinates
            raw_x = int(norm_x * width)
            raw_y = int(norm_y * height)

            # 3. Apply Failsafe Bumpers (Keep it 5 pixels inside the screen)
            x = max(5, min(raw_x, width - 5))
            y = max(5, min(raw_y, height - 5))

            pyautogui.click(x, y)
            return f"clicked ({x}, {y})"

        if action.action == ActionType.TYPE:
            if action.text is None:
                raise ValueError("Type action requires text")

            pyautogui.write(action.text or " ", interval=0.02)
            return f"typed {action.text!r}"

        if action.action == ActionType.SCROLL:
            if action.direction is None:
                raise ValueError("Scroll action requires direction")
            clicks = -500 if action.direction == ScrollDirection.DOWN else 500
            pyautogui.scroll(clicks)

            return f"scrolled {action.direction.value}"

        if action.action == ActionType.WAIT:
            time.sleep(settings.WAIT_SECONDS)
            return f"waited {settings.WAIT_SECONDS}s"

        if action.action == ActionType.PRESS:
            if not action.text:
                raise ValueError("Press action requires a key name in the 'text' field")

            # PyAutoGUI expects lowercase key names (e.g., 'enter' not 'Enter')
            key_to_press = action.text.strip().lower()

            pyautogui.press(key_to_press)
            return f"pressed '{key_to_press}'"
        return str(ActionType.DONE.value)


if __name__ == "__main__":
    from agent.models.action import (
        Action,
        ActionType,
        ScrollDirection,
    )

    executor = Executor()

    # Test Click
    action = Action(
        reasoning="Testing click",
        action=ActionType.CLICK,
        x=500,
        y=500,
    )

    print(executor.execute_action(action))

    # Test Type
    action = Action(
        reasoning="Testing type",
        action=ActionType.TYPE,
        text="Hello World!",
    )

    print(executor.execute_action(action))

    # Test Scroll
    action = Action(
        reasoning="Testing scroll",
        action=ActionType.SCROLL,
        direction=ScrollDirection.DOWN,
    )

    print(executor.execute_action(action))

    # Test Wait
    action = Action(
        reasoning="Testing wait",
        action=ActionType.WAIT,
    )

    print(executor.execute_action(action))

    # Test Done
    action = Action(
        reasoning="Testing done",
        action=ActionType.DONE,
    )

    print(executor.execute_action(action))
