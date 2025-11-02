import io
from PIL import Image
from jose import jwt
import os


def _make_image_bytes(color=(0, 128, 255)) -> bytes:
    img = Image.new("RGB", (256, 256), color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _auth_header_for(user_id: int, role: str = "user") -> dict:
    # Mirror the app's signing defaults
    secret = os.environ.get("JWT_SECRET", "devsecret")
    token = jwt.encode({"sub": str(user_id), "role": role}, secret, algorithm="HS256")
    return {"Authorization": f"Bearer {token}"}


def test_signup_and_login_flow(client):
    email = "user@example.com"
    password = "example123"

    r = client.post("/auth/signup", json={"email": email, "password": password})
    assert r.status_code == 200
    assert r.json()["email"] == email

    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token


def test_predict_creates_record_without_real_model(client):
    img_bytes = _make_image_bytes()
    files = {"file": ("test.png", img_bytes, "image/png")}
    headers = _auth_header_for(1)
    # Ensure model load fails and falls back to stub path
    os.environ["MODEL_PATH"] = "__nonexistent__model__.h5"
    r = client.post("/predict", files=files, headers=headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["image_url"].startswith("/static/")
    assert data["heatmap_url"].startswith("/static/")
    assert 0.0 <= float(data["confidence"]) <= 1.0


def test_history_requires_auth_and_lists_user_records(client):
    # Unauthenticated should 401
    r = client.get("/history/")
    assert r.status_code == 401

    # With auth should work
    headers = _auth_header_for(1)
    r = client.get("/history/", headers=headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


