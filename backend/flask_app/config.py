"""Centralized configuration for the Flask backend."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_PATH = ROOT_DIR / "model" / "artifacts" / "model.h5"
DEFAULT_LABEL_MAP_PATH = ROOT_DIR / "model" / "label_map.json"
DEFAULT_UPLOAD_DIR = ROOT_DIR / "uploads"


@dataclass
class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/skinvision",
    )
    model_path: Path = Path(os.getenv("MODEL_PATH", DEFAULT_MODEL_PATH))
    label_map_path: Path = Path(os.getenv("LABEL_MAP_PATH", DEFAULT_LABEL_MAP_PATH))
    upload_dir: Path = Path(os.getenv("UPLOAD_DIR", DEFAULT_UPLOAD_DIR))
    cors_origins: List[str] = field(
        default_factory=lambda: [origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",") if origin]
    )
    debug: bool = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    def ensure_directories(self) -> None:
        self.upload_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_directories()
