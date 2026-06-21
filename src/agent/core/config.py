import pyautogui
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    LOGIC_MODEL: str = "llama-3.3-70b-versatile"
    VISION_MODEL: str = "meta-llama/llama-4-scout-17b-16e-instruct"
    MAX_STEPS: int = 15
    WAIT_SECONDS: float = 1.5
    SCREENSHOT_WIDTH: int = 1280

    GEMINI_API_KEY: str = Field(default="", min_length=1)
    GROQ_API_KEY: str = Field(default="", min_length=1)


model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore",
)


settings = Settings()

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
