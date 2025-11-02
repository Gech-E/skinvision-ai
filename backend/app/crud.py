from sqlalchemy.orm import Session
from . import models, schemas


def create_prediction(db: Session, data: schemas.PredictionCreate, user_id: int | None = None) -> models.Prediction:
    pred = models.Prediction(
        image_url=data.image_url,
        predicted_class=data.predicted_class,
        confidence=data.confidence,
        heatmap_url=data.heatmap_url,
        user_id=user_id,
    )
    db.add(pred)
    db.commit()
    db.refresh(pred)
    return pred


def list_predictions(db: Session):
    return db.query(models.Prediction).order_by(models.Prediction.timestamp.desc()).all()


def list_predictions_for_user(db: Session, user_id: int):
    return (
        db.query(models.Prediction)
        .filter(models.Prediction.user_id == user_id)
        .order_by(models.Prediction.timestamp.desc())
        .all()
    )


def delete_prediction(db: Session, pred_id: int) -> bool:
    pred = db.query(models.Prediction).filter(models.Prediction.id == pred_id).first()
    if not pred:
        return False
    db.delete(pred)
    db.commit()
    return True


