from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.schemas.dashboard import DashboardResponse, OverallRisk, CorridorRisk, TopCorridor, RiskTrendPoint
from app.services.risk_engine import calculate_risk
from datetime import datetime, timezone, timedelta
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("", response_model=DashboardResponse)
async def get_dashboard(db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Returns baseline dashboard metrics, KPIs, overall risk, corridor risks, top corridors, and risk trend.
    Reads live seeded collections from MongoDB Atlas.
    """
    corridors_cursor = db.corridors.find({})
    corridors_docs = await corridors_cursor.to_list(length=100)

    events_cursor = db.risk_events.find({})
    events_docs = await events_cursor.to_list(length=100)

    corridor_risks = []
    top_corridors = []
    total_score = 0.0

    for c in corridors_docs:
        c_name = c.get("name", "Unknown Corridor")
        c_id = c.get("_id", "corr_unknown")
        base_risk = c.get("base_risk", 50.0)
        share_pct = c.get("share_of_india_imports_pct", 30.0)

        matching_evts = [e.get("severity", 50) for e in events_docs if e.get("corridor") == c_name or e.get("corridor_id") == c_id]
        evt_severity = sum(matching_evts) / len(matching_evts) if matching_evts else base_risk

        calc = calculate_risk({
            "shipping_disruption": base_risk,
            "geopolitical_tension": evt_severity,
            "corridor_dependency": share_pct * 1.5
        }, entity_type="corridor")

        corridor_risks.append(CorridorRisk(
            corridor=c_name,
            score=calc["score"],
            category=calc["category"]
        ))

        top_corridors.append(TopCorridor(
            id=c_id,
            name=c_name,
            share_pct=share_pct,
            risk_score=calc["score"]
        ))

        total_score += calc["score"]

    india = await db.countries.find_one({"iso_code": "IND"})
    if not india:
        india = {"total_daily_import_bpd": 4700000, "reserve_days": 9.5}

    # Load ML Demand Forecast if available
    ml_demand_forecast = None
    total_daily_import_bpd = india.get("total_daily_import_bpd", 4700000)
    forecast_path = DATA_DIR / "prophet_forecast_output.json"
    if forecast_path.exists():
        try:
            with open(forecast_path, "r") as f:
                forecast_data = json.load(f)
                ml_demand_forecast = forecast_data.get("forecast", [])
                if ml_demand_forecast:
                    # Use the first future forecast as the current demand metric
                    total_daily_import_bpd = ml_demand_forecast[-1]["forecasted_demand_bpd"]
        except Exception as e:
            print(f"Error loading ML forecast: {e}")

    # Load ML Price Anomalies if available
    ml_price_anomalies = None
    anomalies_path = DATA_DIR / "brent_anomalies_output.json"
    if anomalies_path.exists():
        try:
            with open(anomalies_path, "r") as f:
                # Get the last 24 months of data to avoid sending massive payloads
                ml_price_anomalies = json.load(f)[-24:]
        except Exception as e:
            print(f"Error loading ML anomalies: {e}")

    avg_overall_score = round(total_score / len(corridor_risks), 1) if corridor_risks else 61.0
    overall_cat = "Critical" if avg_overall_score > 75 else "High" if avg_overall_score > 55 else "Medium" if avg_overall_score > 30 else "Low"

    now = datetime.now(timezone.utc)
    trend_points = [
        RiskTrendPoint(date=(now - timedelta(days=20)).strftime("%Y-%m-%d"), score=round(avg_overall_score * 0.85, 1)),
        RiskTrendPoint(date=(now - timedelta(days=15)).strftime("%Y-%m-%d"), score=round(avg_overall_score * 0.90, 1)),
        RiskTrendPoint(date=(now - timedelta(days=10)).strftime("%Y-%m-%d"), score=round(avg_overall_score * 0.95, 1)),
        RiskTrendPoint(date=(now - timedelta(days=5)).strftime("%Y-%m-%d"), score=round(avg_overall_score * 0.98, 1)),
        RiskTrendPoint(date=now.strftime("%Y-%m-%d"), score=avg_overall_score)
    ]

    return DashboardResponse(
        import_dependency_pct=88.0,
        hormuz_share_pct=42.0,
        reserve_days=india.get("reserve_days", 9.5),
        total_daily_import_bpd=total_daily_import_bpd,
        overall_risk=OverallRisk(score=avg_overall_score, category=overall_cat),
        corridor_risks=corridor_risks,
        top_corridors=top_corridors,
        risk_trend=trend_points,
        ml_demand_forecast=ml_demand_forecast,
        ml_price_anomalies=ml_price_anomalies
    )
