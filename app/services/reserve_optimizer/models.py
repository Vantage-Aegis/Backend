from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

@dataclass
class ReserveSite:
    site_id: str
    site_name: str
    state: str
    status: str  # "operational" or "planned_not_operational"
    capacity_mmt: float
    capacity_million_bbl: float
    current_fill_pct: float
    current_fill_million_bbl: float
    safety_floor_pct: float
    max_drawdown_rate_kbpd: float
    data_type: str
    source_or_basis: str

    @property
    def is_operational(self) -> bool:
        return self.status.lower() == "operational"

    @property
    def capacity_kbbl(self) -> float:
        return self.capacity_million_bbl * 1000.0

    @property
    def current_fill_kbbl(self) -> float:
        return self.current_fill_million_bbl * 1000.0

    @property
    def safety_floor_kbbl(self) -> float:
        return self.capacity_kbbl * (self.safety_floor_pct / 100.0)

    @property
    def available_drawdown_capacity_kbbl(self) -> float:
        return max(0.0, self.current_fill_kbbl - self.safety_floor_kbbl)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "site_id": self.site_id,
            "site_name": self.site_name,
            "state": self.state,
            "status": self.status,
            "capacity_mmt": self.capacity_mmt,
            "capacity_million_bbl": self.capacity_million_bbl,
            "current_fill_pct": self.current_fill_pct,
            "current_fill_million_bbl": round(self.current_fill_million_bbl, 2),
            "safety_floor_pct": self.safety_floor_pct,
            "safety_floor_million_bbl": round(self.safety_floor_kbbl / 1000.0, 2),
            "available_reserve_million_bbl": round(self.available_drawdown_capacity_kbbl / 1000.0, 2),
            "max_drawdown_rate_kbpd": self.max_drawdown_rate_kbpd,
            "data_type": self.data_type,
            "source_or_basis": self.source_or_basis
        }

@dataclass
class NationalBaseline:
    metrics: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    @property
    def total_crude_consumption_kbpd(self) -> float:
        return float(self.metrics.get("total_crude_consumption", {}).get("value", 5600.0))

    @property
    def import_dependency_pct(self) -> float:
        return float(self.metrics.get("import_dependency_pct", {}).get("value", 88.0))

    @property
    def spr_total_capacity_million_bbl(self) -> float:
        return float(self.metrics.get("spr_total_capacity_million_bbl", {}).get("value", 39.05))

    @property
    def spr_current_fill_pct(self) -> float:
        return float(self.metrics.get("spr_current_fill_pct", {}).get("value", 64.0))

    def to_dict(self) -> Dict[str, Any]:
        return {k: v.get("value") for k, v in self.metrics.items()}

@dataclass
class DailyForecast:
    scenario_id: str
    day: int
    date: str
    forecast_gap_kbpd: float
    confidence_pct: float
    trigger_event: str

@dataclass
class DailyDrawdownResult:
    day: int
    date: str
    forecast_gap_kbpd: float
    drawdown_by_site: Dict[str, float]  # kbpd per site
    total_drawn_kbpd: float
    residual_shortfall_kbpd: float
    reserve_level_after: Dict[str, float]  # kbbl remaining per site
    reserve_level_after_million_bbl: Dict[str, float]  # million bbl remaining per site
    status: str  # "MET" or "UNMET"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "date": self.date,
            "forecast_gap_kbpd": round(self.forecast_gap_kbpd, 1),
            "drawdown_by_site": {k: round(v, 1) for k, v in self.drawdown_by_site.items()},
            "total_drawn_kbpd": round(self.total_drawn_kbpd, 1),
            "residual_shortfall_kbpd": round(self.residual_shortfall_kbpd, 1),
            "reserve_level_after": {k: round(v, 1) for k, v in self.reserve_level_after.items()},
            "reserve_level_after_million_bbl": {k: round(v, 3) for k, v in self.reserve_level_after_million_bbl.items()},
            "status": self.status
        }

@dataclass
class OptimizationSummary:
    total_gap_kbpd: float
    total_covered_kbpd: float
    total_residual_kbpd: float
    days_until_any_site_hits_safety_floor: Optional[int]
    national_days_of_cover_after_scenario: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_gap_kbpd": round(self.total_gap_kbpd, 1),
            "total_covered_kbpd": round(self.total_covered_kbpd, 1),
            "total_residual_kbpd": round(self.total_residual_kbpd, 1),
            "days_until_any_site_hits_safety_floor": self.days_until_any_site_hits_safety_floor,
            "national_days_of_cover_after_scenario": round(self.national_days_of_cover_after_scenario, 2)
        }
