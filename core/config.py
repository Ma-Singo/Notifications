from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool | None = False
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    ALGORITHM: str


    model_config = SettingsConfigDict(
        env_file = BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,

    )

@lru_cache
def get_settings() -> Settings:
    """
    Creates a cached instance of the settings class
    """
    return Settings()

settings = Settings()