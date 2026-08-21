import os
import sys
import json
import math
import pandas as pd
import numpy as np
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path

# Set up paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = BASE_DIR / "Backend"
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"

# Load environment variables
load_dotenv(BACKEND_DIR / ".env")
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "energy_resilience_db")

print(f"Connecting to MongoDB: {DATABASE_NAME}")
client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]

# -------------------------------------------------------------
# 1. Load Datasets
# -------------------------------------------------------------
print("Loading raw files and data sources...")
with open(RAW_DIR / "supplier_countries.json", "r", encoding="utf-8") as f:
    raw_suppliers = json.load(f)

with open(RAW_DIR / "india_ports.json", "r", encoding="utf-8") as f:
    raw_india_ports = json.load(f)

with open(RAW_DIR / "supplier_ports.json", "r", encoding="utf-8") as f:
    raw_supplier_ports = json.load(f)

with open(RAW_DIR / "india_refineries.json", "r", encoding="utf-8") as f:
    raw_refineries = json.load(f)

with open(RAW_DIR / "chokepoints.json", "r", encoding="utf-8") as f:
    raw_chokepoints = json.load(f)

with open(RAW_DIR / "routes.json", "r", encoding="utf-8") as f:
    raw_routes = json.load(f)

df_import_share = pd.read_csv(DATA_DIR / "india_import_share_by_country.csv")
df_wgi = pd.read_csv(DATA_DIR / "wgi_scores_by_country_year.csv")
df_sanctions = pd.read_csv(DATA_DIR / "sanctions_by_country.csv")

# -------------------------------------------------------------
# 2. Helpers: IDs, Slugs, & Lookups
# -------------------------------------------------------------
def make_id(prefix: str, name: str) -> str:
    cleaned = name.lower()
    for char in ["(", ")", "/", ",", "-", "'", ".", "&"]:
        cleaned = cleaned.replace(char, " ")
    parts = [p.strip() for p in cleaned.split() if p.strip()]
    return f"{prefix}_{'_'.join(parts[:3])}"

# Specific stable ID maps for corridors
CORRIDOR_ID_MAP = {
    "Strait of Hormuz": "corr_hormuz",
    "Strait of Malacca": "corr_malacca",
    "Suez Canal": "corr_suez",
    "Bab el-Mandeb": "corr_babelmandeb",
    "Bab el-Mandeb Strait": "corr_babelmandeb",
    "Danish Straits": "corr_danish",
    "Turkish Straits": "corr_turkish",
    "Bosporus": "corr_bosporus",
    "Dardanelles": "corr_dardanelles",
    "Panama Canal": "corr_panama",
    "Gibraltar Strait": "corr_gibraltar",
    "English Channel / Dover Strait": "corr_dover",
    "Sunda Strait": "corr_sunda",
    "Lombok Strait": "corr_lombok",
    "Makassar Strait": "corr_makassar",
    "Cape of Good Hope": "corr_cape",
    "Cape Agulhas": "corr_cape_agulhas",
    "Kiel Canal": "corr_kiel",
    "Mozambique Channel": "corr_mozambique",
    "Taiwan Strait": "corr_taiwan",
    "Tsushima Strait": "corr_tsushima",
    "Korea Strait": "corr_korea",
    "Tsugaru Strait": "corr_tsugaru",
    "Bering Strait": "corr_bering",
    "Strait of Magellan": "corr_magellan",
    "Cape Horn": "corr_capehorn"
}

# Aliases for India import share lookup
COUNTRY_ALIASES = {
    "United States": "United States Of America",
    "Russia": "Russia",
    "Iran": "Iran",
    "Egypt": "Egypt",
    "Venezuela": "Venezuela",
    "Democratic Republic of the Congo": "Democratic Republic Of The Congo",
    "Republic of the Congo": "Republic Of The Congo",
    "Ivory Coast": "Cote D' Ivoire",
    "UAE": "United Arab Emirates"
}

# -------------------------------------------------------------
# 3. Process Indian Ports & Origin Ports
# -------------------------------------------------------------
ports_dict = {}
indian_ports_list = []
origin_ports_list = []

# Process Indian destination ports
for p in raw_india_ports:
    p_id = make_id("port", p["name"])
    # Standardize well-known ports
    if "mundra" in p["name"].lower():
        p_id = "port_mundra"
    elif "vadinar" in p["name"].lower() or "sikka" in p["name"].lower():
        p_id = "port_vadinar"
    elif "mumbai" in p["name"].lower() or "jnpt" in p["name"].lower():
        p_id = "port_jnpt"
    elif "kochi" in p["name"].lower() or "cochin" in p["name"].lower():
        p_id = "port_kochi"
    elif "mangalore" in p["name"].lower():
        p_id = "port_mangalore"
    elif "visakhapatnam" in p["name"].lower() or "vizag" in p["name"].lower():
        p_id = "port_vizag"
    elif "paradip" in p["name"].lower():
        p_id = "port_paradip"
    elif "ennore" in p["name"].lower() or "kamarajar" in p["name"].lower():
        p_id = "port_ennore"
    elif "chennai" in p["name"].lower():
        p_id = "port_chennai"
    elif "haldia" in p["name"].lower():
        p_id = "port_haldia"
    elif "kakinada" in p["name"].lower():
        p_id = "port_kakinada"
    elif "kandla" in p["name"].lower() or "deendayal" in p["name"].lower():
        p_id = "port_kandla"

    port_doc = {
        "_id": p_id,
        "name": p["name"],
        "country_iso": p.get("country_iso", "IND"),
        "type": "indian_port",
        "lat": round(float(p["latitude"]), 4),
        "lng": round(float(p["longitude"]), 4),
        "throughput_capacity_bpd": int(p.get("throughput_capacity_bpd", 1000000))
    }
    ports_dict[p["name"]] = port_doc
    ports_dict[p_id] = port_doc
    indian_ports_list.append(port_doc)

# Process Origin Export Ports (select primary ports per supplier)
for p in raw_supplier_ports:
    p_id = make_id("port", p["name"])
    port_doc = {
        "_id": p_id,
        "name": p["name"],
        "country_iso": p.get("country_iso", "UNK"),
        "type": "origin",
        "lat": round(float(p["latitude"]), 4),
        "lng": round(float(p["longitude"]), 4),
        "throughput_capacity_bpd": int(p.get("throughput_capacity_bpd", 500000))
    }
    ports_dict[p["name"]] = port_doc
    ports_dict[p_id] = port_doc
    origin_ports_list.append(port_doc)

all_ports = indian_ports_list + origin_ports_list
print(f"Total ports prepared: {len(all_ports)} ({len(indian_ports_list)} Indian, {len(origin_ports_list)} Origin)")

# -------------------------------------------------------------
# 4. Process Suppliers & Compute Reliability / Import Volumes
# -------------------------------------------------------------
TOTAL_INDIA_IMPORT_BPD = 4700000

# Representative coordinates for each supplier country
SUPPLIER_ORIGIN_COORDS = {
    "RUS": {"lat": 60.35, "lng": 28.67, "port": "Primorsk Oil Terminal"},
    "IRQ": {"lat": 29.68, "lng": 48.80, "port": "Basra Oil Terminal (ABOT)"},
    "SAU": {"lat": 26.64, "lng": 50.16, "port": "Ras Tanura Port"},
    "ARE": {"lat": 25.12, "lng": 56.33, "port": "Fujairah Oil Terminal"},
    "USA": {"lat": 29.73, "lng": -95.02, "port": "Houston Ship Channel"},
    "KWT": {"lat": 29.08, "lng": 48.14, "port": "Mina Al-Ahmadi Port"},
    "NGA": {"lat": 4.43, "lng": 7.17, "port": "Bonny Oil Terminal"},
    "AGO": {"lat": -8.80, "lng": 13.23, "port": "Luanda Port"},
    "BRA": {"lat": -23.96, "lng": -46.30, "port": "Santos Port"},
    "EGY": {"lat": 29.65, "lng": 32.34, "port": "Suez / Ain Sokhna Port"},
    "COL": {"lat": 9.40, "lng": -75.68, "port": "Coveñas Port"},
    "QAT": {"lat": 24.99, "lng": 51.55, "port": "Mesaieed Port"},
    "OMN": {"lat": 23.62, "lng": 58.56, "port": "Mina Al-Fahal Port"},
    "MEX": {"lat": 18.43, "lng": -93.20, "port": "Dos Bocas Port"},
    "VEN": {"lat": 10.22, "lng": -64.68, "port": "Jose Terminal"},
    "GUY": {"lat": 7.35, "lng": -57.45, "port": "Liza Destiny FPSO"},
    "KAZ": {"lat": 43.65, "lng": 51.16, "port": "Aktau Port"},
    "NOR": {"lat": 60.81, "lng": 5.03, "port": "Mongstad Oil Terminal"},
    "AZE": {"lat": 40.17, "lng": 49.44, "port": "Sangachal Terminal"},
    "DZA": {"lat": 35.85, "lng": -0.30, "port": "Arzew Port"},
    "LBY": {"lat": 30.65, "lng": 18.35, "port": "Es Sider Oil Terminal"},
    "ECU": {"lat": 0.97, "lng": -79.65, "port": "Esmeraldas Port"},
    "MYS": {"lat": 1.37, "lng": 104.12, "port": "Pengerang Integrated Petroleum Complex"},
    "IDN": {"lat": -6.10, "lng": 106.88, "port": "Tanjung Priok Port"},
    "CAN": {"lat": 49.29, "lng": -123.23, "port": "Vancouver Port (Westridge Marine Terminal)"}
}

suppliers_list = []
suppliers_dict = {}

# Compute route sum by supplier for fallback
route_sums = {}
for r in raw_routes:
    sup_name = r["from_supplier"]
    route_sums[sup_name] = route_sums.get(sup_name, 0) + r.get("current_flow_bpd", 0)

for s in raw_suppliers:
    name = s["name"]
    iso = s["country_iso"]
    s_id = make_id("sup", name)

    # 1. Fetch export to India from CSV
    alias = COUNTRY_ALIASES.get(name, name)
    c_matches = df_import_share[df_import_share["country"].str.lower() == alias.lower()]
    if c_matches.empty:
        c_matches = df_import_share[df_import_share["country"].str.contains(name, case=False, na=False)]

    if not c_matches.empty:
        # Get most recent non-zero import entry
        non_zero = c_matches[c_matches["quantity_000t"] > 0]
        if not non_zero.empty:
            latest_row = non_zero.iloc[-1]
            share_pct = float(latest_row["import_share_pct_qty"])
            # Scale to bpd
            computed_export_bpd = int(round((share_pct / 100.0) * TOTAL_INDIA_IMPORT_BPD))
        else:
            computed_export_bpd = route_sums.get(name, 25000)
    else:
        computed_export_bpd = route_sums.get(name, 25000)

    # Make sure it's at least the route sum
    if route_sums.get(name, 0) > 0:
        computed_export_bpd = route_sums[name]

    # 2. Extract WGI indicators
    wgi_matches = df_wgi[(df_wgi["country_code"] == iso) | (df_wgi["country_name"].str.contains(name, case=False, na=False))]
    if not wgi_matches.empty:
        latest_wgi = wgi_matches.iloc[-1]
        ps = float(latest_wgi.get("political_stability", 50.0))
        rl = float(latest_wgi.get("rule_of_law", 50.0))
        ge = float(latest_wgi.get("government_effectiveness", 50.0))
        cc = float(latest_wgi.get("control_of_corruption", 50.0))
        # Normalize from 0..100 or percentile scale
        ps_norm = (ps - 50.0) / 25.0
        rl_norm = (rl - 50.0) / 25.0
        ge_norm = (ge - 50.0) / 25.0
        cc_norm = (cc - 50.0) / 25.0
    else:
        ps_norm, rl_norm, ge_norm, cc_norm = 0.0, 0.0, 0.0, 0.0

    wgi_doc = {
        "political_stability": round(ps_norm, 2),
        "rule_of_law": round(rl_norm, 2),
        "control_of_corruption": round(cc_norm, 2),
        "government_effectiveness": round(ge_norm, 2)
    }

    # 3. Sanctions score
    ISO3_TO_ISO2 = {
        "RUS": "ru", "IRQ": "iq", "SAU": "sa", "ARE": "ae", "USA": "us",
        "KWT": "kw", "NGA": "ng", "AGO": "ao", "BRA": "br", "EGY": "eg",
        "COL": "co", "QAT": "qa", "OMN": "om", "MEX": "mx", "VEN": "ve",
        "GUY": "gy", "KAZ": "kz", "NOR": "no", "AZE": "az", "DZA": "dz",
        "LBY": "ly", "ECU": "ec", "MYS": "my", "IDN": "id", "CAN": "ca"
    }
    iso2 = ISO3_TO_ISO2.get(iso, iso[:2].lower())
    sanc_match = df_sanctions[df_sanctions["country"].str.lower() == iso2]
    sanc_count = int(sanc_match.iloc[0]["sanction_entity_count"]) if not sanc_match.empty else 0
    sanc_penalty = min(1.0, sanc_count / 1500.0) if sanc_count > 0 else (0.4 if iso in ["RUS", "VEN", "IRN"] else 0.0)

    # 4. Compute composite reliability score
    gov_index = ((ps_norm + 2.5) / 5.0 + (rl_norm + 2.5) / 5.0 + (ge_norm + 2.5) / 5.0 + (cc_norm + 2.5) / 5.0) / 4.0
    rel_score = 0.45 * gov_index + 0.30 * (1.0 - sanc_penalty) + 0.25 * 0.95
    rel_score = round(max(0.60, min(0.99, rel_score)), 2)

    # Specific overrides for well known sovereign profiles
    if iso == "USA": rel_score = 0.98
    elif iso == "ARE": rel_score = 0.95
    elif iso == "QAT": rel_score = 0.93
    elif iso == "KWT": rel_score = 0.91
    elif iso == "SAU": rel_score = 0.90
    elif iso == "NOR": rel_score = 0.98
    elif iso == "CAN": rel_score = 0.97
    elif iso == "RUS": rel_score = 0.85
    elif iso == "IRQ": rel_score = 0.82
    elif iso == "NGA": rel_score = 0.78
    elif iso == "AGO": rel_score = 0.80
    elif iso == "VEN": rel_score = 0.68

    coords = SUPPLIER_ORIGIN_COORDS.get(iso, {"lat": 20.0, "lng": 0.0, "port": "Origin Hub"})

    sup_doc = {
        "_id": s_id,
        "name": name,
        "country_iso": iso,
        "lat": coords["lat"],
        "lng": coords["lng"],
        "primary_terminal": coords.get("port"),
        "max_capacity_bpd": int(s.get("max_capacity_bpd", 2000000)),
        "current_export_bpd": computed_export_bpd,
        "current_total_export": int(s.get("current_total_export", computed_export_bpd * 3)),
        "base_price_usd_bbl": float(s.get("base_price_usd_bbl", 75.0)),
        "reliability_score": rel_score,
        "notes": f"Crude exporter via {coords.get('port')}",
        "wgi_indicators": wgi_doc
    }
    suppliers_list.append(sup_doc)
    suppliers_dict[name] = sup_doc
    suppliers_dict[s_id] = sup_doc

print(f"Total suppliers prepared: {len(suppliers_list)}")

# -------------------------------------------------------------
# 5. Process Corridors / Chokepoints
# -------------------------------------------------------------
# Baseline risk indices based on geopolitical chokepoint vulnerability
CORRIDOR_BASE_RISKS = {
    "Strait of Hormuz": 62.0,
    "Bab el-Mandeb": 54.0,
    "Bab el-Mandeb Strait": 54.0,
    "Suez Canal": 38.0,
    "Turkish Straits": 45.0,
    "Bosporus": 45.0,
    "Dardanelles": 42.0,
    "Strait of Malacca": 32.0,
    "Danish Straits": 28.0,
    "Gibraltar Strait": 22.0,
    "English Channel / Dover Strait": 20.0,
    "Panama Canal": 26.0,
    "Cape of Good Hope": 20.0,
    "Cape Agulhas": 20.0,
    "Mozambique Channel": 22.0,
    "Sunda Strait": 25.0,
    "Lombok Strait": 24.0,
    "Makassar Strait": 24.0,
    "Taiwan Strait": 48.0,
    "Korea Strait": 28.0,
    "Tsushima Strait": 28.0,
    "Bering Strait": 20.0,
    "Strait of Magellan": 22.0,
    "Cape Horn": 24.0
}

# Calculate corridor flows from routes
corridor_flows = {}
for r in raw_routes:
    flow = r.get("current_flow_bpd", 0)
    for c_name in r.get("corridors", []):
        corridor_flows[c_name] = corridor_flows.get(c_name, 0) + flow

corridors_list = []
corridors_dict = {}

for chk in raw_chokepoints:
    name = chk["name"]
    c_id = CORRIDOR_ID_MAP.get(name, make_id("corr", name))
    
    flow_bpd = corridor_flows.get(name, 0)
    # Check alternate naming
    if flow_bpd == 0:
        if "Bab el-Mandeb" in name: flow_bpd = corridor_flows.get("Bab el-Mandeb", 0) or corridor_flows.get("Bab el-Mandeb Strait", 0)
        elif "Cape" in name: flow_bpd = corridor_flows.get("Cape of Good Hope", 0)
        elif "Turkish" in name: flow_bpd = corridor_flows.get("Turkish Straits", 0)

    share_pct = round((flow_bpd / TOTAL_INDIA_IMPORT_BPD) * 100.0, 1)
    base_risk = CORRIDOR_BASE_RISKS.get(name, 25.0)

    corr_doc = {
        "_id": c_id,
        "name": name,
        "lat": round(float(chk["latitude"]), 4),
        "lng": round(float(chk["longitude"]), 4),
        "region": chk.get("region", "International Waters"),
        "daily_volume_bpd": flow_bpd,
        "share_of_india_imports_pct": share_pct,
        "base_risk": base_risk,
        "importance": chk.get("importance", "Strategic maritime corridor")
    }
    corridors_list.append(corr_doc)
    corridors_dict[name] = corr_doc
    corridors_dict[c_id] = corr_doc

print(f"Total corridors prepared: {len(corridors_list)}")

# -------------------------------------------------------------
# 6. Process Refineries
# -------------------------------------------------------------
refineries_list = []
for ref in raw_refineries:
    ref_id = make_id("ref", ref["name"])
    
    # Map connected ports to port IDs
    conn_port_ids = []
    for port_name in ref.get("connected_ports", []):
        if port_name in ports_dict:
            conn_port_ids.append(ports_dict[port_name]["_id"])
        else:
            # Match partial name
            matched = False
            for p in indian_ports_list:
                if any(part.lower() in p["name"].lower() for part in port_name.split() if len(part) > 3):
                    conn_port_ids.append(p["_id"])
                    matched = True
                    break
            if not matched:
                conn_port_ids.append("port_mundra")

    ref_doc = {
        "_id": ref_id,
        "name": ref["name"],
        "lat": round(float(ref["latitude"]), 4),
        "lng": round(float(ref["longitude"]), 4),
        "capacity_bpd": int(ref.get("capacity_bpd", 200000)),
        "connected_ports": list(set(conn_port_ids))
    }
    refineries_list.append(ref_doc)

print(f"Total refineries prepared: {len(refineries_list)}")

# -------------------------------------------------------------
# 7. Generate Sea Route Coordinates & Multi-Corridor Series Risk
# -------------------------------------------------------------
print("Calculating multi-corridor series risk, transit lead times, and waypoints for 45 routes...")

try:
    import searoute
    has_searoute = True
    print("searoute module loaded successfully.")
except ImportError:
    has_searoute = False
    print("searoute not available, using high-precision geodesic waypoint interpolation.")

def calculate_distance_km(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

routes_list = []

for idx, r in enumerate(raw_routes, start=1):
    r_id = f"route_{idx:03d}"
    sup_name = r["from_supplier"]
    port_name = r["to_port"]
    corridors_traversed = r.get("corridors", [])
    flow_bpd = r.get("current_flow_bpd", 100000)

    # Get supplier doc and Indian port doc
    sup_doc = suppliers_dict.get(sup_name)
    if not sup_doc:
        for s in suppliers_list:
            if s["name"].lower() == sup_name.lower():
                sup_doc = s
                break

    port_doc = ports_dict.get(port_name)
    if not port_doc:
        for p in indian_ports_list:
            if p["name"].lower() == port_name.lower():
                port_doc = p
                break

    from_node_id = sup_doc["_id"] if sup_doc else "sup_russia"
    to_node_id = port_doc["_id"] if port_doc else "port_mundra"

    from_lat, from_lng = sup_doc["lat"] if sup_doc else 60.35, sup_doc["lng"] if sup_doc else 28.67
    to_lat, to_lng = port_doc["lat"] if port_doc else 22.74, port_doc["lng"] if port_doc else 69.70

    # 1. Calculate Multi-Corridor Series Risk
    # Weakest-link series bottleneck formula: R_chokepoints = 100 * [1 - Prod(1 - Rc/100)]
    corridor_ids = []
    chokepoint_safe_prob = 1.0
    
    for c_name in corridors_traversed:
        c_id = CORRIDOR_ID_MAP.get(c_name)
        if c_id:
            corridor_ids.append(c_id)
        c_risk = CORRIDOR_BASE_RISKS.get(c_name, 25.0)
        chokepoint_safe_prob *= (1.0 - (c_risk / 100.0))

    if not corridors_traversed:
        compounded_chokepoint_risk = 15.0 # Direct / open ocean
    else:
        compounded_chokepoint_risk = 100.0 * (1.0 - chokepoint_safe_prob)

    # 2. Compute Sea Navigation Path & Distance
    waypoints = []
    dist_km = 0

    if has_searoute:
        try:
            # searoute takes [longitude, latitude]
            res = searoute.searoute([from_lng, from_lat], [to_lng, to_lat])
            raw_coords = res['geometry']['coordinates']
            # Convert to [lat, lng] for Leaflet
            waypoints = [[round(coord[1], 4), round(coord[0], 4)] for coord in raw_coords]
            dist_km = int(round(res['properties'].get('length', 0) * 1.852)) # nautical miles to km
        except Exception as ex:
            pass

    if not waypoints or dist_km == 0:
        # Geodesic calculation with corridor midpoints
        midpoints = []
        for c_name in corridors_traversed:
            c_doc = corridors_dict.get(c_name)
            if c_doc:
                midpoints.append([c_doc["lat"], c_doc["lng"]])
        
        all_pts = [[from_lat, from_lng]] + midpoints + [[to_lat, to_lng]]
        waypoints = all_pts
        dist_km = int(round(calculate_distance_km(from_lat, from_lng, to_lat, to_lng) * 1.45))

    # Lead time at 13.5 knots (~600 km/day)
    lead_time_days = max(2, int(round(dist_km / 600.0)))
    # Transport cost $/bbl based on distance and canal tolls
    toll_fee = 0.80 if ("Suez Canal" in corridors_traversed or "Panama Canal" in corridors_traversed) else 0.0
    transport_cost = round(1.20 + (dist_km / 1000.0) * 0.40 + toll_fee, 2)

    # Composite route base risk
    supplier_rel = sup_doc["reliability_score"] if sup_doc else 0.90
    dist_risk = min(100.0, (lead_time_days / 35.0) * 100.0)
    
    route_risk = (
        0.65 * compounded_chokepoint_risk +
        0.20 * ((1.0 - supplier_rel) * 100.0) +
        0.15 * dist_risk
    )
    route_risk = round(max(15.0, min(95.0, route_risk)), 1)

    corridor_display = " + ".join(corridors_traversed) if corridors_traversed else "Direct / Arabian Sea"
    primary_corr_id = corridor_ids[0] if corridor_ids else None

    route_doc = {
        "_id": r_id,
        "from_node": from_node_id,
        "to_node": to_node_id,
        "corridor": corridor_display,
        "corridor_id": primary_corr_id,
        "corridors": corridor_ids,
        "capacity_bpd": int(flow_bpd * 1.3),
        "current_flow_bpd": flow_bpd,
        "distance_km": dist_km,
        "lead_time_days": lead_time_days,
        "transport_cost_usd_bbl": transport_cost,
        "risk_base": route_risk,
        "status": "active",
        "waypoints": waypoints
    }
    routes_list.append(route_doc)

print(f"Total routes generated: {len(routes_list)}")

# -------------------------------------------------------------
# 8. Scenario Templates
# -------------------------------------------------------------
scenario_templates = [
    {
        "_id": "hormuz_closure",
        "label": "Strait of Hormuz Blockade (Severe)",
        "event_type": "hormuz_closure",
        "default_severity": 5,
        "default_duration_days": 30,
        "affected_corridor_id": "corr_hormuz",
        "description": "Complete naval blockade of Strait of Hormuz disrupting Gulf crude exports to western Indian ports."
    },
    {
        "_id": "redsea_disruption",
        "label": "Red Sea / Bab-el-Mandeb Shipping Suspension",
        "event_type": "redsea_disruption",
        "default_severity": 4,
        "default_duration_days": 45,
        "affected_corridor_id": "corr_babelmandeb",
        "description": "Commercial missile & drone threats forcing European and Russian crude to reroute around Cape of Good Hope."
    },
    {
        "_id": "malacca_blockade",
        "label": "Strait of Malacca Chokepoint Blockade",
        "event_type": "corridor_disruption",
        "default_severity": 4,
        "default_duration_days": 30,
        "affected_corridor_id": "corr_malacca",
        "description": "Maritime blockade or dispute halting crude & condensate shipments from Far East and Pacific terminals."
    },
    {
        "_id": "suez_redsea_dual",
        "label": "Dual Chokepoint Crisis (Suez + Bab-el-Mandeb)",
        "event_type": "dual_corridor_disruption",
        "default_severity": 5,
        "default_duration_days": 40,
        "affected_corridor_id": "corr_suez",
        "description": "Simultaneous blockage of Suez Canal and Bab-el-Mandeb cutting Mediterranean and Russian crude flows."
    },
    {
        "_id": "saudi_terminal_outage",
        "label": "Ras Tanura Export Terminal Outage",
        "event_type": "supplier_disruption",
        "default_severity": 4,
        "default_duration_days": 21,
        "affected_supplier_id": "sup_saudi_arabia",
        "description": "Major infrastructure damage at Ras Tanura port curtailing Saudi Aramco crude exports by 75%."
    },
    {
        "_id": "mundra_port_cyclone",
        "label": "Mundra Port Terminal Cyclone Damage",
        "event_type": "port_disruption",
        "default_severity": 4,
        "default_duration_days": 14,
        "affected_port_id": "port_mundra",
        "description": "Severe Arabian Sea cyclone damage to single-point mooring berths at Mundra offloading hub."
    }
]

# -------------------------------------------------------------
# 9. Geopolitical Risk Events
# -------------------------------------------------------------
risk_events = [
    {
        "_id": "evt_001",
        "title": "Renewed sanctions on Persian Gulf crude tankers",
        "corridor": "Strait of Hormuz",
        "corridor_id": "corr_hormuz",
        "severity": 65,
        "source": "manual",
        "category": "sanctions",
        "description": "Tightened secondary sanctions and naval interdictions in Gulf waters."
    },
    {
        "_id": "evt_002",
        "title": "Drone attack near Bab-el-Mandeb shipping lanes",
        "corridor": "Bab el-Mandeb Strait",
        "corridor_id": "corr_babelmandeb",
        "severity": 75,
        "source": "manual",
        "category": "shipping_attack",
        "description": "VLCC tankers rerouting around Cape of Good Hope due to safety threats."
    },
    {
        "_id": "evt_003",
        "title": "Naval exercise near Singapore and Malacca Straits",
        "corridor": "Strait of Malacca",
        "corridor_id": "corr_malacca",
        "severity": 45,
        "source": "manual",
        "category": "conflict",
        "description": "Military maneuvers causing vessel congestion and 2-day queue delays."
    },
    {
        "_id": "evt_004",
        "title": "Suez Canal northbound tanker queue congestion",
        "corridor": "Suez Canal",
        "corridor_id": "corr_suez",
        "severity": 40,
        "source": "manual",
        "category": "other",
        "description": "Scheduled dredging operations reducing daily convoy transit slots."
    },
    {
        "_id": "evt_005",
        "title": "Diplomatic standoff and naval patrols in Gulf of Oman",
        "corridor": "Strait of Hormuz",
        "corridor_id": "corr_hormuz",
        "severity": 60,
        "source": "manual",
        "category": "diplomatic",
        "description": "Elevated war-risk insurance premiums for commercial crude carriers."
    }
]

# -------------------------------------------------------------
# 10. Country Profile (India Baseline)
# -------------------------------------------------------------
countries = [
    {
        "_id": "IND",
        "name": "India",
        "iso_code": "IND",
        "is_import_dependent": True,
        "daily_consumption_bpd": 5340000,
        "total_daily_import_bpd": TOTAL_INDIA_IMPORT_BPD,
        "strategic_reserve_bbl": 42000000,
        "reserve_safety_floor_bbl": 8000000,
        "reserve_days": 9.5
    }
]

# -------------------------------------------------------------
# 11. Write to MongoDB Atlas & Update Backend seed.py
# -------------------------------------------------------------
collections_payload = {
    "suppliers": suppliers_list,
    "ports": all_ports,
    "refineries": refineries_list,
    "corridors": corridors_list,
    "routes": routes_list,
    "scenario_templates": scenario_templates,
    "risk_events": risk_events,
    "countries": countries,
    "risk_scores": []
}

print("\n--- Seeding MongoDB Collections ---")
for coll_name, docs in collections_payload.items():
    coll = db[coll_name]
    coll.delete_many({})
    if docs:
        coll.insert_many(docs)
        print(f"Collection '{coll_name}': successfully seeded {len(docs)} documents.")
    else:
        print(f"Collection '{coll_name}': cleared (0 documents).")

# Save as updated seed.py for standalone execution
seed_py_content = f'''import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable not set")
DATABASE_NAME = os.getenv("DATABASE_NAME", "energy_resilience_db")

def seed_database():
    print(f"Connecting to MongoDB Atlas Cluster: {{MONGODB_URI}}")
    client = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]

    suppliers = {json.dumps(suppliers_list, indent=8)}
    ports = {json.dumps(all_ports, indent=8)}
    refineries = {json.dumps(refineries_list, indent=8)}
    corridors = {json.dumps(corridors_list, indent=8)}
    routes = {json.dumps(routes_list, indent=8)}
    scenario_templates = {json.dumps(scenario_templates, indent=8)}
    risk_events = {json.dumps(risk_events, indent=8)}
    countries = {json.dumps(countries, indent=8)}

    collections = {{
        "suppliers": suppliers,
        "ports": ports,
        "refineries": refineries,
        "corridors": corridors,
        "routes": routes,
        "scenario_templates": scenario_templates,
        "risk_events": risk_events,
        "countries": countries,
        "risk_scores": []
    }}

    for name, docs in collections.items():
        coll = db[name]
        coll.delete_many({{}})
        if docs:
            coll.insert_many(docs)
            print(f"Collection '{{name}}': seeded {{len(docs)}} documents into '{{DATABASE_NAME}}'.")
        else:
            print(f"Collection '{{name}}': cleared.")

    print("\\nDatabase seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
'''

with open(BACKEND_DIR / "scripts" / "seed.py", "w", encoding="utf-8") as f:
    f.write(seed_py_content)

print(f"\nUpdated {BACKEND_DIR / 'scripts' / 'seed.py'} successfully.")
print("\nAll database generation and seeding tasks completed!")
