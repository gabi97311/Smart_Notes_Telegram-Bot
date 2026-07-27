from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    app_name: str = "SmartNotes"
    debug: bool = True
    static_dir: str = "static"
    DATABASE_URL: str
    BOT_TOKEN: str
    GEMINI_API_KEY: str
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
    )


setting = Settings()
