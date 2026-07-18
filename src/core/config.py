from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
model_config = SettingsConfigDict(env_file=BASE_DIR / '.env', extra='ignore')

class Settings(BaseSettings):
    app_name: str = 'SmartNotes'
    debug: bool = True
    static_dir: str = 'static'
    DATABASE_URL: str
    BOT_TOKEN: str
    GEMINI_API_KEY: str
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

setting = Settings()