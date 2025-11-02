"""
Notification management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserUpdate, UserOut
from .. import models
from jose import jwt
import os

router = APIRouter()

ALGO = "HS256"
SECRET = os.environ.get("JWT_SECRET", "devsecret")


def get_current_user_id(authorization: str = Header(default=None)) -> int:
    """Extract user ID from JWT token."""
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        return int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.put("/settings", response_model=UserOut)
def update_notification_settings(
    settings: UserUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Update user notification preferences."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update settings
    if settings.phone_number is not None:
        user.phone_number = settings.phone_number
    if settings.email_notifications is not None:
        user.email_notifications = settings.email_notifications
    if settings.sms_notifications is not None:
        user.sms_notifications = settings.sms_notifications
    if settings.name is not None:
        user.name = settings.name
    
    db.commit()
    db.refresh(user)
    return user


@router.get("/settings", response_model=UserOut)
def get_notification_settings(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Get user notification preferences."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
