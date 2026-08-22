import pytest
from app.services.reserve_optimizer.loader import (
    load_reserve_sites, load_national_baseline, load_forecast_scenarios
)
from app.services.reserve_optimizer.optimiser_greedy import optimize_greedy
from app.services.reserve_optimizer.optimiser_lp import optimize_lp
from app.services.reserve_optimizer.schedule import run_reserve_optimization, optimize_reserves

def test_load_data():
    sites = load_reserve_sites()
    baseline = load_national_baseline()
    scenarios = load_forecast_scenarios()

    assert len(sites) >= 5
    assert baseline.total_crude_consumption_kbpd == 5600.0
    assert "hormuz_closure_v1" in scenarios
    assert "red_sea_disruption_v1" in scenarios

def test_greedy_safety_floor_and_rate_limits():
    sites = load_reserve_sites()
    scenarios = load_forecast_scenarios()
    forecast = scenarios["hormuz_closure_v1"]

    results = optimize_greedy(sites, forecast, include_planned=False)

    operational_sites = {s.site_id: s for s in sites if s.is_operational}

    for r in results:
        # Check rate limits
        for site_id, drawn in r.drawdown_by_site.items():
            if site_id in operational_sites:
                max_rate = operational_sites[site_id].max_drawdown_rate_kbpd
                assert drawn <= max_rate + 1e-3, f"Site {site_id} exceeded max rate {max_rate}: drawn {drawn}"
            else:
                assert drawn == 0.0, f"Planned site {site_id} was drawn from!"

        # Check safety floors
        for site_id, s in operational_sites.items():
            level_kbbl = r.reserve_level_after[site_id]
            assert level_kbbl >= s.safety_floor_kbbl - 1e-3, f"Site {site_id} fell below safety floor!"

        # Check math consistency
        assert abs(r.total_drawn_kbpd + r.residual_shortfall_kbpd - r.forecast_gap_kbpd) < 1e-2

def test_lp_safety_floor_and_rate_limits():
    sites = load_reserve_sites()
    scenarios = load_forecast_scenarios()
    forecast = scenarios["hormuz_closure_v1"]

    results = optimize_lp(sites, forecast, include_planned=False)

    operational_sites = {s.site_id: s for s in sites if s.is_operational}

    for r in results:
        for site_id, drawn in r.drawdown_by_site.items():
            if site_id in operational_sites:
                max_rate = operational_sites[site_id].max_drawdown_rate_kbpd
                assert drawn <= max_rate + 1e-3, f"LP: Site {site_id} exceeded max rate {max_rate}: drawn {drawn}"
            else:
                assert drawn == 0.0, f"LP: Planned site {site_id} was drawn from!"

        for site_id, s in operational_sites.items():
            level_kbbl = r.reserve_level_after[site_id]
            assert level_kbbl >= s.safety_floor_kbbl - 1e-3, f"LP: Site {site_id} fell below safety floor!"

        assert abs(r.total_drawn_kbpd + r.residual_shortfall_kbpd - r.forecast_gap_kbpd) < 1e-2

def test_extreme_gap_residual_shortfall():
    """When forecast gap exceeds system capacity (e.g. 5000 kbpd), residual shortfall must be recorded explicitly."""
    res = run_reserve_optimization(
        scenario_id="extreme_test",
        algorithm="greedy",
        custom_gap_forecast=[
            {"day": 1, "forecast_gap_kbpd": 5000.0, "date": "2026-09-01"}
        ]
    )

    day1 = res["daily_schedule"][0]
    assert day1["status"] == "UNMET"
    assert day1["total_drawn_kbpd"] == 390.0  # VSP(100) + MNG(110) + PDR(180)
    assert day1["residual_shortfall_kbpd"] == 4610.0

def test_zero_gap_day():
    res = run_reserve_optimization(
        scenario_id="zero_gap_test",
        algorithm="greedy",
        custom_gap_forecast=[
            {"day": 1, "forecast_gap_kbpd": 0.0, "date": "2026-09-01"}
        ]
    )

    day1 = res["daily_schedule"][0]
    assert day1["status"] == "MET"
    assert day1["total_drawn_kbpd"] == 0.0
    assert day1["residual_shortfall_kbpd"] == 0.0

def test_adapter_optimize_reserves():
    res = optimize_reserves(deficit_bpd=1974000, duration_days=10)
    assert "days" in res
    assert "days_of_coverage" in res
    assert "safety_floor_bbl" in res
    assert len(res["daily_schedule"]) == 10
