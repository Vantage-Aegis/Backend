import pytest
from app.simulation.scenario_simulator import run_simulation
from app.services.reserve_optimizer import optimize_reserves

def test_reserve_optimizer_drawdown():
    plan = optimize_reserves(deficit_bpd=1974000, duration_days=30)
    assert len(plan["days"]) == 30
    assert plan["days_of_coverage"] > 0
    assert plan["safety_floor_bbl"] == 8000000

def test_run_simulation_pipeline():
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

    res = run_simulation({"event_type": "hormuz_closure", "severity": 5}, dummy_routes, dummy_suppliers, dummy_refineries)
    assert "scenario_id" in res
    assert res["supply_impact"]["deficit_bpd"] > 0
    assert "gdp_impact_pct" in res["supply_impact"]
    assert "gdp_impact_usd_per_day" in res["supply_impact"]
    assert len(res["recommendations"]) > 0
