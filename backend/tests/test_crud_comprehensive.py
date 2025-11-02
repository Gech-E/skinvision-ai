"""Comprehensive CRUD operation tests."""
import pytest
from datetime import datetime

from app import crud, schemas, models


def test_create_prediction_with_all_fields(db_session):
    """Test creating a prediction with all fields populated."""
    data = schemas.PredictionCreate(
        image_url="/static/test_image.jpg",
        predicted_class="Melanoma",
        confidence=0.95,
        heatmap_url="/static/heatmap_test_image.jpg"
    )
    
    pred = crud.create_prediction(db_session, data, user_id=1)
    
    assert pred.id is not None
    assert pred.image_url == "/static/test_image.jpg"
    assert pred.predicted_class == "Melanoma"
    assert pred.confidence == 0.95
    assert pred.heatmap_url == "/static/heatmap_test_image.jpg"
    assert pred.user_id == 1
    assert pred.timestamp is not None


def test_create_prediction_without_user_id(db_session):
    """Test creating a prediction without user_id (anonymous user)."""
    data = schemas.PredictionCreate(
        image_url="/static/test.jpg",
        predicted_class="Nevus",
        confidence=0.78
    )
    
    pred = crud.create_prediction(db_session, data, user_id=None)
    
    assert pred.id is not None
    assert pred.user_id is None


def test_list_predictions_for_user_filters_correctly(db_session):
    """Test that listing predictions filters by user_id."""
    # Create predictions for different users
    for user_id in [1, 1, 2, 1]:
        data = schemas.PredictionCreate(
            image_url=f"/static/img_{user_id}.jpg",
            predicted_class="BCC",
            confidence=0.85
        )
        crud.create_prediction(db_session, data, user_id=user_id)
    
    # Get predictions for user 1
    user1_preds = crud.list_predictions_for_user(db_session, 1)
    
    assert len(user1_preds) == 3
    assert all(p.user_id == 1 for p in user1_preds)
    
    # Get predictions for user 2
    user2_preds = crud.list_predictions_for_user(db_session, 2)
    assert len(user2_preds) == 1
    assert user2_preds[0].user_id == 2


def test_list_all_predictions(db_session):
    """Test listing all predictions regardless of user."""
    # Create multiple predictions
    for i in range(5):
        data = schemas.PredictionCreate(
            image_url=f"/static/img_{i}.jpg",
            predicted_class="AK",
            confidence=0.7 + (i * 0.05)
        )
        crud.create_prediction(db_session, data, user_id=i % 3)
    
    all_preds = crud.list_predictions(db_session)
    
    assert len(all_preds) == 5


def test_list_predictions_ordered_by_timestamp(db_session):
    """Test that predictions are ordered by timestamp descending."""
    # Create predictions with small delays
    import time
    
    pred_ids = []
    for i in range(3):
        data = schemas.PredictionCreate(
            image_url=f"/static/img_{i}.jpg",
            predicted_class="Benign",
            confidence=0.6
        )
        pred = crud.create_prediction(db_session, data, user_id=1)
        pred_ids.append(pred.id)
        time.sleep(0.01)  # Small delay to ensure different timestamps
    
    preds = crud.list_predictions_for_user(db_session, 1)
    
    # Should be in descending order (newest first)
    timestamps = [p.timestamp for p in preds]
    assert timestamps == sorted(timestamps, reverse=True)


def test_delete_prediction_success(db_session):
    """Test successfully deleting a prediction."""
    # Create a prediction
    data = schemas.PredictionCreate(
        image_url="/static/to_delete.jpg",
        predicted_class="Melanoma",
        confidence=0.9
    )
    pred = crud.create_prediction(db_session, data, user_id=1)
    pred_id = pred.id
    
    # Delete it
    result = crud.delete_prediction(db_session, pred_id)
    assert result is True
    
    # Verify it's gone
    remaining = crud.list_predictions_for_user(db_session, 1)
    assert all(p.id != pred_id for p in remaining)


def test_delete_prediction_nonexistent(db_session):
    """Test deleting a non-existent prediction returns False."""
    result = crud.delete_prediction(db_session, 99999)
    assert result is False


def test_multiple_disease_classes(db_session):
    """Test predictions with different disease classes."""
    classes = ["Melanoma", "Nevus", "BCC", "AK", "Benign"]
    
    for disease in classes:
        data = schemas.PredictionCreate(
            image_url=f"/static/{disease.lower()}.jpg",
            predicted_class=disease,
            confidence=0.85
        )
        crud.create_prediction(db_session, data, user_id=1)
    
    preds = crud.list_predictions_for_user(db_session, 1)
    assert len(preds) == 5
    
    predicted_classes = {p.predicted_class for p in preds}
    assert predicted_classes == set(classes)
