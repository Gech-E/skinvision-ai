from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


class PredictionCreate(BaseModel):
    image_url: str
    predicted_class: str
    confidence: float
    heatmap_url: Optional[str] = None


class PredictionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    image_url: str
    predicted_class: str
    confidence: float
    heatmap_url: Optional[str] = None
    timestamp: datetime
    user_id: Optional[int] = None


class UserCreate(BaseModel):  # optional
    email: EmailStr
    password: str


class Token(BaseModel):  # optional
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: EmailStr
    role: str
    phone_number: Optional[str] = None
    email_notifications: Optional[str] = "true"
    sms_notifications: Optional[str] = "false"


class UserUpdate(BaseModel):
    phone_number: Optional[str] = None
    email_notifications: Optional[str] = None
    sms_notifications: Optional[str] = None


class TokenData(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None


