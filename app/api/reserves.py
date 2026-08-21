from fastapi import APIRouter, Depends, Query
from typing import Optional, List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.schemas.reserve import ReserveOptimizeRequest, ReserveOptimizeResponse
from app.services.reserve_optimizer import run_reserve_optimization, optimize_reserves
from app.services.reserve_optimizer.loader import load_reserve_sites, load_national_baseline, load_forecast_scenarios

router = APIRouter(prefix="/api/reserves", tags=["Strategic Reserves"])

@router.post("/optimize", response_model=ReserveOptimizeResponse)
async def optimize_reserve_drawdown(
    req: ReserveOptimizeRequest,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Computes day-by-day strategic reserve drawdown schedule and coverage limits.
    Supports Greedy Proportional (MVP) and Linear Programming (LP) algorithms.
    """
    # If custom deficit_bpd provided without a scenario_id or custom forecast
    if req.deficit_bpd and not req.scenario_id and not req.custom_gap_forecast:
        res = optimize_reserves(
            deficit_bpd=req.deficit_bpd,
            duration_days=req.duration_days or 30,
            algorithm=req.algorithm or "greedy"
        )
        return ReserveOptimizeResponse(**res)

    # Check if scenario exists in DB or in preset CSVs
    scen_id = req.scenario_id or "hormuz_closure_v1"
    custom_forecast = req.custom_gap_forecast

    if not custom_forecast and db is not None:
        scen_doc = await db.scenario_results.find_one({"scenario_id": scen_id})
        if scen_doc and "supply_impact" in scen_doc:
            def_bpd = scen_doc["supply_impact"].get("deficit_bpd", 1974000)
            res = optimize_reserves(
                deficit_bpd=def_bpd,
                duration_days=req.duration_days or 30,
                algorithm=req.algorithm or "greedy"
            )
            return ReserveOptimizeResponse(**res)

    res = run_reserve_optimization(
        scenario_id=scen_id,
        algorithm=req.algorithm or "greedy",
        include_planned=req.include_planned or False,
        custom_gap_forecast=custom_forecast
    )

    return ReserveOptimizeResponse(**res)

@router.get("/sites")
async def get_sites():
    """Returns strategic reserve sites telemetry metadata."""
    sites = load_reserve_sites()
    return {"sites": [s.to_dict() for s in sites]}

@router.get("/baseline")
async def get_baseline():
    """Returns national supply baseline metrics."""
    baseline = load_national_baseline()
    return {"baseline": baseline.to_dict()}

@router.get("/scenarios")
async def get_scenarios():
    """Returns pre-configured supply gap forecast scenarios."""
    scenarios = load_forecast_scenarios()
    scen_summary = []
    for scen_id, forecasts in scenarios.items():
        if forecasts:
            scen_summary.append({
                "scenario_id": scen_id,
                "days": len(forecasts),
                "peak_gap_kbpd": max(f.forecast_gap_kbpd for f in forecasts),
                "trigger_event": forecasts[0].trigger_event
            })
    return {"scenarios": scen_summary}
