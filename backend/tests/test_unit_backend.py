import io
import numpy as np
from PIL import Image

from app import crud, schemas
from app.routers.predict import preprocess_image
from app.routers import auth as auth_router


def test_crud_create_and_list(db_session):
    # Clear any existing predictions for user 1
    from app import models
    db_session.query(models.Prediction).filter(models.Prediction.user_id == 1).delete()
    db_session.commit()
    
    data = schemas.PredictionCreate(
        image_url="/static/a.png",
        predicted_class="Melanoma",
        confidence=0.9,
        heatmap_url="/static/a_hm.png",
    )
    rec = crud.create_prediction(db_session, data, user_id=1)
    assert rec.id is not None
    assert rec.user_id == 1

    all_recs = crud.list_predictions_for_user(db_session, 1)
    assert len(all_recs) == 1
    assert all_recs[0].predicted_class == "Melanoma"


def test_preprocess_image_returns_batched_normalized_array():
    img = Image.new("RGB", (300, 200), (255, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    arr = preprocess_image(buf.getvalue())
    assert isinstance(arr, np.ndarray)
    assert arr.shape == (1, 224, 224, 3)
    assert 0.0 <= float(arr.max()) <= 1.0


def test_password_hash_and_verify():
    password = "S3cret!"
    hashed = auth_router.get_password_hash(password)
    assert hashed and hashed != password
    assert auth_router.verify_password(password, hashed) is True


