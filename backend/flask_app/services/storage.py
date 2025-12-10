"""File-system helpers for persisting uploaded images."""

from __future__ import annotations

import secrets
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..config import settings


def save_image_bytes(data: bytes, original_filename: Optional[str] = None) -> str:
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    ext = Path(original_filename or "upload.jpg").suffix or ".jpg"
    filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{secrets.token_hex(8)}{ext}"
    target_path = settings.upload_dir / filename
    with open(target_path, "wb") as f:
        f.write(data)
    return str(target_path)
