from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas import PredictionOut
from .. import models
from ..crud import list_predictions_for_user, delete_prediction
from jose import jwt, JWTError
from fastapi import Header
from ..database import SessionLocal
from .. import models
import os


ALGO = "HS256"
SECRET = os.environ.get("JWT_SECRET", "devsecret")


def get_current_user_id(authorization: str | None = Header(default=None)) -> int:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id


def is_admin(authorization: str | None = Header(default=None)) -> bool:
    if not authorization or not authorization.lower().startswith("bearer "):
        return False
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        return payload.get("role") == "admin"
    except Exception:
        return False


router = APIRouter()


@router.get("/", response_model=List[PredictionOut])
def get_history(
    db: Session = Depends(get_db),
    authorization: str = Header(default=None),
    all: bool = Query(False, alias="all")
):
    """Get prediction history. Requires authentication. Use ?all=true for admin to see all predictions."""
    admin = is_admin(authorization)
    if all and not admin:
        raise HTTPException(status_code=403, detail="Admin required to view all predictions")
    
    try:
        user_id = get_current_user_id(authorization)
    except HTTPException:
        # Allow viewing all without auth if admin query param is used (for demo)
        if not all:
            raise HTTPException(status_code=401, detail="Authentication required")
        user_id = None
    
    if all and admin:
        # Admin can view all
        return db.query(models.Prediction).order_by(models.Prediction.timestamp.desc()).all()
    elif user_id:
        return list_predictions_for_user(db, user_id)
    else:
        # Fallback: return all if no auth (for development/demo)
        return db.query(models.Prediction).order_by(models.Prediction.timestamp.desc()).all()


@router.delete("/{pred_id}")
def remove_record(pred_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    # Basic authorization: ensure record belongs to user
    recs = list_predictions_for_user(db, user_id)
    if not any(r.id == pred_id for r in recs):
        raise HTTPException(status_code=404, detail="Record not found")
    ok = delete_prediction(db, pred_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"status": "deleted"}


