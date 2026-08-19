from typing import Dict, Any

def compare_scenarios(baseline: Dict[str, Any], scenario_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes side-by-side comparative deltas between baseline and disrupted scenario.
    """
    base_supply = baseline.get("total_daily_import_bpd", 4700000)
    disrupted_supply = scenario_result.get("supply_impact", {}).get("remaining_supply_bpd", 2726000)
    deficit = scenario_result.get("supply_impact", {}).get("deficit_bpd", 1974000)
    price_impact_pct = scenario_result.get("supply_impact", {}).get("price_impact_pct", 18.5)

    base_risk = baseline.get("overall_risk", {}).get("score", 61.0)
    scen_risk = scenario_result.get("risk", {}).get("score", 88.0)

    return {
        "baseline": {
            "daily_import_bpd": base_supply,
            "overall_risk_score": base_risk,
            "overall_risk_category": baseline.get("overall_risk", {}).get("category", "High"),
            "reserve_days": baseline.get("reserve_days", 9.5)
        },
        "disrupted": {
            "daily_import_bpd": disrupted_supply,
            "overall_risk_score": scen_risk,
            "overall_risk_category": scenario_result.get("risk", {}).get("category", "Critical"),
            "deficit_bpd": deficit,
            "price_impact_pct": price_impact_pct,
            "extra_transport_cost_usd_per_day": scenario_result.get("supply_impact", {}).get("extra_transport_cost_usd_per_day", 3200000)
        },
        "delta": {
            "import_drop_bpd": base_supply - disrupted_supply,
            "risk_score_increase": round(scen_risk - base_risk, 1),
            "reserve_days_coverage": scenario_result.get("reserve_plan", {}).get("days_of_coverage", 6.2)
        }
    }
