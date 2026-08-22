from typing import List, Dict, Tuple, Any
from app.services.reserve_optimizer.models import ReserveSite, DailyForecast, DailyDrawdownResult

def optimize_greedy(
    sites: List[ReserveSite],
    forecast: List[DailyForecast],
    include_planned: bool = False
) -> List[DailyDrawdownResult]:
    """
    MVP Greedy Proportional Drawdown Algorithm.
    Proportionally allocates drawdown capacity across eligible operational sites.
    Strictly enforces per-site max daily drawdown rate limits and safety floors.
    """
    # Filter eligible sites
    eligible_sites = [s for s in sites if s.is_operational or include_planned]
    
    # Initialize working reserve levels in kbbl
    current_reserve_kbbl: Dict[str, float] = {
        s.site_id: s.current_fill_kbbl for s in sites
    }

    results: List[DailyDrawdownResult] = []

    for day_fc in forecast:
        gap = max(0.0, day_fc.forecast_gap_kbpd)

        # Calculate daily available drawdown capacity for each site
        daily_max_draw_kbpd: Dict[str, float] = {}
        for s in eligible_sites:
            s_id = s.site_id
            usable_reserve = max(0.0, current_reserve_kbbl[s_id] - s.safety_floor_kbbl)
            # Cannot draw more than daily rate limit or usable reserve
            daily_max_draw_kbpd[s_id] = min(s.max_drawdown_rate_kbpd, usable_reserve)

        total_avail_capacity = sum(daily_max_draw_kbpd.values())

        drawdown_by_site: Dict[str, float] = {}
        
        if gap == 0.0 or total_avail_capacity == 0.0:
            if gap == 0.0:
                for s in sites:
                    drawdown_by_site[s.site_id] = 0.0
                total_drawn = 0.0
                residual = 0.0
                status = "MET"
            else: # gap > 0 but total_avail_capacity == 0
                for s in sites:
                    drawdown_by_site[s.site_id] = 0.0
                total_drawn = 0.0
                residual = gap
                status = "UNMET"
        elif gap <= total_avail_capacity:
            total_drawn = gap
            residual = 0.0
            status = "MET"
            # Proportionally allocate gap based on site's available max draw capacity share
            for s in sites:
                if s.site_id in daily_max_draw_kbpd and total_avail_capacity > 0:
                    share = daily_max_draw_kbpd[s.site_id] / total_avail_capacity
                    drawdown_by_site[s.site_id] = round(gap * share, 3)
                else:
                    drawdown_by_site[s.site_id] = 0.0
        else: # gap > total_avail_capacity
            # Draw maximum allowed from every eligible site
            total_drawn = total_avail_capacity
            residual = gap - total_drawn
            status = "UNMET" if residual > 0.01 else "MET"
            for s in sites:
                if s.site_id in daily_max_draw_kbpd:
                    drawdown_by_site[s.site_id] = daily_max_draw_kbpd[s.site_id]
                else:
                    drawdown_by_site[s.site_id] = 0.0

        # Update current reserve levels for next day
        for s in sites:
            s_id = s.site_id
            drawn = drawdown_by_site.get(s_id, 0.0)
            current_reserve_kbbl[s_id] = max(0.0, current_reserve_kbbl[s_id] - drawn)

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
