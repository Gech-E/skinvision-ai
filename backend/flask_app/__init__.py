"""Flask application factory."""

from __future__ import annotations

from flask import Flask
from flask_cors import CORS

from .config import settings
from .database import Base, engine
from .routes.history import history_bp
from .routes.predict import predict_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    CORS(app, resources={r"/*": {"origins": settings.cors_origins or "*"}})

    Base.metadata.create_all(bind=engine)

    app.register_blueprint(predict_bp)
    app.register_blueprint(history_bp)

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    return app
