from pydantic import BaseModel, Field
from typing import List, Optional

class PredictionIn(BaseModel):
    # exactamente 3 IDs
    card_ids: List[int] = Field(min_length=3, max_length=3)
    seed: Optional[int] = None

class PredictionOut(BaseModel):
    total_energy: int
    category: str
    message: str
