from typing import List, Dict, Any

ROUTE_WEIGHTS = {
    "available_supply": 0.20,
    "route_risk": 0.20,
    "capacity": 0.15,
    "landed_cost": 0.15,
    "lead_time": 0.10,
    "reliability": 0.10,
    "existing_dependency_penalty": 0.10
}

def rank_alternatives(deficit_bpd: int, routes: List[Dict[str, Any]], suppliers: List[Dict[str, Any]], excluded_route_ids: List[str]) -> List[Dict[str, Any]]:
    """
    Evaluates and ranks candidate alternative crude procurement routes and suppliers.
    """
    supplier_map = {s["_id"]: s for s in suppliers}
    candidates = []
    
    # Try loading ML Ranker
    ranker_model = None
    ranker_features = None
    try:
        import xgboost as xgb
        import pandas as pd
        import json
        from pathlib import Path
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        MODELS_DIR = BASE_DIR / "ml" / "models"
        if (MODELS_DIR / "xgboost_ranker_model.json").exists() and (MODELS_DIR / "ranker_features.json").exists():
            ranker_model = xgb.XGBRanker()
            ranker_model.load_model(MODELS_DIR / "xgboost_ranker_model.json")
            with open(MODELS_DIR / "ranker_features.json", "r") as f:
                ranker_features = json.load(f)
    except Exception as e:
        print(f"ML Ranker load failed: {e}")

    for r in routes:
        if r["_id"] in excluded_route_ids or r.get("status") == "blocked":
            continue

        sup = supplier_map.get(r["from_node"], {})
        sup_name = sup.get("name", "Alternative Supplier")
        
        current_flow = r.get("current_flow_bpd", 0)
        max_cap = r.get("capacity_bpd", current_flow)
        spare_capacity = max(0, max_cap - current_flow)
        if spare_capacity <= 0:
            continue

        available_bpd = min(deficit_bpd if deficit_bpd > 0 else 500000, spare_capacity)

        base_price = sup.get("base_price_usd_bbl", 82.0)
        freight_cost = r.get("transport_cost_usd_bbl", 3.0)
        landed_cost = round(base_price + freight_cost, 2)
        
        transit_days = r.get("lead_time_days", 10)
        risk_score = r.get("risk_base", 30.0)
        reliability = sup.get("reliability_score", 0.9)

        # Compute multi-factor suitability score (0.0 to 1.0)
        supply_score = min(1.0, available_bpd / 500000.0)
        risk_norm = max(0.0, 1.0 - (risk_score / 100.0))
        capacity_norm = min(1.0, max_cap / 1000000.0)
        cost_norm = max(0.0, 1.0 - ((landed_cost - 70.0) / 30.0))
        lead_time_norm = max(0.0, 1.0 - (transit_days / 40.0))
        reliability_norm = reliability
        dependency_penalty = 0.9  # slight penalty factor for existing large suppliers

        final_score = (
            supply_score * ROUTE_WEIGHTS["available_supply"] +
            risk_norm * ROUTE_WEIGHTS["route_risk"] +
            capacity_norm * ROUTE_WEIGHTS["capacity"] +
            cost_norm * ROUTE_WEIGHTS["landed_cost"] +
            lead_time_norm * ROUTE_WEIGHTS["lead_time"] +
            reliability_norm * ROUTE_WEIGHTS["reliability"] +
            dependency_penalty * ROUTE_WEIGHTS["existing_dependency_penalty"]
        )

        # ML Score fallback
        ml_score = None
        if ranker_model and ranker_features:
            try:
                import pandas as pd
                row = {
                    "volume_000t": available_bpd / 20.0,
                    "value_million_usd": available_bpd * landed_cost / 1000.0,
                    "unit_cost_usd_per_t": landed_cost,
                    "route_risk_score": float(risk_score),
                    "supplier_reliability": float(reliability),
                    "import_share_pct_qty": 5.0,
                    "cost_competitiveness": 1.0,
                }
                row = {col: row.get(col, 0.0) for col in ranker_features}
                df = pd.DataFrame([row])
                raw_score = float(ranker_model.predict(df)[0])
                ml_score = max(0.0, min(1.0, (raw_score + 5) / 10.0))
            except Exception:
                pass

        PORT_NAMES = {
            "port_mundra": "Mundra",
            "port_vadinar": "Vadinar",
            "port_jnpt": "JNPT",
            "port_mumbai": "Mumbai",
            "port_kochi": "Kochi",
            "port_mangalore": "Mangalore",
            "port_vizag": "Vizag",
            "port_paradip": "Paradip",
            "port_ennore": "Ennore",
            "port_chennai": "Chennai",
            "port_haldia": "Haldia",
            "port_kakinada": "Kakinada",
            "port_kandla": "Kandla"
        }
        dest_port = PORT_NAMES.get(r.get("to_node"), r.get("to_node", "").replace("port_", "").title())
        risk_label = "Low risk" if risk_score < 30 else "Medium risk" if risk_score < 55 else "High risk"

        route_name = f"{r.get('corridor', 'Direct')} ({r['from_node']} -> {r['to_node']})"
        reason = f"{risk_label} ({int(risk_score)}) with {available_bpd:,} bpd available spare capacity via {transit_days}-day transit."

        candidates.append({
            "supplier": sup_name,
            "dest_port": dest_port,
            "route_id": r["_id"],
            "route_name": route_name,
            "available_bpd": available_bpd,
            "landed_cost_usd_bbl": landed_cost,
            "transit_days": transit_days,
            "risk_score": float(risk_score),
            "score": round(final_score, 2),
            "ml_score": round(ml_score, 2) if ml_score is not None else None,
            "reason": reason
        })

    # Sort descending by ml_score if available, otherwise deterministic score
    candidates.sort(key=lambda x: x["ml_score"] if x.get("ml_score") is not None else x["score"], reverse=True)
    
    # Assign ML Rank
    for i, c in enumerate(candidates):
        if c.get("ml_score") is not None:
            c["ml_rank"] = i + 1
            
    return candidates
