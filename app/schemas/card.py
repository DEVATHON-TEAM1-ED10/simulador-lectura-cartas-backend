from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class Card(BaseModel):
    id: int
    name: str
    meaning: str
    image: str
    energy: int = Field(..., description='Rango -2 a +2')

class DrawnCard(BaseModel):
    card: 'Card'
    orientation: Literal['upright', 'reversed']

class DrawResponse(BaseModel):
    seed: Optional[int] = None
    count: int
    cards: List['DrawnCard']

