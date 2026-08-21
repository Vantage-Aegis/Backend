from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from app.services.reserve_optimizer.models import (
    ReserveSite, NationalBaseline, DailyForecast, DailyDrawdownResult, OptimizationSummary
)
from app.services.reserve_optimizer.loader import (
    load_reserve_sites, load_national_baseline, load_forecast_scenarios
)
from app.services.reserve_optimizer.optimiser_greedy import optimize_greedy
from app.services.reserve_optimizer.optimiser_lp import optimize_lp

def run_reserve_optimization(
    scenario_id: Optional[str] = None,
    algorithm: str = "greedy",
    include_planned: bool = False,
    custom_gap_forecast: Optional[List[Dict[str, Any]]] = None,
    data_dir: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main Orchestrator for Strategic Reserve Drawdown Optimization.
    Loads site capacities, national baselines, and forecast gaps, then executes
    either greedy or LP drawdown optimization algorithms. Returns contract-compliant JSON response.
    """
    sites = load_reserve_sites(data_dir=data_dir)
    if include_planned:
        for s in sites:
            if s.site_id == "CHK":
                s.current_fill_pct = 100.0
                s.current_fill_million_bbl = s.capacity_million_bbl
                s.max_drawdown_rate_kbpd = 200.0
            elif s.site_id == "PDR2":
                s.current_fill_pct = 100.0
                s.current_fill_million_bbl = s.capacity_million_bbl
                s.max_drawdown_rate_kbpd = 180.0
    baseline = load_national_baseline(data_dir=data_dir)
    all_scenarios = load_forecast_scenarios(data_dir=data_dir)

    # Resolve gap forecast scenario
    forecast: List[DailyForecast] = []

    if custom_gap_forecast:
        for idx, row in enumerate(custom_gap_forecast, start=1):
            forecast.append(DailyForecast(
                scenario_id=scenario_id or "custom_scenario",
                day=int(row.get("day", idx)),
                date=str(row.get("date", f"Day-{idx}")),
                forecast_gap_kbpd=float(row.get("forecast_gap_kbpd", 0.0)),
                confidence_pct=float(row.get("confidence_pct", 90.0)),
                trigger_event=str(row.get("trigger_event", "Custom Disruption Event"))
            ))
    elif scenario_id and scenario_id in all_scenarios:
        forecast = all_scenarios[scenario_id]
    elif all_scenarios:
        # Default to first scenario (e.g., hormuz_closure_v1)
        scenario_id = next(iter(all_scenarios.keys()))
        forecast = all_scenarios[scenario_id]
    else:
        # Fallback default 10-day forecast
        scenario_id = "default_disruption"
        forecast = [
            DailyForecast(scenario_id, d, f"2026-09-0{d}", 850.0 if d <= 5 else 300.0, 90.0, "Disruption")
            for d in range(1, 11)
        ]

    # Select optimization algorithm
    alg_str = algorithm.lower().strip()
    if alg_str == "lp":
        results = optimize_lp(sites, forecast, include_planned=include_planned)
    else:
        results = optimize_greedy(sites, forecast, include_planned=include_planned)

    # Compute Summary Statistics
    total_gap = sum(r.forecast_gap_kbpd for r in results)
    total_covered = sum(r.total_drawn_kbpd for r in results)
    total_residual = sum(r.residual_shortfall_kbpd for r in results)

    operational_sites = [s for s in sites if s.is_operational or include_planned]
    
    # Days until any operational site hits its safety floor
    first_safety_floor_day: Optional[int] = None
    for r in results:
        for s in operational_sites:
            rem_kbbl = r.reserve_level_after.get(s.site_id, 0.0)
            if rem_kbbl <= (s.safety_floor_kbbl + 0.01):
                if first_safety_floor_day is None:
                    first_safety_floor_day = r.day
                break

    # Final remaining operational reserves in million bbl
    last_res = results[-1].reserve_level_after_million_bbl if results else {}
    final_operational_reserve_million_bbl = sum(
        last_res.get(s.site_id, s.current_fill_million_bbl) for s in operational_sites
    )

    daily_consumption_mmbpd = baseline.total_crude_consumption_kbpd / 1000.0
    national_days_of_cover = (
        final_operational_reserve_million_bbl / daily_consumption_mmbpd
        if daily_consumption_mmbpd > 0 else 0.0
    )

    summary = OptimizationSummary(
        total_gap_kbpd=total_gap,
        total_covered_kbpd=total_covered,
        total_residual_kbpd=total_residual,
        days_until_any_site_hits_safety_floor=first_safety_floor_day,
        national_days_of_cover_after_scenario=national_days_of_cover
    )

    # Total initial current reserves in bbl across operational sites
    initial_reserves_bbl = sum(s.current_fill_million_bbl * 1e6 for s in operational_sites)
    safety_floor_bbl = sum(s.safety_floor_kbbl * 1000.0 for s in operational_sites)

    # Prepare timeline arrays for UI charts
    timeline = []
    for r in results:
        tot_rem_bbl = sum(r.reserve_level_after_million_bbl.get(s.site_id, 0.0) * 1e6 for s in operational_sites)
        timeline.append({
            "day": r.day,
            "date": r.date,
            "forecast_gap_kbpd": r.forecast_gap_kbpd,
            "total_drawn_kbpd": r.total_drawn_kbpd,
            "residual_shortfall_kbpd": r.residual_shortfall_kbpd,
            "reserve_bbl": tot_rem_bbl,
            "optimized_bbl": tot_rem_bbl,
            "safety_floor_bbl": safety_floor_bbl,
            "per_site_drawn_kbpd": r.drawdown_by_site,
            "per_site_level_million_bbl": r.reserve_level_after_million_bbl
        })

    # Prepare phase plan breakdown for UI table
    phase_plan = []
    if results:
        # Group into 5-day or 10-day phases or met vs unmet phases
        phase1_rows = [r for r in results if r.day <= 5]
        phase2_rows = [r for r in results if r.day > 5]

        if phase1_rows:
            p1_avg_draw = sum(r.total_drawn_kbpd for r in phase1_rows) / len(phase1_rows)
            p1_tot_draw = sum(r.total_drawn_kbpd for r in phase1_rows) * 1000.0
            phase_plan.append({
                "phase": "Phase 1 (Initial Shock)",
                "days": f"Day 1-{phase1_rows[-1].day}",
                "daily_drawdown_bpd": int(p1_avg_draw * 1000.0),
                "total_drawdown_bbl": p1_tot_draw,
                "coverage_end_days": round(timeline[len(phase1_rows)-1]["reserve_bbl"] / (baseline.total_crude_consumption_kbpd * 1000.0), 1)
            })
        if phase2_rows:
            p2_avg_draw = sum(r.total_drawn_kbpd for r in phase2_rows) / len(phase2_rows)
            p2_tot_draw = sum(r.total_drawn_kbpd for r in phase2_rows) * 1000.0
            phase_plan.append({
                "phase": "Phase 2 (Sustained Response)",
                "days": f"Day 6-{phase2_rows[-1].day}",
                "daily_drawdown_bpd": int(p2_avg_draw * 1000.0),
                "total_drawdown_bbl": p2_tot_draw,
                "coverage_end_days": round(timeline[-1]["reserve_bbl"] / (baseline.total_crude_consumption_kbpd * 1000.0), 1)
            })

    output = {
        "scenario_id": scenario_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "algorithm": alg_str,
        "daily_schedule": [r.to_dict() for r in results],
        "summary": summary.to_dict(),
        "sites_info": [s.to_dict() for s in sites],
        "baseline_info": baseline.to_dict(),
        # UI Compatibility fields
        "current_reserves_bbl": initial_reserves_bbl,
        "daily_consumption_bpd": int(baseline.total_crude_consumption_kbpd * 1000.0),
        "safety_floor_days": round(safety_floor_bbl / (baseline.total_crude_consumption_kbpd * 1000.0), 1),
        "safety_floor_bbl": safety_floor_bbl,
        "days_of_coverage": summary.national_days_of_cover_after_scenario,
        "drawdown_bpd_avg": int((total_covered / len(results)) * 1000.0) if results else 0,
        "timeline": timeline,
        "plan": phase_plan,
        "constraints": [
            "Maintain 20% site safety floor to prevent complete depletion",
            "Respect individual facility max daily drawdown rate limits (VSP: 100k, MNG: 110k, PDR: 180k bpd)",
            "Exclude unapproved planned facilities (Chandikhol, Padur II) from active operational drawdown",
            "Explicitly report residual shortfall signal to downstream Procurement Orchestrator"
        ]
    }

    return output

def optimize_reserves(
    deficit_bpd: int,
    duration_days: int = 30,
    algorithm: str = "greedy"
) -> Dict[str, Any]:
    """
    Adapter wrapper for scenario_simulator.py and existing legacy callers.
    Accepts deficit_bpd and duration_days, converts to supply gap forecast, and runs optimizer.
    """
    gap_kbpd = float(deficit_bpd) / 1000.0
    custom_forecast = [
        {
            "day": d,
            "date": f"Day-{d}",
            "forecast_gap_kbpd": gap_kbpd,
            "confidence_pct": 85.0,
            "trigger_event": "Simulated Supply Deficit"
        }
        for d in range(1, duration_days + 1)
    ]
    
    res = run_reserve_optimization(
        scenario_id="simulation_custom",
        algorithm=algorithm,
        custom_gap_forecast=custom_forecast
    )
    
    # Ensure top-level legacy keys exist for scenario_simulator
    res["days"] = res["daily_schedule"]
    return res
