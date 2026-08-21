from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any

class ScenarioSimulateRequest(BaseModel):
    event_type: str  # "hormuz_closure", "redsea_disruption", "supplier_disruption", "port_disruption"
    affected_corridor_id: Optional[str] = "corr_hormuz"
    affected_supplier_id: Optional[str] = None
    affected_port_id: Optional[str] = None
    severity: int = 5  # 1 to 5 scale
    duration_days: int = 30
    demand_delta_pct: float = 0.0

class AffectedEntities(BaseModel):
    edges: List[str]
    ports: List[str]
    refineries: List[str]
    affected_suppliers: Optional[List[str]] = []
    affected_refinery_names: Optional[List[str]] = []

class SupplyImpact(BaseModel):
    baseline_supply_bpd: int
    lost_supply_bpd: int
    remaining_supply_bpd: int
    deficit_bpd: int
    price_impact_pct: float
    extra_transport_cost_usd_per_day: float
    gdp_impact_pct: float = 0.0
    gdp_impact_usd_per_day: float = 0.0

class AlternativeRoute(BaseModel):
    supplier: str
    route_id: str
    route_name: str
    available_bpd: int
    landed_cost_usd_bbl: float
    transit_days: int
    risk_score: float
    score: float
    reason: str

class ReservePlanSummary(BaseModel):
    days_of_coverage: float
    drawdown_bpd_avg: int
    safety_floor_bbl: int

class ScenarioSimulateResponse(BaseModel):
    scenario_id: str
    risk: Dict[str, Any]
    affected: AffectedEntities
    affected_suppliers: Optional[List[str]] = []
    affected_refineries: Optional[List[str]] = []
    supply_impact: SupplyImpact
    alternatives: List[AlternativeRoute]
    reserve_plan: ReservePlanSummary
    recommendations: List[str]

class ScenarioTemplate(BaseModel):
    id: str = Field(..., alias="_id")
    label: str
    event_type: str
    default_severity: int
    default_duration_days: int
    description: str
    affected_corridor_id: Optional[str] = None
    affected_supplier_id: Optional[str] = None
    affected_port_id: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)
