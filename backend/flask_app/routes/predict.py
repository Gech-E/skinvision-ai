"""Prediction and persistence endpoints."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from ..database import session_scope
from ..models import PredictionResult
from ..services.inference import get_predictor
from ..services.storage import save_image_bytes

predict_bp = Blueprint("predict", __name__)


@predict_bp.route("/predict", methods=["POST"])
def predict_route():
    if "file" not in request.files:
        return jsonify({"error": "Missing file"}), 400

    file_storage = request.files["file"]
    file_bytes = file_storage.read()
    if not file_bytes:
        return jsonify({"error": "Empty file"}), 400

    predictor = get_predictor()
    inference = predictor.predict(file_bytes)
    saved_path = save_image_bytes(file_bytes, file_storage.filename)

    response = {
        **inference,
        "image_path": saved_path,
    }
    return jsonify(response)


@predict_bp.route("/save-result", methods=["POST"])
def save_result_route():
    payload = request.get_json(force=True, silent=True)
    if not payload:
        return jsonify({"error": "Invalid JSON"}), 400

    required = ["predicted_class", "confidence"]
    missing = [key for key in required if key not in payload]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    try:
        confidence = float(payload["confidence"])
    except (ValueError, TypeError):
        return jsonify({"error": "Confidence must be numeric"}), 400

    record = PredictionResult(
        image_path=payload.get("image_path"),
        predicted_class=payload["predicted_class"],
        confidence=confidence,
    )

    with session_scope() as session:
        session.add(record)
        session.flush()
        result = record.to_dict()

    return jsonify(result), 201
