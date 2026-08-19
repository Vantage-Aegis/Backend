from typing import Dict, Any, List

def optimize_reserves(deficit_bpd: int, duration_days: int = 30, baseline_reserve_bbl: int = 42000000, safety_floor_bbl: int = 8000000) -> Dict[str, Any]:
    """
    Simulates day-by-day strategic crude reserve drawdown schedule and coverage limit.
    Alternative supply ramps up over ramp_up_days (5 days).
    """
    current_reserve = baseline_reserve_bbl
    baseline_demand = 4700000
    baseline_incoming = max(0, baseline_demand - deficit_bpd)
    ramp_up_days = 5
    alt_max_supply = min(deficit_bpd, 1200000) if deficit_bpd > 0 else 0

    daily_rows = []
    coverage_days = 0.0
    floor_reached = False

    for day in range(1, duration_days + 1):
        # Alternative supply ramps in starting Day 2 (day - 1)
        ramp_factor = min(1.0, (day - 1) / ramp_up_days)
        incoming_alt_supply = int(alt_max_supply * ramp_factor)
        incoming_supply = baseline_incoming + incoming_alt_supply
        current_deficit = max(0, baseline_demand - incoming_supply)

        usable_reserve = max(0, current_reserve - safety_floor_bbl)
        draw_amount = min(current_deficit, usable_reserve)

        if current_reserve - draw_amount <= safety_floor_bbl and not floor_reached:
            floor_reached = True

        current_reserve -= draw_amount

        if current_deficit == 0 or draw_amount >= current_deficit:
            coverage_days += 1.0
        elif draw_amount > 0:
            coverage_days += draw_amount / current_deficit

        daily_rows.append({
            "day": day,
            "demand_bpd": baseline_demand,
            "incoming_supply_bpd": incoming_supply,
            "deficit_bpd": current_deficit,
            "reserve_draw_bpd": draw_amount,
            "remaining_reserve_bbl": current_reserve
        })

    avg_draw = int(sum(r["reserve_draw_bpd"] for r in daily_rows) / len(daily_rows)) if daily_rows else 0

    return {
        "days": daily_rows,
        "days_of_coverage": round(coverage_days, 1),
        "drawdown_bpd_avg": avg_draw,
        "safety_floor_bbl": safety_floor_bbl
    }
