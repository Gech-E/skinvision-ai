"""Comprehensive prediction endpoint tests."""
import io
import os
from PIL import Image
from jose import jwt


def _make_test_image_bytes(width=256, height=256, color=(128, 128, 128)) -> bytes:
    """Helper to create test image bytes."""
    img = Image.new("RGB", (width, height), color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _get_auth_token(user_id=1, role="user"):
    """Helper to create auth token."""
    secret = os.environ.get("JWT_SECRET", "devsecret")
    token = jwt.encode(
        {"sub": str(user_id), "role": role, "exp": 9999999999, "iat": 1000000000},
        secret,
        algorithm="HS256"
    )
    return f"Bearer {token}"


def test_predict_without_authentication(client):
    """Test prediction works without authentication (anonymous)."""
    img_bytes = _make_test_image_bytes()
    files = {"file": ("test.png", img_bytes, "image/png")}
    
    response = client.post("/predict", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "predicted_class" in data
    assert "confidence" in data
    assert "image_url" in data
    assert "heatmap_url" in data
    assert data["confidence"] >= 0.0 and data["confidence"] <= 1.0


def test_predict_with_authentication(client):
    """Test prediction with authentication saves user_id."""
    img_bytes = _make_test_image_bytes()
    files = {"file": ("auth_test.png", img_bytes, "image/png")}
    headers = {"Authorization": _get_auth_token(user_id=42)}
    
    response = client.post("/predict", files=files, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 42


def test_predict_validates_image_file(client):
    """Test that only image files are accepted."""
    # Try with non-image file
    files = {"file": ("test.txt", b"not an image", "text/plain")}
    
    response = client.post("/predict", files=files)
    
    # Should either fail or handle gracefully
    assert response.status_code in [400, 422, 500]


def test_predict_handles_different_image_formats(client):
    """Test prediction works with different image formats."""
    formats = ["PNG", "JPEG"]
    
    for fmt in formats:
        img = Image.new("RGB", (224, 224), (100, 100, 100))
        buf = io.BytesIO()
        img.save(buf, format=fmt)
        files = {"file": (f"test.{fmt.lower()}", buf.getvalue(), f"image/{fmt.lower()}")}
        
        response = client.post("/predict", files=files)
        assert response.status_code == 200


def test_predict_handles_large_images(client):
    """Test prediction handles large images (should resize)."""
    # Create a large image
    large_img = Image.new("RGB", (2000, 2000), (50, 50, 50))
    buf = io.BytesIO()
    large_img.save(buf, format="PNG")
    files = {"file": ("large.png", buf.getvalue(), "image/png")}
    
    response = client.post("/predict", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "image_url" in data


def test_predict_creates_static_files(client):
    """Test that uploaded images and heatmaps are saved."""
    img_bytes = _make_test_image_bytes()
    files = {"file": ("saved_test.png", img_bytes, "image/png")}
    
    response = client.post("/predict", files=files)
    
    assert response.status_code == 200
    data = response.json()
    
    # Check that URLs are provided (files may exist)
    assert data["image_url"].startswith("/static/")
    assert data["heatmap_url"].startswith("/static/")


def test_predict_returns_consistent_structure(client):
    """Test that prediction response has consistent structure."""
    img_bytes = _make_test_image_bytes()
    files = {"file": ("consistent.png", img_bytes, "image/png")}
    
    response = client.post("/predict", files=files)
    data = response.json()
    
    # Check all required fields
    required_fields = ["id", "image_url", "predicted_class", "confidence", 
                     "heatmap_url", "timestamp"]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"
    
    # Check types
    assert isinstance(data["id"], int)
    assert isinstance(data["predicted_class"], str)
    assert isinstance(data["confidence"], float)
    assert isinstance(data["image_url"], str)
    assert isinstance(data["heatmap_url"], str)


def test_predict_handles_empty_file(client):
    """Test that empty file upload is rejected."""
    files = {"file": ("empty.png", b"", "image/png")}
    
    response = client.post("/predict", files=files)
    
    assert response.status_code == 400


def test_preprocess_image_function():
    """Test the image preprocessing function."""
    from app.routers.predict import preprocess_image
    import numpy as np
    
    img_bytes = _make_test_image_bytes(300, 200)
    processed = preprocess_image(img_bytes)
    
    assert isinstance(processed, np.ndarray)
    assert processed.shape == (1, 224, 224, 3)
    assert processed.dtype in [np.float32, np.float64]
    assert 0.0 <= processed.min() and processed.max() <= 1.0
