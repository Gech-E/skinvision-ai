"""Integration tests for authentication flow."""
import os


def test_complete_auth_flow_signup_login_predict(client):
    """Test complete authentication flow: signup → login → predict."""
    email = "flow@example.com"
    password = "TestPass123!"
    
    # Step 1: Signup
    signup_response = client.post(
        "/auth/signup",
        json={"email": email, "password": password}
    )
    assert signup_response.status_code == 200
    user_data = signup_response.json()
    assert user_data["email"] == email
    assert "id" in user_data
    
    # Step 2: Login
    login_response = client.post(
        "/auth/login",
        json={"email": email, "password": password}
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    token = token_data["access_token"]
    
    # Step 3: Use token for authenticated request
    headers = {"Authorization": f"Bearer {token}"}
    history_response = client.get("/history/", headers=headers)
    assert history_response.status_code == 200


def test_login_with_wrong_password_fails(client):
    """Test that login with wrong password fails."""
    email = "wrongpass@example.com"
    password = "CorrectPass123"
    
    # Signup
    client.post("/auth/signup", json={"email": email, "password": password})
    
    # Try login with wrong password
    login_response = client.post(
        "/auth/login",
        json={"email": email, "password": "WrongPass456"}
    )
    
    assert login_response.status_code == 401


def test_signup_duplicate_email_fails(client):
    """Test that signing up with duplicate email fails."""
    email = "duplicate@example.com"
    password = "Password123"
    
    # First signup succeeds
    response1 = client.post("/auth/signup", json={"email": email, "password": password})
    assert response1.status_code == 200
    
    # Second signup with same email fails
    response2 = client.post("/auth/signup", json={"email": email, "password": password})
    assert response2.status_code == 400
    assert "already registered" in response2.json()["detail"].lower()


def test_first_user_becomes_admin(client):
    """Test that the first user registered becomes admin."""
    email = "firstadmin@example.com"
    password = "AdminPass123"
    
    response = client.post("/auth/signup", json={"email": email, "password": password})
    user_data = response.json()
    
    assert user_data["role"] == "admin"


def test_subsequent_users_are_not_admin(client):
    """Test that users after the first are regular users."""
    # Create first user (admin)
    client.post("/auth/signup", json={"email": "admin1@example.com", "password": "pass1"})
    
    # Create second user (should be user, not admin)
    response = client.post("/auth/signup", json={"email": "user2@example.com", "password": "pass2"})
    user_data = response.json()
    
    assert user_data["role"] == "user"


def test_jwt_token_works_for_protected_endpoints(client):
    """Test that JWT token from login works for protected endpoints."""
    email = "jwt@example.com"
    password = "JWTTest123"
    
    # Signup and login
    client.post("/auth/signup", json={"email": email, "password": password})
    login_response = client.post("/auth/login", json={"email": email, "password": password})
    token = login_response.json()["access_token"]
    
    # Use token for history endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/history/", headers=headers)
    
    assert response.status_code == 200


def test_invalid_token_rejected(client):
    """Test that invalid JWT tokens are rejected."""
    headers = {"Authorization": "Bearer invalid_token_here"}
    
    response = client.get("/history/", headers=headers)
    
    assert response.status_code == 401


def test_missing_token_rejected(client):
    """Test that missing token results in 401."""
    response = client.get("/history/")
    
    assert response.status_code == 401
