"""Configuration module using Pydantic settings."""

from pydantic import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    BOT_TOKEN: str
    ADMIN_IDS: List[int]
    DB_URL: str = "postgresql+psycopg2://postgres:postgres@db:5432/postgres"
    CHANNEL_ID: int
    REDIS_URL: str = "redis://redis:6379/0"

    class Config:
        env_file = ".env"


settings = Settings()
