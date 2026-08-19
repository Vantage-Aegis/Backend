from fastapi import APIRouter, Depends, Query
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.schemas.route import RoutesResponse
from app.services.recommendation_engine import rank_alternatives

router = APIRouter(prefix="/api/routes", tags=["Alternative Routes"])

@router.get("", response_model=RoutesResponse)
async def get_alternative_routes(
    scenario_id: Optional[str] = Query(None),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Returns ranked alternative crude procurement routes and suppliers.
    """
    scen_doc = None
    if scenario_id:
        scen_doc = await db.scenario_results.find_one({"scenario_id": scenario_id})

    if scen_doc and "alternatives" in scen_doc:
        return RoutesResponse(
            scenario_id=scenario_id or "baseline",
            routes=scen_doc["alternatives"]
        )

    # Compute default alternatives
    suppliers = await db.suppliers.find({}).to_list(length=100)
    routes = await db.routes.find({}).to_list(length=100)
    ranked = rank_alternatives(1974000, routes, suppliers, ["route_001", "route_002"])

    return RoutesResponse(
        scenario_id=scenario_id or "default",
        routes=ranked
    )
