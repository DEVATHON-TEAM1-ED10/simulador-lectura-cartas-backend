from fastapi import APIRouter, HTTPException, status
from app.schemas.prediction import PredictionIn

router = APIRouter(prefix="/api/predictions", tags=["predictions"])

@router.post("")
def create_prediction_stub(payload: PredictionIn):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Predictions endpoint not implemented (scaffold)"
    )
