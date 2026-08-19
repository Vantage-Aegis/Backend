from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.schemas.explanation import ExplainRequest, ExplanationResponse
from app.agents.explanation_agent import generate_explanation

router = APIRouter(prefix="/api/explain", tags=["AI Explanation Agent"])

@router.post("", response_model=ExplanationResponse)
async def explain_scenario(req: ExplainRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Generates an AI executive narrative explanation for decision-makers using Gemini LLM.
    Cached in `ai_explanations` MongoDB collection.
    """
    cached = await db.ai_explanations.find_one({"scenario_id": req.scenario_id})
    if cached:
        return ExplanationResponse(**cached)

    scen_doc = await db.scenario_results.find_one({"scenario_id": req.scenario_id})
    if not scen_doc:
        # Default mock scenario data payload for generation if ID not stored
        scen_doc = {
            "scenario_id": req.scenario_id,
            "risk": {"score": 88.0, "category": "Critical"},
            "disruption": {"event": "Hormuz Closure", "severity": 5, "duration_days": 30},
            "supply_impact": {"baseline_supply_bpd": 4700000, "lost_supply_bpd": 1974000, "deficit_bpd": 1974000, "price_impact_pct": 18.5},
            "alternatives": [{"supplier": "UAE (Fujairah Bypass)", "score": 0.81}],
            "reserve_plan": {"days_of_coverage": 6.2, "drawdown_bpd_avg": 320000}
        }

    explanation_res = await generate_explanation(scen_doc)
    explanation_res["scenario_id"] = req.scenario_id

    # Cache explanation in DB
    await db.ai_explanations.update_one(
        {"scenario_id": req.scenario_id},
        {"$set": explanation_res},
        upsert=True
    )

    return ExplanationResponse(**explanation_res)
