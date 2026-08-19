from typing import List, Dict, Any

def generate_recommendations(risk: Dict[str, Any], deficit_bpd: int, baseline_supply_bpd: int, alternatives: List[Dict[str, Any]], reserve_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generates ranked actionable directives based on upstream deterministic calculations.
    """
    actions = []
    rank = 1

    # 1. Primary mitigation action
    disrupted_share_pct = round((deficit_bpd / baseline_supply_bpd) * 100) if baseline_supply_bpd > 0 else 42
    actions.append({
        "rank": rank,
        "action": f"Reduce vulnerability on primary corridor by diverting {disrupted_share_pct}% of affected imports",
        "score": round(risk.get("score", 61.0) / 100.0, 2),
        "reason": f"Risk score is elevated to {risk.get('score')} ({risk.get('category')} category)."
    })
    rank += 1

    # 2. Top alternative procurement actions
    for alt in alternatives[:3]:
        shift_pct = min(100, round((alt["available_bpd"] / deficit_bpd * 100))) if deficit_bpd > 0 else 15
        actions.append({
            "rank": rank,
            "action": f"Increase {alt['supplier']} crude sourcing via {alt['route_name']} by {shift_pct}% ({alt['available_bpd']:,} bpd)",
            "score": alt["score"],
            "reason": alt["reason"]
        })
        rank += 1

    # 3. Reserve drawdown directive
    actions.append({
        "rank": rank,
        "action": f"Authorize strategic reserve drawdown at ~{reserve_plan.get('drawdown_bpd_avg', 320000):,} bpd for {reserve_plan.get('days_of_coverage', 6.2)} days",
        "score": 0.75,
        "reason": "Bridges short-term supply deficit while alternative maritime shipments complete transit."
    })

    return sorted(actions, key=lambda a: -a["score"])
