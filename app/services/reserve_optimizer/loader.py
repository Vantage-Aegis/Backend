import csv
import os
import pandas as pd
from typing import List, Dict, Any, Optional
from app.services.reserve_optimizer.models import ReserveSite, NationalBaseline, DailyForecast

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "reserve_optimizer"))

def load_reserve_sites(data_dir: Optional[str] = None) -> List[ReserveSite]:
    path = os.path.join(data_dir or DATA_DIR, "reserve_sites.csv")
    if not os.path.exists(path):
        # Fallback path if needed
        path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "md_files", "reserve-optimizer", "reserve_sites.csv")

    sites: List[ReserveSite] = []
    if os.path.exists(path):
        df = pd.read_csv(path)
        for _, row in df.iterrows():
            sites.append(ReserveSite(
                site_id=str(row["site_id"]).strip(),
                site_name=str(row["site_name"]).strip(),
                state=str(row["state"]).strip(),
                status=str(row["status"]).strip(),
                capacity_mmt=float(row["capacity_mmt"]),
                capacity_million_bbl=float(row["capacity_million_bbl"]),
                current_fill_pct=float(row["current_fill_pct"]),
                current_fill_million_bbl=float(row["current_fill_million_bbl"]),
                safety_floor_pct=float(row["safety_floor_pct"]),
                max_drawdown_rate_kbpd=float(row["max_drawdown_rate_kbpd"]),
                data_type=str(row["data_type"]).strip(),
                source_or_basis=str(row["source_or_basis"]).strip()
            ))
    else:
        # Default fallback inline if file missing
        sites = [
            ReserveSite("VSP", "Visakhapatnam", "Andhra Pradesh", "operational", 1.33, 9.75, 64.0, 6.24, 20.0, 100.0, "ASSUMPTION", "ISPRL/PIB"),
            ReserveSite("MNG", "Mangalore", "Karnataka", "operational", 1.5, 11.0, 64.0, 7.04, 20.0, 110.0, "ASSUMPTION", "ISPRL/PIB"),
            ReserveSite("PDR", "Padur", "Karnataka", "operational", 2.5, 18.32, 64.0, 11.72, 20.0, 180.0, "ASSUMPTION", "ISPRL/PIB"),
            ReserveSite("CHK", "Chandikhol", "Odisha", "planned_not_operational", 4.0, 29.32, 0.0, 0.0, 20.0, 0.0, "REAL", "PIB Approved"),
            ReserveSite("PDR2", "Padur Phase-II", "Karnataka", "planned_not_operational", 2.5, 18.32, 0.0, 0.0, 20.0, 0.0, "REAL", "PIB Approved")
        ]
    return sites

def load_national_baseline(data_dir: Optional[str] = None) -> NationalBaseline:
    path = os.path.join(data_dir or DATA_DIR, "national_supply_baseline.csv")
    if not os.path.exists(path):
        path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "md_files", "reserve-optimizer", "national_supply_baseline.csv")

    metrics: Dict[str, Dict[str, Any]] = {}
    if os.path.exists(path):
        df = pd.read_csv(path)
        for _, row in df.iterrows():
            metric_key = str(row["metric"]).strip()
            val_raw = row["value"]
            try:
                val = float(val_raw)
            except (ValueError, TypeError):
                val = val_raw
            metrics[metric_key] = {
                "value": val,
                "unit": str(row["unit"]).strip(),
                "data_type": str(row["data_type"]).strip(),
                "as_of": str(row["as_of"]).strip(),
                "source_or_basis": str(row["source_or_basis"]).strip()
            }
    return NationalBaseline(metrics=metrics)

def load_forecast_scenarios(data_dir: Optional[str] = None) -> Dict[str, List[DailyForecast]]:
    path = os.path.join(data_dir or DATA_DIR, "supply_gap_forecast_sample.csv")
    if not os.path.exists(path):
        path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "md_files", "reserve-optimizer", "supply_gap_forecast_sample.csv")

    scenarios: Dict[str, List[DailyForecast]] = {}
    if os.path.exists(path):
        df = pd.read_csv(path)
        for _, row in df.iterrows():
            scen_id = str(row["scenario_id"]).strip()
            if scen_id not in scenarios:
                scenarios[scen_id] = []
            scenarios[scen_id].append(DailyForecast(
                scenario_id=scen_id,
                day=int(row["day"]),
                date=str(row["date"]).strip(),
                forecast_gap_kbpd=float(row["forecast_gap_kbpd"]),
                confidence_pct=float(row["confidence_pct"]),
                trigger_event=str(row["trigger_event"]).strip()
            ))
    return scenarios
