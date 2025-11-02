"""
Notification Preferences Management
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..schemas import UserUpdate, UserOut
from jose import jwt
import os

router = APIRouter()

SECRET = os.environ.get("JWT_SECRET", "devsecret")
ALGO = "HS256"


def get_current_user_id(authorization: str | None = Header(default=None)) -> int:
    """Get current user ID from JWT token."""
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        return int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/preferences", response_model=UserOut)
def get_notification_preferences(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Get user notification preferences."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/preferences", response_model=UserOut)
def update_notification_preferences(
    preferences: UserUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Update user notification preferences."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if preferences.phone_number is not None:
        user.phone_number = preferences.phone_number
    if preferences.email_notifications is not None:
        user.email_notifications = preferences.email_notifications
    if preferences.sms_notifications is not None:
        user.sms_notifications = preferences.sms_notifications
    
    db.commit()
    db.refresh(user)
    return user
