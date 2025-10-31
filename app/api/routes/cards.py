from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from app.schemas.card import Card, DrawResponse
from app.services.cards import list_cards, draw_cards

router = APIRouter(prefix="/api/cards", tags=["cards"])

@router.get("", response_model=list[Card])
def get_cards():
    """Devuelve todas las cartas (sin orientación)."""
    return list_cards()

@router.get("/draw", response_model=DrawResponse)
def draw_endpoint(
    count: int = Query(3, ge=1, description="Cantidad de cartas a sortear"),
    seed: Optional[int] = Query(None, description="Semilla para reproducibilidad"),
):
    """Sortea N cartas únicas con orientación (upright/reversed)."""
    try:
        drawn = draw_cards(count=count, seed=seed)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return DrawResponse(seed=seed, count=count, cards=drawn)
