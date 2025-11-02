"""
OTP Authentication endpoints for history access
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from ..database import get_db
from ..services.otp_service import otp_service
from .. import models
from jose import jwt
import os

router = APIRouter()

ALGO = "HS256"
SECRET = os.environ.get("JWT_SECRET", "devsecret")


class OTPRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class OTPVerify(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    otp: str


class OTPSession(BaseModel):
    session_token: str
    expires_in: int


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


@router.post("/request", response_model=dict)
def request_otp(
    request: OTPRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    Request OTP for history access.
    Sends OTP to user's email or phone if configured.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    success = False
    method = None
    identifier = None
    
    # Try email first
    if request.email or user.email:
        identifier = request.email or user.email
        _, success = otp_service.send_otp_email(identifier, user.name)
        method = "email"
    
    # If email failed and phone provided, try SMS
    if not success and (request.phone or user.phone_number):
        identifier = request.phone or user.phone_number
        _, success = otp_service.send_otp_sms(identifier, user.name)
        method = "sms"
    
    if not success:
        raise HTTPException(
            status_code=400,
            detail="Failed to send OTP. Please ensure your email or phone number is configured in your account settings."
        )
    
    return {
        "message": f"OTP sent to your {method}",
        "method": method,
        "identifier": identifier[:3] + "****" + identifier[-3:] if len(identifier) > 6 else "****"  # Mask identifier
    }


@router.post("/verify", response_model=OTPSession)
def verify_otp(
    verify: OTPVerify,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    Verify OTP and return a temporary session token for history access.
    Session token is valid for 30 minutes.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    identifier = verify.email or verify.phone or user.email or user.phone_number
    if not identifier:
        raise HTTPException(status_code=400, detail="No email or phone number configured")
    
    # Verify OTP
    if not otp_service.verify_otp(identifier, verify.otp):
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")
    
    # Generate session token (valid for 30 minutes)
    from datetime import datetime, timedelta
    payload = {
        "sub": str(user_id),
        "role": user.role,
        "otp_verified": True,
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "iat": datetime.utcnow()
    }
    
    session_token = jwt.encode(payload, SECRET, algorithm=ALGO)
    
    return OTPSession(
        session_token=session_token,
        expires_in=1800  # 30 minutes in seconds
    )

