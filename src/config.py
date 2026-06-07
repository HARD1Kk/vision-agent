import pyautogui
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODEL: str = "gemini-2.5-flash"
    MAX_STEPS: int = 15
    WAIT_SECONDS: float = 1.5
    SCREENSHOT_WIDTH: int = 1280

    GEMINI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
