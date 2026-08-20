from pydantic import BaseModel
from typing import Dict, Optional

class RiskFactorBreakdown(BaseModel):
    geopolitical_tension: float
    sanctions: float
    conflict_intensity: float
    shipping_disruption: float
    corridor_dependency: float
    supplier_dependency: float
    historical_disruption: float
    price_volatility: float

class ShapFeature(BaseModel):
    feature: str
    contribution: float

class RiskResponse(BaseModel):
    entity_id: str
    entity_type: str  # "corridor" or "supplier"
    score: float
    category: str
    factors: Dict[str, float]
    ml_score: Optional[float] = None
    shap_top3: Optional[list[ShapFeature]] = None
