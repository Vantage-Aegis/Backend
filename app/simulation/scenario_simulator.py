import uuid
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List
from app.services.risk_engine import calculate_risk, calculate_ml_risk
from app.services.twin_service import propagate_disruption
from app.services.recommendation_engine import rank_alternatives
from app.services.reserve_optimizer import optimize_reserves
from app.services.decision_engine import generate_recommendations

PRICE_ELASTICITY_FACTOR = 0.45
AVG_ALT_ROUTE_PREMIUM_USD_PER_BBL = 3.50
DAILY_GDP_BASELINE_USD = 10270000000.0  # ~$3.75T annual GDP / 365 days

def run_simulation(params: Dict[str, Any], routes: List[Dict[str, Any]], suppliers: List[Dict[str, Any]], refineries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Executes complete end-to-end disruption scenario simulation pipeline.
    Includes supply loss, price impact %, extra transport costs, and GDP macroeconomic impact.
    """
    event_type = params.get("event_type", "hormuz_closure")
    severity = int(params.get("severity", 5))
    duration_days = int(params.get("duration_days", 30))
    demand_delta_pct = float(params.get("demand_delta_pct", 0.0))
    corridor_id = params.get("affected_corridor_id", "corr_hormuz")
    supplier_id = params.get("affected_supplier_id")
    port_id = params.get("affected_port_id")

    # 1. Propagate graph disruption
    affected = propagate_disruption(
        corridor_id=corridor_id,
        severity=severity,
        routes=routes,
        refineries=refineries,
        suppliers=suppliers,
        supplier_id=supplier_id,
        port_id=port_id
    )

    # 2. Calculate lost supply & deficit
    baseline_supply = 4700000
    affected_edge_ids = set(affected["edges"])
    
    lost_supply = 0
    for r in routes:
        if r["_id"] in affected_edge_ids:
            lost_supply += int(r.get("current_flow_bpd", 0) * (severity / 5.0))

    if lost_supply == 0 and (event_type == "hormuz_closure" or corridor_id == "corr_hormuz"):
        logger = logging.getLogger("uvicorn.error")
        logger.warning(f"Propagation logic returned 0 lost supply for {event_type}. Using Hormuz baseline fallback.")
        lost_supply = 1974000  # Default ~42% disruption

    remaining_supply = max(0, baseline_supply - lost_supply)
    adjusted_demand = int(baseline_supply * (1.0 + (demand_delta_pct / 100.0)))
    deficit = max(0, adjusted_demand - remaining_supply)

    # 3. Estimate economic & macro impacts (prices, transport premiums, and GDP)
    supply_shock_pct = (lost_supply / baseline_supply) * 100.0 if baseline_supply > 0 else 42.0
    price_impact_pct = round(supply_shock_pct * PRICE_ELASTICITY_FACTOR, 1)
    extra_transport_cost = round(deficit * AVG_ALT_ROUTE_PREMIUM_USD_PER_BBL, 2)

    # Macro GDP elasticity estimate: -0.15% GDP loss per 1M bpd unmitigated deficit
    gdp_impact_pct = round(-0.15 * (deficit / 1000000.0) * (severity / 5.0), 2)
    gdp_impact_usd_per_day = round(abs(gdp_impact_pct / 100.0) * DAILY_GDP_BASELINE_USD, 2)

    # 4. Calculate scenario risk score
    shipping_disruption_val = min(100.0, severity * 20.0)
    risk_factors = {
        "shipping_disruption": shipping_disruption_val,
        "geopolitical_tension": 85.0 if severity >= 4 else 70.0,
        "sanctions": 70.0 if severity >= 4 else 40.0,
        "corridor_dependency": 85.0 if corridor_id == "corr_hormuz" else 60.0,
        "supplier_dependency": 75.0 if severity >= 4 else 50.0,
        "conflict_intensity": 80.0 if severity >= 4 else 50.0,
        "historical_disruption": 60.0,
        "price_volatility": 65.0
    }
    
    det_risk = calculate_risk(risk_factors, entity_type="corridor")
    ml_risk_res = calculate_ml_risk(risk_factors)
    
    # Severe disruption should be Critical/High (>75 or >=85)
    final_score = det_risk["score"]
    if severity >= 5 and corridor_id == "corr_hormuz":
        final_score = max(final_score, 88.0)
    elif ml_risk_res and "ml_score" in ml_risk_res and ml_risk_res["ml_score"] > 50:
        final_score = round((det_risk["score"] * 0.5) + (ml_risk_res["ml_score"] * 0.5), 1)

    category = "Critical" if final_score > 75.0 else "High" if final_score > 55.0 else "Medium" if final_score > 30.0 else "Low"
    
    risk_res = {
        "score": final_score,
        "category": category,
        "factors": risk_factors,
        "shap_top3": ml_risk_res.get("shap_top3", []) if ml_risk_res else []
    }

    # 5. Rank alternative routes
    alternatives = rank_alternatives(deficit, routes, suppliers, list(affected_edge_ids))

    # 6. Strategic reserve drawdown plan
    reserve_plan = optimize_reserves(deficit, duration_days)

    # 7. Generate executable action recommendations
    action_objs = generate_recommendations(risk_res, deficit, baseline_supply, alternatives, reserve_plan)
    recommendation_strings = [a["action"] for a in action_objs]

    now_utc = datetime.now(timezone.utc)
    scenario_id = f"scn_{now_utc.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:4]}"

    return {
        "scenario_id": scenario_id,
        "risk": risk_res,
        "affected": affected,
        "affected_suppliers": affected.get("affected_suppliers", []),
        "affected_refineries": affected.get("affected_refinery_names", []),
        "supply_impact": {
            "baseline_supply_bpd": baseline_supply,
            "lost_supply_bpd": lost_supply,
            "remaining_supply_bpd": remaining_supply,
            "deficit_bpd": deficit,
            "price_impact_pct": price_impact_pct,
            "extra_transport_cost_usd_per_day": extra_transport_cost,
            "gdp_impact_pct": gdp_impact_pct,
            "gdp_impact_usd_per_day": gdp_impact_usd_per_day
        },
        "alternatives": alternatives,
        "reserve_plan": {
            "days_of_coverage": reserve_plan["days_of_coverage"],
            "drawdown_bpd_avg": reserve_plan["drawdown_bpd_avg"],
            "safety_floor_bbl": reserve_plan["safety_floor_bbl"]
        },
        "recommendations": recommendation_strings,
        "action_cards": action_objs,
        "created_at": now_utc.isoformat()
    }
