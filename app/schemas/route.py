from pydantic import BaseModel
from typing import List

class RouteAlternative(BaseModel):
    supplier: str
    route_id: str
    route_name: str
    available_bpd: int
    landed_cost_usd_bbl: float
    transit_days: int
    risk_score: float
    score: float
    reason: str

class RoutesResponse(BaseModel):
    scenario_id: str
    routes: List[RouteAlternative]
