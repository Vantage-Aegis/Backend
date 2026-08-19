from pydantic import BaseModel
from typing import List

class ActionCard(BaseModel):
    rank: int
    action: str
    score: float
    reason: str

class RecommendationsResponse(BaseModel):
    scenario_id: str
    actions: List[ActionCard]
