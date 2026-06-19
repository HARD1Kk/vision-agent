import logging

import pyautogui

logger = logging.getLogger(__name__)

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


def parse_and_validate_hotkey(raw_keys: str | None) -> list[str]:
    """
    Parses a raw string from the agent, applies aliases,
    and validates against pyautogui's master list.
    """
    if not raw_keys or not raw_keys.strip():
        raise ValueError("No keys provided by the agent.")

    parsed_keys = []

    for k in raw_keys.replace("+", ",").split(","):
        clean_key = k.strip().lower()
        if clean_key:
            # 1. Translate
            translated_key = KEY_ALIASES.get(clean_key, clean_key)

            # 2. Validate
            if translated_key not in pyautogui.KEYBOARD_KEYS:
                raise ValueError(f"Invalid key requested by agent: '{translated_key}'")

            parsed_keys.append(translated_key)

    return parsed_keys
