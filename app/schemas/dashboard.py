from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class OverallRisk(BaseModel):
    score: float
    category: str

class CorridorRisk(BaseModel):
    corridor: str
    score: float
    category: str

class TopCorridor(BaseModel):
    id: str
    name: str
    share_pct: float
    risk_score: float

class RiskTrendPoint(BaseModel):
    date: str
    score: float

class DemandForecastPoint(BaseModel):
    date: str
    forecasted_demand_tmt: float
    forecast_lower: float
    forecast_upper: float
    forecasted_demand_bpd: int
    forecast_lower_bpd: int
    forecast_upper_bpd: int

class PriceAnomalyPoint(BaseModel):
    date: str
    price: float
    price_change_pct: Optional[float]
    anomaly_flag: bool
    anomaly_score: float

class DashboardResponse(BaseModel):
    import_dependency_pct: float = 88.0
    hormuz_share_pct: float = 42.0
    reserve_days: float = 9.5
    total_daily_import_bpd: int = 4700000
    overall_risk: OverallRisk
    corridor_risks: List[CorridorRisk]
    top_corridors: List[TopCorridor] = []
    risk_trend: List[RiskTrendPoint] = []
    ml_demand_forecast: Optional[List[DemandForecastPoint]] = None
    ml_price_anomalies: Optional[List[PriceAnomalyPoint]] = None
