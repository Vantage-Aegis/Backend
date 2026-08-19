from typing import List, Dict, Any, Set
from app.services.risk_engine import calculate_risk

def build_network(suppliers: List[Dict[str, Any]], ports: List[Dict[str, Any]], refineries: List[Dict[str, Any]], routes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Assembles unified digital-twin graph representation (nodes & edges)
    """
    nodes = []

    # Map suppliers to nodes
    for s in suppliers:
        nodes.append({
            "_id": s["_id"],
            "id": s["_id"],
            "type": "supplier",
            "name": s["name"],
            "lat": s["lat"],
            "lng": s["lng"],
            "risk": round((1.0 - s.get("reliability_score", 0.9)) * 100, 1)
        })

    # Map ports to nodes
    for p in ports:
        nodes.append({
            "_id": p["_id"],
            "id": p["_id"],
            "type": p.get("type", "indian_port"),
            "name": p["name"],
            "lat": p["lat"],
            "lng": p["lng"],
            "risk": 15.0 if p.get("type") == "indian_port" else 25.0
        })

    # Map refineries to nodes
    for r in refineries:
        nodes.append({
            "_id": r["_id"],
            "id": r["_id"],
            "type": "refinery",
            "name": r["name"],
            "lat": r["lat"],
            "lng": r["lng"],
            "risk": 10.0
        })

    # Map routes to edges
    edges = []
    for rt in routes:
        base_risk = rt.get("risk_base", 45)
        # Use fuller factors to avoid inflating with defaults
        risk_res = calculate_risk({
            "shipping_disruption": base_risk,
            "corridor_dependency": 60,
            "geopolitical_tension": base_risk * 1.1,
            "sanctions": 20.0,
            "conflict_intensity": base_risk * 0.9,
            "historical_disruption": base_risk * 0.8,
            "price_volatility": base_risk * 0.9,
            "supplier_dependency": 40.0
        }, entity_type="corridor")
        flow = rt.get("current_flow_bpd", 0)
        edges.append({
            "_id": rt["_id"],
            "id": rt["_id"],
            "from": rt["from_node"],
            "to": rt["to_node"],
            "from_node": rt["from_node"],
            "to_node": rt["to_node"],
            "corridor": rt.get("corridor"),
            "corridor_id": rt.get("corridor_id"),
            "risk": risk_res["score"],
            "status": rt.get("status", "active"),
            "flow_bpd": flow,
            "current_flow_bpd": flow,
            "capacity_bpd": rt.get("capacity_bpd", 0),
            "waypoints": rt.get("waypoints", [])
        })

    return {"nodes": nodes, "edges": edges}

def propagate_disruption(
    corridor_id: str = None,
    severity: int = 5,
    routes: List[Dict[str, Any]] = None,
    refineries: List[Dict[str, Any]] = None,
    supplier_id: str = None,
    port_id: str = None
) -> Dict[str, Any]:
    """
    BFS disruption propagation:
    Given a disrupted corridor, supplier, or port and severity level (1-5), flags affected routes, ports, and downstream refineries.
    """
    routes = routes or []
    refineries = refineries or []
    affected_edges = []
    affected_ports: Set[str] = set()

    for r in routes:
        is_affected = False
        if corridor_id and (r.get("corridor_id") == corridor_id or r.get("corridor") == corridor_id):
            is_affected = True
        elif supplier_id and r.get("from_node") == supplier_id:
            is_affected = True
        elif port_id and r.get("to_node") == port_id:
            is_affected = True

        if is_affected:
            affected_edges.append(r["_id"])
            if r.get("to_node"):
                affected_ports.add(r["to_node"])
            # Update edge status and capacity
            r["status"] = "blocked" if severity >= 5 else "degraded"
            r["effective_capacity_bpd"] = int(r.get("capacity_bpd", 0) * (1 - severity/5.0))

    affected_refineries: Set[str] = set()
    for ref in refineries:
        connected = ref.get("connected_ports", [])
        # Refinery affected only if ALL its supply edges are blocked/degraded
        if connected and all(p_id in affected_ports for p_id in connected):
            affected_refineries.add(ref["_id"])

    return {
        "edges": affected_edges,
        "ports": list(affected_ports),
        "refineries": list(affected_refineries)
    }
