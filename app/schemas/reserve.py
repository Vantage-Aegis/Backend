from pydantic import BaseModel
from typing import List, Optional

class ReserveOptimizeRequest(BaseModel):
    scenario_id: Optional[str] = None
    deficit_bpd: Optional[int] = None
    duration_days: Optional[int] = 30

class DayDrawdownRow(BaseModel):
    day: int
    demand_bpd: int
    incoming_supply_bpd: int
    deficit_bpd: int
    reserve_draw_bpd: int
    remaining_reserve_bbl: int

class ReserveOptimizeResponse(BaseModel):
    days: List[DayDrawdownRow]
    days_of_coverage: float
    safety_floor_bbl: int
