from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    MONGODB_URI: str
    DATABASE_NAME: str = "energy_resilience_db"
    GEMINI_API_KEY: str
    LLM_MODEL: str = "gemini-2.5-flash"
    ENABLE_GDELT_POLLING: bool = True
    GDELT_POLL_INTERVAL_MINUTES: int = 15

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
