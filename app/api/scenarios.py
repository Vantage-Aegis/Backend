from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.schemas.scenario import ScenarioSimulateRequest, ScenarioSimulateResponse, ScenarioTemplate
from app.simulation.scenario_simulator import run_simulation
from app.services.comparison_service import compare_scenarios

router = APIRouter(prefix="/api/scenarios", tags=["Scenario Simulator"])

@router.get("/catalog", response_model=List[ScenarioTemplate])
async def get_scenario_catalog(db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Returns list of predefined disruption scenario templates.
    """
    docs = await db.scenario_templates.find({}).to_list(length=100)
    result = []
    for d in docs:
        result.append(ScenarioTemplate(
            _id=d["_id"],
            id=d["_id"],
            label=d["label"],
            event_type=d["event_type"],
            default_severity=d["default_severity"],
            default_duration_days=d["default_duration_days"],
            description=d.get("description", ""),
            affected_corridor_id=d.get("affected_corridor_id"),
            affected_supplier_id=d.get("affected_supplier_id"),
            affected_port_id=d.get("affected_port_id")
        ))
    return result

@router.post("/simulate", response_model=ScenarioSimulateResponse)
async def simulate_scenario(req: ScenarioSimulateRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Executes full disruption scenario simulation pipeline and persists results in MongoDB Atlas.
    """
    suppliers_docs = await db.suppliers.find({}).to_list(length=100)
    refineries_docs = await db.refineries.find({}).to_list(length=100)
    routes_docs = await db.routes.find({}).to_list(length=100)

    sim_res = run_simulation(req.model_dump(), routes_docs, suppliers_docs, refineries_docs)

    # Persist scenario result in DB
    await db.scenario_results.insert_one(dict(sim_res))

    return ScenarioSimulateResponse(
        scenario_id=sim_res["scenario_id"],
        risk=sim_res["risk"],
        affected=sim_res["affected"],
        supply_impact=sim_res["supply_impact"],
        alternatives=sim_res["alternatives"],
        reserve_plan=sim_res["reserve_plan"],
        recommendations=sim_res["recommendations"]
    )

@router.get("/{scenario_id}/compare")
async def get_scenario_comparison(scenario_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Returns comparative diff analysis between baseline state and simulated disruption scenario.
    """
    sim_doc = await db.scenario_results.find_one({"scenario_id": scenario_id})
    if not sim_doc:
        suppliers_docs = await db.suppliers.find({}).to_list(length=100)
        refineries_docs = await db.refineries.find({}).to_list(length=100)
        routes_docs = await db.routes.find({}).to_list(length=100)
        sim_doc = run_simulation({"event_type": "hormuz_closure"}, routes_docs, suppliers_docs, refineries_docs)

    baseline_data = {
        "total_daily_import_bpd": 4700000,
        "overall_risk": {"score": 61.0, "category": "High"}
    }
    return compare_scenarios(baseline_data, sim_doc)
