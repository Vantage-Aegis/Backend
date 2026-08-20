from fastapi import APIRouter, Depends, Query
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.schemas.risk import RiskResponse
from app.services.risk_engine import calculate_risk, calculate_ml_risk, calculate_ml_risk_async
from datetime import datetime, timezone

router = APIRouter(prefix="/api/risk", tags=["Risk Intelligence"])

@router.get("", response_model=RiskResponse)
async def get_risk(
    entity_type: Optional[str] = Query("corridor", description="corridor or supplier"),
    entity_id: Optional[str] = Query("corr_hormuz", description="Entity ID"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Returns detailed risk score breakdown and factor metrics for a given corridor or supplier.
    """
    if entity_type == "supplier":
        sup = await db.suppliers.find_one({"_id": entity_id})
        rel = sup.get("reliability_score", 0.9) if sup else 0.9
        export_bpd = sup.get("current_export_bpd", 500000) if sup else 500000
        
        factors = {
            "geopolitical_tension": round((1.0 - rel) * 100 + 40, 1),
            "sanctions": 60.0 if entity_id in ["sup_russia", "sup_iran"] else 20.0,
            "conflict_intensity": 50.0,
            "shipping_disruption": 45.0,
            "corridor_dependency": 40.0,
            "supplier_dependency": round(min(100.0, (export_bpd / 4700000.0) * 300.0), 1),
            "historical_disruption": 35.0,
            "price_volatility": 40.0
        }
        res = calculate_risk(factors, entity_type="supplier")
        ml_res = await calculate_ml_risk_async(factors, db=db, entity_id=entity_id, entity_type="supplier") or {}
        
        doc = {
            "entity_type": "supplier",
            "entity_id": entity_id,
            "score": res["score"],
            "category": res["category"],
            "factors": res["factors"],
            "ml_score": ml_res.get("ml_score"),
            "shap_top3": ml_res.get("shap_top3"),
            "computed_at": datetime.now(timezone.utc).isoformat()
        }
        await db.risk_scores.update_one(
            {"entity_type": "supplier", "entity_id": entity_id},
            {"$set": doc},
            upsert=True
        )

        return RiskResponse(
            entity_id=entity_id,
            entity_type="supplier",
            score=res["score"],
            category=res["category"],
            factors=res["factors"],
            ml_score=ml_res.get("ml_score"),
            shap_top3=ml_res.get("shap_top3")
        )

    # Corridor risk
    corr = await db.corridors.find_one({"_id": entity_id}) or await db.corridors.find_one({"name": entity_id})
    base_risk = corr.get("base_risk", 61.0) if corr else 61.0
    share_pct = corr.get("share_of_india_imports_pct", 42.0) if corr else 42.0

    factors = {
        "geopolitical_tension": round(base_risk * 1.15, 1),
        "sanctions": 40.0,
        "conflict_intensity": round(base_risk * 0.9, 1),
        "shipping_disruption": base_risk,
        "corridor_dependency": round(min(100.0, share_pct * 2.0), 1),
        "supplier_dependency": 60.0,
        "historical_disruption": round(base_risk * 0.8, 1),
        "price_volatility": round(base_risk * 0.9, 1)
    }
    res = calculate_risk(factors, entity_type="corridor")
    corr_id = entity_id or "corr_hormuz"
    ml_res = await calculate_ml_risk_async(factors, db=db, entity_id=corr_id, entity_type="corridor") or {}
    
    doc = {
        "entity_type": "corridor",
        "entity_id": corr_id,
        "score": res["score"],
        "category": res["category"],
        "factors": res["factors"],
        "ml_score": ml_res.get("ml_score"),
        "shap_top3": ml_res.get("shap_top3"),
        "computed_at": datetime.now(timezone.utc).isoformat()
    }
    await db.risk_scores.update_one(
        {"entity_type": "corridor", "entity_id": corr_id},
        {"$set": doc},
        upsert=True
    )

    return RiskResponse(
        entity_id=corr_id,
        entity_type="corridor",
        score=res["score"],
        category=res["category"],
        factors=res["factors"],
        ml_score=ml_res.get("ml_score"),
        shap_top3=ml_res.get("shap_top3")
    )
