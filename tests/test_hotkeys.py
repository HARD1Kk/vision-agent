import logging
import time
from enum import Enum

import pyautogui

# --- 1. Mocking your environment ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ActionType(Enum):
    HOTKEY = "HOTKEY"


class MockAction:
    def __init__(self, action, text):
        self.action = action
        self.text = text


# --- 2. The Alias Dictionary ---
KEY_ALIASES = {
    "windows": "win",
    "control": "ctrl",
    "escape": "esc",
    "return": "enter",
    "cmd": "command",
    "opt": "option",
    "page down": "pgdn",
    "page up": "pgup",
}


# --- 3. Your optimized logic ---
def process_agent_action(action):
    if action.action == ActionType.HOTKEY:
        raw_keys = action.text

        if not raw_keys or not raw_keys.strip():
            logger.error("Failed to execute HOTKEY: No keys provided by the agent.")
            return

        # Parse and translate the keys
        parsed_keys = []
        for k in raw_keys.replace("+", ",").split(","):
            clean_key = k.strip().lower()
            if clean_key:
                # Check the dictionary. If "windows" is found, it becomes "win".
                translated_key = KEY_ALIASES.get(clean_key, clean_key)
                parsed_keys.append(translated_key)

        # Verify parsing worked
        print(f"\n[Success] Raw string '{raw_keys}' parsed into list: {parsed_keys}")

        # Execute with a delay
        if parsed_keys:
            print("[Countdown] Executing in 3 seconds...")
            time.sleep(1)
            print("[Countdown] 2...")
            time.sleep(1)
            print("[Countdown] 1...")
            time.sleep(1)

            pyautogui.hotkey(*parsed_keys)
            print(f"[Fired] Pressed: {' + '.join(parsed_keys)}\n")


# --- 4. Test Cases ---
if __name__ == "__main__":
    print("=== RUNNING HOTKEY TESTS ===")

    print("--- Test A: Normal Input ---")
    action_a = MockAction(ActionType.HOTKEY, "Ctrl + F")
    process_agent_action(action_a)

    print("--- Test B: Messy Input ---")
    action_b = MockAction(ActionType.HOTKEY, " sHift +   a + ")
    process_agent_action(action_b)

    print("--- Test C: Empty Input ---")
    action_c = MockAction(ActionType.HOTKEY, "   ")
    process_agent_action(action_c)

    # Test D: The Alias Test (Windows + R)
    print("--- Test D: The Alias Test ---")
    action_d = MockAction(ActionType.HOTKEY, " Windows + R ")
    process_agent_action(action_d)
