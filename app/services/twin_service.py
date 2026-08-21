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
            "corridors": rt.get("corridors", []),
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
    suppliers: List[Dict[str, Any]] = None,
    supplier_id: str = None,
    port_id: str = None
) -> Dict[str, Any]:
    """
    BFS disruption propagation:
    Given a disrupted corridor, supplier, or port and severity level (1-5), flags affected routes, ports, and downstream refineries.
    Supports multi-corridor array checking.
    """
    routes = routes or []
    refineries = refineries or []
    suppliers = suppliers or []
    
    supplier_map = {s["_id"]: s.get("name", s["_id"]) for s in suppliers}
    refinery_map = {r["_id"]: r.get("name", r["_id"]) for r in refineries}

    affected_edges = []
    affected_ports: Set[str] = set()
    affected_supplier_names: Set[str] = set()

    for r in routes:
        is_affected = False
        r_corridors = r.get("corridors", [])
        if corridor_id and (
            r.get("corridor_id") == corridor_id or
            r.get("corridor") == corridor_id or
            corridor_id in str(r.get("corridor")) or
            corridor_id in r_corridors or
            any(corridor_id in str(c) for c in r_corridors)
        ):
            is_affected = True
        elif supplier_id and r.get("from_node") == supplier_id:
            is_affected = True
        elif port_id and r.get("to_node") == port_id:
            is_affected = True

        if is_affected:
            affected_edges.append(r["_id"])
            if r.get("to_node"):
                affected_ports.add(r["to_node"])
            if r.get("from_node"):
                from_id = r["from_node"]
                sup_name = supplier_map.get(from_id, from_id.replace("sup_", "").replace("_", " ").title())
                affected_supplier_names.add(sup_name)
            # Update edge status and capacity
            r["status"] = "blocked" if severity >= 5 else "degraded"
            r["effective_capacity_bpd"] = int(r.get("capacity_bpd", 0) * (1 - severity / 5.0))

    affected_refinery_ids: Set[str] = set()
    affected_refinery_names: Set[str] = set()

    for ref in refineries:
        connected = ref.get("connected_ports", [])
        # Refinery affected if any connected port receives blocked/degraded supply
        if connected and any(p_id in affected_ports for p_id in connected):
            ref_id = ref["_id"]
            affected_refinery_ids.add(ref_id)
            affected_refinery_names.add(refinery_map.get(ref_id, ref.get("name", ref_id)))

    return {
        "edges": affected_edges,
        "ports": list(affected_ports),
        "refineries": list(affected_refinery_ids),
        "affected_suppliers": sorted(list(affected_supplier_names)),
        "affected_refinery_names": sorted(list(affected_refinery_names))
    }

