from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PredictionCreate(BaseModel):
    image_url: str
    predicted_class: str
    confidence: float
    heatmap_url: Optional[str] = None


class PredictionOut(BaseModel):
    id: int
    image_url: str
    predicted_class: str
    confidence: float
    heatmap_url: Optional[str] = None
    timestamp: datetime
    user_id: Optional[int] = None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):  # optional
    email: EmailStr
    password: str


class Token(BaseModel):  # optional
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    phone_number: Optional[str] = None
    email_notifications: bool = True
    sms_notifications: bool = False
    name: Optional[str] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    phone_number: Optional[str] = None
    email_notifications: Optional[bool] = None
    sms_notifications: Optional[bool] = None
    name: Optional[str] = None


class TokenData(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None


