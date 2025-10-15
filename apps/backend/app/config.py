from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application configuration."""

    storage_dir: Path = Path(__file__).resolve().parent.parent / "storage"
    content_dir: Path = Path(__file__).resolve().parent / "content"
    cors_origins: List[str] = ["http://localhost:5173"]

    class Config:
        env_prefix = "WUXIA_"
        env_file = ".env"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance."""

    settings = Settings()
    settings.storage_dir.mkdir(parents=True, exist_ok=True)
    return settings
