from __future__ import annotations

import os
from dotenv import load_dotenv
from typing import NamedTuple


class AppConfig(NamedTuple):
    """Application configuration loaded from environment variables."""
    max_projects: int
    max_tasks: int


def load_config() -> AppConfig:
    """Load configuration values from the .env file."""
    load_dotenv()

    try:
        max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10"))
        max_tasks = int(os.getenv("MAX_NUMBER_OF_TASK", "100"))
    except ValueError as exc:
        raise ValueError("Environment values must be integers.") from exc

    return AppConfig(max_projects=max_projects, max_tasks=max_tasks)
