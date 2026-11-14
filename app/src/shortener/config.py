"""Configuration, read from environment variables only."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    redis_url: str
    base_url: str
    app_version: str


def load_settings() -> Settings:
    """Read the required variables. A missing one raises KeyError and stops startup."""
    return Settings(
        redis_url=os.environ["REDIS_URL"],
        base_url=os.environ["BASE_URL"].rstrip("/"),
        app_version=os.environ["APP_VERSION"],
    )
