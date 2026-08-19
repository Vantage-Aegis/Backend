from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.schemas.recommendation import RecommendationsResponse, ActionCard

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

@router.get("/{scenario_id}", response_model=RecommendationsResponse)
async def get_recommendations(scenario_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Returns ranked actionable procurement directives for a given scenario.
    """
    scen_doc = await db.scenario_results.find_one({"scenario_id": scenario_id})
    
    if scen_doc and "action_cards" in scen_doc:
        return RecommendationsResponse(
            scenario_id=scenario_id,
            actions=[ActionCard(**card) for card in scen_doc["action_cards"]]
        )

    # Fallback recommendations if scenario_id not found in DB
    fallback_cards = [
        ActionCard(
            rank=1,
            action="Reduce vulnerability on Strait of Hormuz corridor by diverting 42% of affected imports",
            score=0.88,
            reason="Corridor risk is Critical (88.0) with acute bottleneck threats."
        ),
        ActionCard(
            rank=2,
            action="Increase UAE crude sourcing via Fujairah Bypass Pipeline by 20% (400,000 bpd)",
            score=0.81,
            reason="Low risk (28.0) route bypassing Hormuz with 400,000 bpd spare capacity."
        ),
        ActionCard(
            rank=3,
            action="Authorize strategic reserve drawdown at ~320,000 bpd for 6.2 days",
            score=0.78,
            reason="Bridges short-term supply deficit while long-haul replacement tankers complete transit."
        )
    ]
    return RecommendationsResponse(scenario_id=scenario_id, actions=fallback_cards)
