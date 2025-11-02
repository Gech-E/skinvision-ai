from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext
from ..schemas import UserCreate, Token, TokenData, UserOut
from ..database import get_db
from .. import models
import os, datetime as dt


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGO = "HS256"
SECRET = os.environ.get("JWT_SECRET", "devsecret")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(sub: str, role: str, expires_minutes: int = 60) -> str:
    now = dt.datetime.now(dt.timezone.utc)
    payload = {
        "sub": sub,
        "role": role,
        "exp": now + dt.timedelta(minutes=expires_minutes),
        "iat": now,
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)


@router.post("/signup", response_model=UserOut)
def signup(body: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if email already exists
        existing = db.query(models.User).filter(models.User.email == body.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Determine role (first user becomes admin)
        first_user = db.query(models.User).count() == 0
        role = "admin" if first_user else "user"
        
        # Hash password
        hashed_password = get_password_hash(body.password)
        
        # Create user with default notification preferences
        user = models.User(
            email=body.email, 
            hashed_password=hashed_password, 
            role=role,
            phone_number=getattr(body, 'phone_number', None),  # Optional phone number
            email_notifications="true",  # Enable email by default
            sms_notifications="false"   # Disable SMS by default
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Signup error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create account: {str(e)}")


@router.post("/login", response_model=Token)
def login(body: UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == body.email).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return Token(access_token=create_access_token(str(user.id), user.role))


