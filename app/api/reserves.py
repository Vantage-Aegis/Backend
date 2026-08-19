from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.schemas.reserve import ReserveOptimizeRequest, ReserveOptimizeResponse
from app.services.reserve_optimizer import optimize_reserves

router = APIRouter(prefix="/api/reserves", tags=["Strategic Reserves"])

@router.post("/optimize", response_model=ReserveOptimizeResponse)
async def optimize_reserve_drawdown(req: ReserveOptimizeRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Computes day-by-day strategic reserve drawdown schedule and coverage limits.
    """
    deficit = req.deficit_bpd

    if deficit is None and req.scenario_id:
        scen_doc = await db.scenario_results.find_one({"scenario_id": req.scenario_id})
        if scen_doc and "supply_impact" in scen_doc:
            deficit = scen_doc["supply_impact"].get("deficit_bpd", 1974000)

    if deficit is None:
        deficit = 1974000

    plan = optimize_reserves(deficit_bpd=deficit, duration_days=req.duration_days or 30)

    return ReserveOptimizeResponse(
        days=plan["days"],
        days_of_coverage=plan["days_of_coverage"],
        safety_floor_bbl=plan["safety_floor_bbl"]
    )
