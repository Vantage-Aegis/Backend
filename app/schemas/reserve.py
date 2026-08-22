from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class ReserveOptimizeRequest(BaseModel):
    scenario_id: Optional[str] = "hormuz_closure_v1"
    algorithm: Optional[str] = "greedy"  # "greedy" or "lp"
    include_planned: Optional[bool] = False
    deficit_bpd: Optional[int] = None
    duration_days: Optional[int] = 30
    custom_gap_forecast: Optional[List[Dict[str, Any]]] = None

class ReserveOptimizeResponse(BaseModel):
    scenario_id: str
    generated_at: str
    algorithm: str
    daily_schedule: List[Dict[str, Any]]
    summary: Dict[str, Any]
    sites_info: List[Dict[str, Any]]
    baseline_info: Dict[str, Any]
    current_reserves_bbl: float
    daily_consumption_bpd: float
    safety_floor_days: float
    safety_floor_bbl: float
    days_of_coverage: float
    drawdown_bpd_avg: float
    timeline: List[Dict[str, Any]]
    plan: Optional[List[Dict[str, Any]]] = None
    constraints: List[str]
