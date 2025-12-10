"""Database models."""

from __future__ import annotations

from sqlalchemy import Column, DateTime, Float, Integer, String, func

from .database import Base


class PredictionResult(Base):
    __tablename__ = "prediction_results"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String, nullable=True)
    predicted_class = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "image_path": self.image_path,
            "predicted_class": self.predicted_class,
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }
