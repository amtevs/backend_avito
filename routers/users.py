from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.moderation import predict_violation

router = APIRouter()

class PredictRequest(BaseModel):
    seller_id: int
    is_verified_seller: bool
    item_id: int
    name: str
    description: str
    category: int
    images_qty: int


@router.post("/predict", response_model=bool)
async def predict(data: PredictRequest) -> bool:
    try:
        return predict_violation(
            is_verified_seller=data.is_verified_seller,
            images_qty=data.images_qty,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка при обработке объявления",
        ) from exc