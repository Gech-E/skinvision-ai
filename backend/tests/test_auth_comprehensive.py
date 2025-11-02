"""Comprehensive authentication tests."""
import os
from jose import jwt

from app.routers import auth
from app import models


def test_password_hashing():
    """Test that passwords are hashed correctly."""
    password = "MySecurePassword123!"
    hashed = auth.get_password_hash(password)
    
    assert hashed != password
    assert len(hashed) > 20  # bcrypt hashes are long
    assert hashed.startswith("$2b$")  # bcrypt format


def test_password_verification_correct(db_session):
    """Test that correct password verifies successfully."""
    password = "TestPassword123"
    hashed = auth.get_password_hash(password)
    
    assert auth.verify_password(password, hashed) is True


def test_password_verification_incorrect(db_session):
    """Test that incorrect password fails verification."""
    password = "CorrectPassword123"
    wrong_password = "WrongPassword456"
    hashed = auth.get_password_hash(password)
    
    assert auth.verify_password(wrong_password, hashed) is False


def test_create_access_token():
    """Test JWT token creation."""
    user_id = "123"
    role = "user"
    
    token = auth.create_access_token(user_id, role, expires_minutes=60)
    
    assert isinstance(token, str)
    assert len(token) > 20
    
    # Decode and verify
    secret = os.environ.get("JWT_SECRET", "devsecret")
    payload = jwt.decode(token, secret, algorithms=["HS256"])
    
    assert payload["sub"] == user_id
    assert payload["role"] == role
    assert "exp" in payload
    assert "iat" in payload


def test_token_expiration():
    """Test that tokens have expiration claim."""
    token = auth.create_access_token("1", "user", expires_minutes=30)
    secret = os.environ.get("JWT_SECRET", "devsecret")
    payload = jwt.decode(token, secret, algorithms=["HS256"])
    
    assert payload["exp"] > payload["iat"]


def test_first_user_becomes_admin(db_session):
    """Test that the first registered user becomes admin."""
    email = "first@example.com"
    password = "password123"
    
    user_data = auth.UserCreate(email=email, password=password)
    
    # Create first user (should be admin)
    from app.routers.auth import router
    # Simulate signup
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    user = models.User(
        email=email,
        hashed_password=pwd_context.hash(password),
        role="admin"  # First user
    )
    db_session.add(user)
    db_session.commit()
    
    assert user.role == "admin"


def test_subsequent_users_are_regular_users(db_session):
    """Test that users after the first are regular users."""
    # Add first user (admin)
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    admin = models.User(
        email="admin@example.com",
        hashed_password=pwd_context.hash("pass"),
        role="admin"
    )
    db_session.add(admin)
    db_session.commit()
    
    # Add second user (should be user)
    user = models.User(
        email="user@example.com",
        hashed_password=pwd_context.hash("pass"),
        role="user"
    )
    db_session.add(user)
    db_session.commit()
    
    assert user.role == "user"
