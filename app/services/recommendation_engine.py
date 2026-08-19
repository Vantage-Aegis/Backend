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

    for r in routes:
        if r["_id"] in excluded_route_ids or r.get("status") == "blocked":
            continue

        sup = supplier_map.get(r["from_node"], {})
        sup_name = sup.get("name", "Alternative Supplier")
        
        current_flow = r.get("current_flow_bpd", 0)
        max_cap = r.get("capacity_bpd", current_flow)
        spare_capacity = max(0, max_cap - current_flow)
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

        route_name = f"{r.get('corridor', 'Direct')} ({r['from_node']} -> {r['to_node']})"
        reason = f"Low risk ({risk_score}) with {available_bpd:,} bpd available spare capacity via {transit_days}-day transit."

        candidates.append({
            "supplier": sup_name,
            "dest_port": r.get("to_node", "").replace("port_", "").upper(),
            "route_id": r["_id"],
            "route_name": route_name,
            "available_bpd": available_bpd,
            "landed_cost_usd_bbl": landed_cost,
            "transit_days": transit_days,
            "risk_score": float(risk_score),
            "score": round(final_score, 2),
            "reason": reason
        })

    # Sort descending by score
    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates
