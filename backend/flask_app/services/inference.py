"""Model loading and prediction utilities."""

from __future__ import annotations

import json
import sys
import threading
from pathlib import Path
from typing import Dict, List

import numpy as np
from tensorflow.keras.models import load_model

# Ensure the repository root (and thus the `model` package) is importable.
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from model import preprocessing  # type: ignore  # pylint: disable=import-error
from ..config import settings


class SkinCancerPredictor:
    """Singleton-like wrapper that lazily loads the TensorFlow model."""

    _instance = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        self.model = load_model(settings.model_path)
        with open(settings.label_map_path, "r", encoding="utf-8") as f:
            mapping = json.load(f)
        self.index_to_label = {int(k): v for k, v in mapping["index_to_label"].items()}
        self.labels: List[str] = [self.index_to_label[idx] for idx in sorted(self.index_to_label.keys())]

    @classmethod
    def instance(cls) -> "SkinCancerPredictor":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def predict(self, image_bytes: bytes) -> Dict[str, object]:
        image = preprocessing.load_image(image_bytes)
        tensor = preprocessing.preprocess_image(image)
        probs = self.model.predict(tensor, verbose=0)[0]
        predictions = [
            {"label": label, "score": float(prob)}
            for label, prob in zip(self.labels, probs)
        ]
        predictions.sort(key=lambda item: item["score"], reverse=True)
        top = predictions[0]
        return {
            "predicted_class": top["label"],
            "confidence": top["score"],
            "probabilities": predictions,
        }


def get_predictor() -> SkinCancerPredictor:
    return SkinCancerPredictor.instance()
