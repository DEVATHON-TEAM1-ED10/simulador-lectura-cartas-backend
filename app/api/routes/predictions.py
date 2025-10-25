from fastapi import APIRouter, HTTPException, status
from app.db.session import SessionLocal
from app.schemas.prediction import PredictionIn
from app.models.card import Card as CardDB

router = APIRouter(prefix="/api/predictions", tags=["predictions"])

@router.post("")
def create_prediction_stub(payload: PredictionIn):
    selected_cards = []
    db = SessionLocal()

    for card_id in payload.card_ids:
        card = db.query(CardDB).where(CardDB.id == card_id).first()

        if not card:
            if card_id > 22:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Card {card_id} no existe. Son 22 cartas")
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Card {card_id} no encontrada")

        selected_cards.append(card)

    if len(selected_cards) != 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Debes escoger exactamente 3 cartas")

    # Calcular el tono
    total_energy = sum(card.energy for card in selected_cards)
    if total_energy > 1:
        tone = "positive"
    elif total_energy < -1:
        tone = "challenging"
    else:
        tone = "neutral"

    # Crear narrativa
    narrative = (
        f"Pasado: {selected_cards[0].meaning}\n"
        f"Presente: {selected_cards[1].meaning}\n"
        f"Futuro: {selected_cards[2].meaning}"
    )

    alternative_narrative = [
        {"position": "Pasado", "text": selected_cards[0].meaning},
        {"position": "Presente", "text": selected_cards[1].meaning},
        {"position": "Futuro", "text": selected_cards[2].meaning},
    ]

    return {
        "total_energy": total_energy,
        "tone": tone,
        "message": narrative,
        "message_alternative": alternative_narrative,
        "cards": [
            {
                "id": c.id,
                "name": c.name,
                "image": c.image,
                "meaning": c.meaning,
                "energy": c.energy,
            }
            for c in selected_cards
        ]
    }
