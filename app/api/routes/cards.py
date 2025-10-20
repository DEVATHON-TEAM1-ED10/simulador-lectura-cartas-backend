from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/api/cards", tags=["cards"])

@router.get("")
def list_cards_stub():
    # Solo para validar estructura. No hay DB ni lógica.
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                        detail="Cards endpoint not implemented (scaffold)")
