"""Integration tests for history endpoints."""
import os
import io
from PIL import Image
from jose import jwt


def _make_test_image() -> bytes:
    img = Image.new("RGB", (256, 256), (128, 128, 128))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _get_token(user_id=1, role="user"):
    secret = os.environ.get("JWT_SECRET", "devsecret")
    return f"Bearer {jwt.encode({'sub': str(user_id), 'role': role}, secret, algorithm='HS256')}"


def test_full_prediction_to_history_flow(client):
    """Test complete flow: predict → save → retrieve from history."""
    # Step 1: Make a prediction
    img_bytes = _make_test_image()
    files = {"file": ("flow_test.png", img_bytes, "image/png")}
    headers = {"Authorization": _get_token(user_id=5)}
    
    predict_response = client.post("/predict", files=files, headers=headers)
    assert predict_response.status_code == 200
    pred_data = predict_response.json()
    pred_id = pred_data["id"]
    
    # Step 2: Retrieve from history
    history_response = client.get("/history/", headers=headers)
    assert history_response.status_code == 200
    history = history_response.json()
    
    # Step 3: Verify prediction is in history
    assert any(p["id"] == pred_id for p in history)
    found = next(p for p in history if p["id"] == pred_id)
    assert found["predicted_class"] == pred_data["predicted_class"]
    assert found["confidence"] == pred_data["confidence"]


def test_history_shows_only_user_predictions(client):
    """Test that history endpoint filters by user."""
    # Create predictions for two users
    img_bytes = _make_test_image()
    files = {"file": ("user1.png", img_bytes, "image/png")}
    
    headers_user1 = {"Authorization": _get_token(user_id=10)}
    headers_user2 = {"Authorization": _get_token(user_id=20)}
    
    # User 1 makes prediction
    client.post("/predict", files=files, headers=headers_user1)
    
    # User 2 makes prediction
    files2 = {"file": ("user2.png", img_bytes, "image/png")}
    client.post("/predict", files=files2, headers=headers_user2)
    
    # User 1 checks history
    response = client.get("/history/", headers=headers_user1)
    assert response.status_code == 200
    user1_history = response.json()
    
    # Should only see user 1's predictions
    assert all(p.get("user_id") == 10 for p in user1_history)


def test_delete_prediction_from_history(client):
    """Test deleting a prediction from history."""
    # Create a prediction
    img_bytes = _make_test_image()
    files = {"file": ("delete_test.png", img_bytes, "image/png")}
    headers = {"Authorization": _get_token(user_id=7)}
    
    predict_response = client.post("/predict", files=files, headers=headers)
    pred_id = predict_response.json()["id"]
    
    # Verify it exists
    history = client.get("/history/", headers=headers).json()
    assert any(p["id"] == pred_id for p in history)
    
    # Delete it
    delete_response = client.delete(f"/history/{pred_id}", headers=headers)
    assert delete_response.status_code == 200
    
    # Verify it's gone
    history_after = client.get("/history/", headers=headers).json()
    assert not any(p["id"] == pred_id for p in history_after)


def test_delete_other_users_prediction_fails(client):
    """Test that users cannot delete other users' predictions."""
    img_bytes = _make_test_image()
    headers_user1 = {"Authorization": _get_token(user_id=30)}
    headers_user2 = {"Authorization": _get_token(user_id=31)}
    
    # User 1 creates prediction
    files = {"file": ("user1_pred.png", img_bytes, "image/png")}
    pred = client.post("/predict", files=files, headers=headers_user1).json()
    pred_id = pred["id"]
    
    # User 2 tries to delete it
    delete_response = client.delete(f"/history/{pred_id}", headers=headers_user2)
    
    # Should fail (403 or 404)
    assert delete_response.status_code in [403, 404]


def test_admin_can_view_all_predictions(client):
    """Test admin can view all predictions with ?all=true."""
    img_bytes = _make_test_image()
    admin_headers = {"Authorization": _get_token(user_id=100, role="admin")}
    user_headers = {"Authorization": _get_token(user_id=101, role="user")}
    
    # Create predictions from different users
    for i, headers in enumerate([admin_headers, user_headers]):
        files = {"file": (f"pred_{i}.png", img_bytes, "image/png")}
        client.post("/predict", files=files, headers=headers)
    
    # Admin can view all
    response = client.get("/history/?all=true", headers=admin_headers)
    assert response.status_code == 200
    all_preds = response.json()
    assert len(all_preds) >= 2
    
    # Regular user cannot use ?all=true
    response = client.get("/history/?all=true", headers=user_headers)
    assert response.status_code == 403


def test_history_pagination_and_ordering(client):
    """Test that history is ordered by timestamp descending."""
    img_bytes = _make_test_image()
    headers = {"Authorization": _get_token(user_id=50)}
    
    # Create multiple predictions
    pred_ids = []
    for i in range(3):
        import time
        files = {"file": (f"ordered_{i}.png", img_bytes, "image/png")}
        pred = client.post("/predict", files=files, headers=headers).json()
        pred_ids.append(pred["id"])
        time.sleep(0.01)  # Ensure different timestamps
    
    # Get history
    response = client.get("/history/", headers=headers)
    history = response.json()
    
    # Check ordering (newest first)
    timestamps = [p["timestamp"] for p in history if p["id"] in pred_ids]
    assert timestamps == sorted(timestamps, reverse=True)
