from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.schemas.dashboard import DashboardResponse, OverallRisk, CorridorRisk, TopCorridor, RiskTrendPoint, LiveBrentPriceSummary
from app.services.risk_engine import calculate_risk
from app.services.oil_price_service import OilPriceService
from app.simulation.scenario_simulator import run_simulation
from datetime import datetime, timezone, timedelta
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR.parent / "data" if (BASE_DIR.parent / "data").exists() else BASE_DIR / "data"

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("", response_model=DashboardResponse)
async def get_dashboard(db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Returns baseline dashboard metrics, KPIs, overall risk, corridor risks, top corridors, and risk trend.
    Reads live seeded collections from MongoDB Atlas and live Brent crude market prices.
    """
    corridors_cursor = db.corridors.find({})
    corridors_docs = await corridors_cursor.to_list(length=100)

    events_cursor = db.risk_events.find({})
    events_docs = await events_cursor.to_list(length=100)
    
    routes_docs = await db.routes.find({}).to_list(length=100)

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
        
        # Check if corridor is actively blocked
        corridor_routes = [r for r in routes_docs if r.get("corridor_id") == c_id or r.get("corridor") == c_name]
        is_blocked = any(r.get("status") == "blocked" for r in corridor_routes)
        
        final_score = 100.0 if is_blocked else calc["score"]
        final_cat = "Critical" if is_blocked else calc["category"]

        corridor_risks.append(CorridorRisk(
            corridor=c_name,
            score=final_score,
            category=final_cat
        ))

        top_corridors.append(TopCorridor(
            id=c_id,
            name=c_name,
            share_pct=share_pct,
            risk_score=final_score
        ))

        total_score += final_score

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

    # Load live Brent price and dynamic anomalies (default to 1W view)
    live_brent_summary = None
    ml_price_anomalies = None
    try:
        latest_price_doc = await OilPriceService.get_latest_price(db)
        if latest_price_doc:
            live_brent_summary = LiveBrentPriceSummary(
                price=float(latest_price_doc.get("price", 0.0)),
                formatted=latest_price_doc.get("formatted", f"${float(latest_price_doc.get('price', 0.0)):.2f}"),
                currency=latest_price_doc.get("currency", "USD"),
                unit=latest_price_doc.get("unit", "barrel"),
                price_change_pct=float(latest_price_doc.get("price_change_pct", 0.0) or 0.0),
                change_24h_amount=float(latest_price_doc.get("change_24h_amount", 0.0) or 0.0),
                updated_at=latest_price_doc.get("updated_at") or latest_price_doc.get("timestamp") or datetime.now(timezone.utc).isoformat(),
                source=latest_price_doc.get("source", "oilpriceapi")
            )
        
        # Default dashboard price history to 1M (last 30 days)
        ml_price_anomalies = await OilPriceService.get_price_history(db, timeframe="1M")
    except Exception as e:
        print(f"Error loading live Brent price or anomalies: {e}")
        # Fallback to static JSON file if DB query fails
        anomalies_path = DATA_DIR / "brent_anomalies_output.json"
        if anomalies_path.exists():
            try:
                with open(anomalies_path, "r") as f:
                    ml_price_anomalies = json.load(f)[-30:]
            except Exception:
                pass

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

    # Check for Shadow Scenario (pending approvals)
    shadow_scenario = None
    pending_approval = await db.status_approvals.find_one({"status": "pending"}, sort=[("created_at", -1)])
    if pending_approval:
        refineries_docs = await db.refineries.find({}).to_list(100)
        suppliers_docs = await db.suppliers.find({}).to_list(100)
        
        sim_params = {
            "event_type": "auto_disruption",
            "severity": int(pending_approval.get("severity", 80) / 20),
            "duration_days": 30,
            "demand_delta_pct": 0.0,
            "affected_corridor_id": pending_approval.get("corridor_id")
        }
        shadow_scenario = run_simulation(sim_params, routes_docs, suppliers_docs, refineries_docs)
        shadow_scenario["pending_title"] = pending_approval.get("title", "Pending Disruption")

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
        ml_price_anomalies=ml_price_anomalies,
        live_brent_price=live_brent_summary,
        shadow_scenario=shadow_scenario
    )
