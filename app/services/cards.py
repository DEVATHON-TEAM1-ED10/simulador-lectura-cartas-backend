import json
import random
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from app.schemas.card import Card, DrawnCard

# 🔹 Nueva ruta: app/db/cards.json
DATA_PATH = Path(__file__).resolve().parents[1] / "db" / "cards.json"

@lru_cache(maxsize=1)
def _load_cards() -> tuple[Card, ...]:
    """Carga y cachea las cartas desde el JSON."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"No se encontró {DATA_PATH}")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        payload = json.load(f)
    return tuple(Card(**c) for c in payload)

def list_cards() -> List[Card]:
    """Devuelve todas las cartas disponibles."""
    return list(_load_cards())

def draw_cards(count: int = 3, seed: Optional[int] = None) -> List[DrawnCard]:
    """Sortea 'count' cartas únicas, con orientación reproducible (semilla opcional)."""
    cards = list(_load_cards())
    if count < 1:
        raise ValueError("count debe ser >= 1")
    if count > len(cards):
        raise ValueError("count no puede exceder el total de cartas")

    rng = random.Random(seed) if seed is not None else random
    seleccion = rng.sample(cards, k=count)

    drawn: List[DrawnCard] = []
    for c in seleccion:
        orientation = "reversed" if rng.random() < 0.5 else "upright"
        drawn.append(DrawnCard(card=c, orientation=orientation))
    return drawn
