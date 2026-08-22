from app.simulation.scenario_simulator import run_simulation

def test_standalone_simulation():
    dummy_routes = [
        {"_id": "route_001", "from_node": "sup_saudi", "to_node": "port_jnpt", "corridor_id": "corr_hormuz", "current_flow_bpd": 850000, "capacity_bpd": 900000, "lead_time_days": 9, "risk_base": 61},
        {"_id": "route_002", "from_node": "sup_uae", "to_node": "port_kandla", "corridor_id": "corr_cape", "current_flow_bpd": 400000, "capacity_bpd": 800000, "lead_time_days": 6, "risk_base": 28}
    ]
    dummy_suppliers = [
        {"_id": "sup_saudi", "name": "Saudi Arabia", "base_price_usd_bbl": 82.5, "reliability_score": 0.9},
        {"_id": "sup_uae", "name": "UAE", "base_price_usd_bbl": 83.0, "reliability_score": 0.95}
    ]
    dummy_refineries = [
        {"_id": "ref_jamnagar", "name": "Jamnagar", "connected_ports": ["port_jnpt"]}
    ]

    params = {
        "event_type": "hormuz_closure",
        "affected_corridor_id": "corr_hormuz",
        "severity": 5,
        "duration_days": 30,
        "demand_delta_pct": 0.0
    }
    res = run_simulation(params, dummy_routes, dummy_suppliers, dummy_refineries)
    assert "scenario_id" in res
    assert res["supply_impact"]["deficit_bpd"] > 0
    print("Standalone simulation successful:", res["scenario_id"])

if __name__ == "__main__":
    test_standalone_simulation()
