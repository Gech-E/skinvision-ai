"""Reusable preprocessing helpers shared by the Colab notebook and the Flask API."""

from __future__ import annotations

import io
from pathlib import Path
from typing import BinaryIO, Union

import numpy as np
from PIL import Image

IMAGE_SIZE = (224, 224)


def load_image(source: Union[str, Path, BinaryIO, bytes]) -> Image.Image:
    """Load an image from disk, raw bytes, or an open file-like object."""
    if isinstance(source, (str, Path)):
        image = Image.open(source)  # type: ignore[arg-type]
    elif isinstance(source, bytes):
        image = Image.open(io.BytesIO(source))
    elif hasattr(source, "read"):
        image = Image.open(source)  # type: ignore[arg-type]
    else:
        raise ValueError("Unsupported image source type")
    return image.convert("RGB")


def preprocess_image(image: Image.Image) -> np.ndarray:
    """Resize to 224x224, normalize pixels to [0, 1], and add a batch dimension."""
    resized = image.resize(IMAGE_SIZE)
    array = np.asarray(resized).astype("float32") / 255.0
    batch = np.expand_dims(array, axis=0)
    return batch


def preprocess_from_source(source: Union[str, Path, BinaryIO, bytes]) -> np.ndarray:
    """Convenience wrapper that loads and preprocesses an image in one call."""
    return preprocess_image(load_image(source))
