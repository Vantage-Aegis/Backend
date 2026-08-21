import numpy as np
from typing import List, Dict, Any
from scipy.optimize import linprog
from app.services.reserve_optimizer.models import ReserveSite, DailyForecast, DailyDrawdownResult
from app.services.reserve_optimizer.optimiser_greedy import optimize_greedy

def optimize_lp(
    sites: List[ReserveSite],
    forecast: List[DailyForecast],
    include_planned: bool = False
) -> List[DailyDrawdownResult]:
    """
    Linear Programming (LP) Drawdown Optimizer.
    Solves a multi-period optimal resource allocation linear program using scipy.optimize.linprog.
    Objective:
      Minimize 10000 * sum(residual_shortfall[t]) + sum(site_weight[s] * x[s, t])
    Subject to:
      1. Daily drawdown rate limits: 0 <= x[s, t] <= max_drawdown_rate_kbpd[s]
      2. Site cumulative drawdown limit: sum_t x[s, t] <= initial_reserve[s] - safety_floor[s]
      3. Supply gap balance: sum_s x[s, t] + residual[t] >= forecast_gap_kbpd[t]
    """
    eligible_sites = [s for s in sites if s.is_operational or include_planned]
    M = len(eligible_sites)
    N = len(forecast)

    if M == 0 or N == 0:
        return optimize_greedy(sites, forecast, include_planned)

    # Variables index: x[s, t] for s in 0..M-1, t in 0..N-1 (total M*N)
    # followed by residual[t] for t in 0..N-1 (total N)
    num_vars = M * N + N

    def var_idx(s_idx: int, t_idx: int) -> int:
        return s_idx * N + t_idx

    def res_idx(t_idx: int) -> int:
        return M * N + t_idx

    # 1. Objective function vector c
    c = np.zeros(num_vars)
    UNMET_PENALTY = 10000.0

    for s_idx, s in enumerate(eligible_sites):
        usable = s.available_drawdown_capacity_kbbl
        # Slight tie-breaker weight favoring sites with larger usable reserves to balance depletion
        weight = 1.0 + (100.0 / (usable + 1.0))
        for t_idx in range(N):
            c[var_idx(s_idx, t_idx)] = weight

    for t_idx in range(N):
        c[res_idx(t_idx)] = UNMET_PENALTY

    # 2. Inequality constraints A_ub * x <= b_ub
    A_ub_list = []
    b_ub_list = []

    # Constraint A: Cumulative drawdown per site <= usable reserve
    for s_idx, s in enumerate(eligible_sites):
        row = np.zeros(num_vars)
        for t_idx in range(N):
            row[var_idx(s_idx, t_idx)] = 1.0
        A_ub_list.append(row)
        b_ub_list.append(s.available_drawdown_capacity_kbbl)

    # Constraint B: sum_s x[s, t] + residual[t] >= forecast_gap[t]
    # In form: - sum_s x[s, t] - residual[t] <= - forecast_gap[t]
    for t_idx, day_fc in enumerate(forecast):
        row = np.zeros(num_vars)
        for s_idx in range(M):
            row[var_idx(s_idx, t_idx)] = -1.0
        row[res_idx(t_idx)] = -1.0
        A_ub_list.append(row)
        b_ub_list.append(-max(0.0, day_fc.forecast_gap_kbpd))

    A_ub = np.array(A_ub_list)
    b_ub = np.array(b_ub_list)

    # 3. Variable bounds
    bounds = []
    for s_idx, s in enumerate(eligible_sites):
        max_rate = s.max_drawdown_rate_kbpd
        for t_idx in range(N):
            bounds.append((0.0, max_rate))
    for t_idx in range(N):
        bounds.append((0.0, None))

    # Solve LP
    try:
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
        if not res.success:
            return optimize_greedy(sites, forecast, include_planned)
        x_sol = res.x
    except Exception:
        return optimize_greedy(sites, forecast, include_planned)

    # Reconstruct step-by-step daily drawdown results
    current_reserve_kbbl: Dict[str, float] = {s.site_id: s.current_fill_kbbl for s in sites}
    results: List[DailyDrawdownResult] = []

    for t_idx, day_fc in enumerate(forecast):
        gap = max(0.0, day_fc.forecast_gap_kbpd)
        drawdown_by_site: Dict[str, float] = {}

        for s in sites:
            drawdown_by_site[s.site_id] = 0.0

        for s_idx, s in enumerate(eligible_sites):
            val = max(0.0, float(x_sol[var_idx(s_idx, t_idx)]))
            # Ensure we don't draw more than remaining usable reserve on this day
            usable = max(0.0, current_reserve_kbbl[s.site_id] - s.safety_floor_kbbl)
            val = min(val, usable)
            drawdown_by_site[s.site_id] = round(val, 3)

        total_drawn = sum(drawdown_by_site.values())
        residual = max(0.0, gap - total_drawn)
        status = "UNMET" if residual > 0.01 else "MET"

        # Update reserves
        for s in sites:
            s_id = s.site_id
            current_reserve_kbbl[s_id] = max(0.0, current_reserve_kbbl[s_id] - drawdown_by_site[s_id])

        results.append(DailyDrawdownResult(
            day=day_fc.day,
            date=day_fc.date,
            forecast_gap_kbpd=gap,
            drawdown_by_site=drawdown_by_site,
            total_drawn_kbpd=total_drawn,
            residual_shortfall_kbpd=residual,
            reserve_level_after=dict(current_reserve_kbbl),
            reserve_level_after_million_bbl={k: v / 1000.0 for k, v in current_reserve_kbbl.items()},
            status=status
        ))

    return results
