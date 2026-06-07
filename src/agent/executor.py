
import time

import pyautogui

from agent.core.config import settings
from agent.models import Action, ActionType, ScrollDirection


class Executor:
    def execute_action(self, action:Action)->str:
        """Execute one Action on the real screen and return a short log string"""

        if action.action == ActionType.CLICK:

            if action.x is None or action.y is None:
                raise ValueError("Click action requires x and y coordinates")
            
            width, height = pyautogui.size()
            x = int((action.x  ) / 1000 * width)
            y = int((action.y  ) / 1000 * height)

            pyautogui.click(x,y)
            return f"clicked ({x}, {y})"


        if action.action ==ActionType.TYPE:

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
        
        return f"ActionType.DONE.value"
    
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