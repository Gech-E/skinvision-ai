"""History endpoints for retrieving stored predictions."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from ..database import session_scope
from ..models import PredictionResult

history_bp = Blueprint("history", __name__)


@history_bp.route("/history", methods=["GET"])
def list_history():
    limit = request.args.get("limit", default=25, type=int)
    limit = max(1, min(limit, 200))

    with session_scope() as session:
        rows = (
            session.query(PredictionResult)
            .order_by(PredictionResult.timestamp.desc())
            .limit(limit)
            .all()
        )
        data = [row.to_dict() for row in rows]

    return jsonify({"items": data, "count": len(data)})
