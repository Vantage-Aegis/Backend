import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

# Ensure app modules can be imported if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable not set")
DATABASE_NAME = os.getenv("DATABASE_NAME", "energy_resilience_db")

def seed_database():
    print(f"Connecting to MongoDB Atlas Cluster: {MONGODB_URI}")
    client = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]

    # Data payload definitions
    suppliers = [
        {
            "_id": "sup_saudi",
            "name": "Saudi Arabia",
            "country_iso": "SAU",
            "lat": 24.0,
            "lng": 45.0,
            "max_capacity_bpd": 1200000,
            "current_export_bpd": 950000,
            "base_price_usd_bbl": 82.5,
            "reliability_score": 0.9,
            "notes": "Primary supplier transiting Strait of Hormuz"
        },
        {
            "_id": "sup_iraq",
            "name": "Iraq",
            "country_iso": "IRQ",
            "lat": 33.3,
            "lng": 44.3,
            "max_capacity_bpd": 1100000,
            "current_export_bpd": 880000,
            "base_price_usd_bbl": 79.0,
            "reliability_score": 0.82,
            "notes": "Basra export terminals via Hormuz"
        },
        {
            "_id": "sup_uae",
            "name": "UAE",
            "country_iso": "ARE",
            "lat": 23.4,
            "lng": 53.8,
            "max_capacity_bpd": 1000000,
            "current_export_bpd": 750000,
            "base_price_usd_bbl": 83.0,
            "reliability_score": 0.95,
            "notes": "Has bypass pipeline to Fujairah port outside Hormuz"
        },
        {
            "_id": "sup_usa",
            "name": "USA (WTI crude)",
            "country_iso": "USA",
            "lat": 29.7,
            "lng": -95.3,
            "max_capacity_bpd": 600000,
            "current_export_bpd": 350000,
            "base_price_usd_bbl": 78.5,
            "reliability_score": 0.98,
            "notes": "Atlantic long-haul supply route"
        },
        {
            "_id": "sup_russia",
            "name": "Russia (Urals)",
            "country_iso": "RUS",
            "lat": 61.5,
            "lng": 105.3,
            "max_capacity_bpd": 1400000,
            "current_export_bpd": 1100000,
            "base_price_usd_bbl": 71.0,
            "reliability_score": 0.85,
            "notes": "Discounted crude via Red Sea / Suez or Cape route"
        },
        {
            "_id": "sup_nigeria",
            "name": "Nigeria (Bonny Light)",
            "country_iso": "NGA",
            "lat": 9.08,
            "lng": 7.5,
            "max_capacity_bpd": 500000,
            "current_export_bpd": 300000,
            "base_price_usd_bbl": 85.0,
            "reliability_score": 0.78,
            "notes": "West African sweet crude transiting Cape route"
        },
        {
            "_id": "sup_kuwait",
            "name": "Kuwait",
            "country_iso": "KWT",
            "lat": 29.3,
            "lng": 47.4,
            "max_capacity_bpd": 700000,
            "current_export_bpd": 520000,
            "base_price_usd_bbl": 81.0,
            "reliability_score": 0.91,
            "notes": "Persian Gulf origin transiting Hormuz"
        },
        {
            "_id": "sup_qatar",
            "name": "Qatar",
            "country_iso": "QAT",
            "lat": 25.3,
            "lng": 51.1,
            "max_capacity_bpd": 450000,
            "current_export_bpd": 300000,
            "base_price_usd_bbl": 82.0,
            "reliability_score": 0.93,
            "notes": "Condensate & light crude transiting Hormuz"
        }
    ]

    ports = [
        {
            "_id": "port_ras_tanura",
            "name": "Ras Tanura Terminal",
            "country_iso": "SAU",
            "type": "origin",
            "lat": 26.64,
            "lng": 50.16,
            "throughput_capacity_bpd": 3000000
        },
        {
            "_id": "port_fujairah",
            "name": "Fujairah Oil Hub",
            "country_iso": "ARE",
            "type": "origin",
            "lat": 25.18,
            "lng": 56.36,
            "throughput_capacity_bpd": 2000000
        },
        {
            "_id": "port_jnpt",
            "name": "JNPT, Mumbai",
            "country_iso": "IND",
            "type": "indian_port",
            "lat": 18.95,
            "lng": 72.95,
            "throughput_capacity_bpd": 1500000
        },
        {
            "_id": "port_kandla",
            "name": "Deendayal / Kandla Port",
            "country_iso": "IND",
            "type": "indian_port",
            "lat": 23.01,
            "lng": 70.22,
            "throughput_capacity_bpd": 1800000
        },
        {
            "_id": "port_paradip",
            "name": "Paradip Port",
            "country_iso": "IND",
            "type": "indian_port",
            "lat": 20.26,
            "lng": 86.67,
            "throughput_capacity_bpd": 1400000
        }
    ]

    refineries = [
        {
            "_id": "ref_jamnagar",
            "name": "Jamnagar Refinery (RIL)",
            "lat": 22.47,
            "lng": 69.85,
            "capacity_bpd": 1400000,
            "connected_ports": ["port_kandla", "port_jnpt"]
        },
        {
            "_id": "ref_vadinar",
            "name": "Vadinar Refinery (Nayara)",
            "lat": 22.40,
            "lng": 69.71,
            "capacity_bpd": 400000,
            "connected_ports": ["port_kandla"]
        },
        {
            "_id": "ref_mangalore",
            "name": "Mangalore Refinery (MRPL)",
            "lat": 13.0,
            "lng": 74.8,
            "capacity_bpd": 300000,
            "connected_ports": ["port_jnpt"]
        },
        {
            "_id": "ref_paradip",
            "name": "Paradip Refinery (IOCL)",
            "lat": 20.28,
            "lng": 86.63,
            "capacity_bpd": 300000,
            "connected_ports": ["port_paradip"]
        }
    ]

    corridors = [
        {
            "_id": "corr_hormuz",
            "name": "Strait of Hormuz",
            "lat": 26.56,
            "lng": 56.25,
            "daily_volume_bpd": 2000000,
            "share_of_india_imports_pct": 42.0,
            "base_risk": 61.0
        },
        {
            "_id": "corr_redsea",
            "name": "Red Sea / Bab-el-Mandeb",
            "lat": 12.58,
            "lng": 43.33,
            "daily_volume_bpd": 1100000,
            "share_of_india_imports_pct": 23.0,
            "base_risk": 48.0
        },
        {
            "_id": "corr_cape",
            "name": "Cape of Good Hope Route",
            "lat": -34.83,
            "lng": 20.00,
            "daily_volume_bpd": 600000,
            "share_of_india_imports_pct": 12.0,
            "base_risk": 20.0
        }
    ]

    routes = [
        {
            "_id": "route_001",
            "from_node": "sup_saudi",
            "to_node": "port_jnpt",
            "corridor": "Strait of Hormuz",
            "corridor_id": "corr_hormuz",
            "capacity_bpd": 900000,
            "current_flow_bpd": 850000,
            "distance_km": 3800,
            "lead_time_days": 9,
            "transport_cost_usd_bbl": 2.5,
            "risk_base": 61,
            "status": "active",
            "waypoints": [[24.5, 57.5], [20.5, 65.5]]
        },
        {
            "_id": "route_002",
            "from_node": "sup_iraq",
            "to_node": "port_kandla",
            "corridor": "Strait of Hormuz",
            "corridor_id": "corr_hormuz",
            "capacity_bpd": 850000,
            "current_flow_bpd": 800000,
            "distance_km": 4100,
            "lead_time_days": 10,
            "transport_cost_usd_bbl": 2.7,
            "risk_base": 63,
            "status": "active",
            "waypoints": [[26.0, 55.0], [24.0, 60.0], [22.0, 65.0]]
        },
        {
            "_id": "route_003",
            "from_node": "sup_uae",
            "to_node": "port_jnpt",
            "corridor": "Strait of Hormuz",
            "corridor_id": "corr_hormuz",
            "capacity_bpd": 400000,
            "current_flow_bpd": 350000,
            "distance_km": 3600,
            "lead_time_days": 8,
            "transport_cost_usd_bbl": 2.3,
            "risk_base": 58,
            "status": "active",
            "waypoints": [[24.5, 58.0], [21.0, 66.0]]
        },
        {
            "_id": "route_004",
            "from_node": "sup_kuwait",
            "to_node": "port_kandla",
            "corridor": "Strait of Hormuz",
            "corridor_id": "corr_hormuz",
            "capacity_bpd": 500000,
            "current_flow_bpd": 480000,
            "distance_km": 3950,
            "lead_time_days": 9,
            "transport_cost_usd_bbl": 2.6,
            "risk_base": 60,
            "status": "active",
            "waypoints": [[28.0, 50.0], [26.0, 55.0], [23.5, 63.0]]
        },
        {
            "_id": "route_005",
            "from_node": "sup_russia",
            "to_node": "port_paradip",
            "corridor": "Red Sea / Bab-el-Mandeb",
            "corridor_id": "corr_redsea",
            "capacity_bpd": 900000,
            "current_flow_bpd": 850000,
            "distance_km": 8200,
            "lead_time_days": 18,
            "transport_cost_usd_bbl": 4.8,
            "risk_base": 48,
            "status": "active",
            "waypoints": [[35.0, 25.0], [27.0, 34.0], [13.0, 43.0], [10.0, 55.0], [5.0, 78.0], [10.0, 83.0]]
        },
        {
            "_id": "route_006",
            "from_node": "sup_russia",
            "to_node": "port_kandla",
            "corridor": "Red Sea / Bab-el-Mandeb",
            "corridor_id": "corr_redsea",
            "capacity_bpd": 600000,
            "current_flow_bpd": 250000,
            "distance_km": 14500,
            "lead_time_days": 32,
            "transport_cost_usd_bbl": 7.2,
            "risk_base": 22,
            "status": "active",
            "waypoints": [[35.0, 25.0], [27.0, 34.0], [13.0, 43.0], [15.0, 55.0], [20.0, 65.0]]
        },
        {
            "_id": "route_007",
            "from_node": "sup_nigeria",
            "to_node": "port_jnpt",
            "corridor": "Cape of Good Hope Route",
            "corridor_id": "corr_cape",
            "capacity_bpd": 400000,
            "current_flow_bpd": 300000,
            "distance_km": 11200,
            "lead_time_days": 24,
            "transport_cost_usd_bbl": 5.9,
            "risk_base": 20,
            "status": "active",
            "waypoints": [[0.0, 0.0], [-35.0, 20.0], [-10.0, 60.0], [10.0, 70.0]]
        },
        {
            "_id": "route_008",
            "from_node": "sup_usa",
            "to_node": "port_paradip",
            "corridor": "Cape of Good Hope Route",
            "corridor_id": "corr_cape",
            "capacity_bpd": 500000,
            "current_flow_bpd": 350000,
            "distance_km": 16800,
            "lead_time_days": 35,
            "transport_cost_usd_bbl": 8.1,
            "risk_base": 18,
            "status": "active",
            "waypoints": [[20.0, -60.0], [0.0, -30.0], [-35.0, 20.0], [-10.0, 70.0], [10.0, 85.0]]
        },
        {
            "_id": "route_009",
            "from_node": "sup_uae",
            "to_node": "port_kandla",
            "corridor": "Bypass Fujairah (Non-Hormuz)",
            "corridor_id": None,
            "capacity_bpd": 400000,
            "current_flow_bpd": 400000,
            "distance_km": 2400,
            "lead_time_days": 6,
            "transport_cost_usd_bbl": 1.9,
            "risk_base": 28,
            "status": "active",
            "waypoints": [[24.5, 58.0], [23.5, 65.0]]
        },
        {
            "_id": "route_010",
            "from_node": "sup_russia",
            "to_node": "port_jnpt",
            "corridor": "Direct / Malacca",
            "corridor_id": None,
            "capacity_bpd": 350000,
            "current_flow_bpd": 300000,
            "distance_km": 3700,
            "lead_time_days": 9,
            "transport_cost_usd_bbl": 2.4,
            "risk_base": 59,
            "status": "active",
            "waypoints": [[35.0, 25.0], [27.0, 34.0], [13.0, 43.0], [10.0, 55.0], [15.0, 68.0]]
        }
    ]

    risk_events = [
        {
            "_id": "evt_001",
            "title": "Renewed sanctions on Iranian crude exports",
            "corridor": "Strait of Hormuz",
            "corridor_id": "corr_hormuz",
            "severity": 60,
            "source": "manual",
            "category": "sanctions",
            "description": "Stricter enforcement on Persian Gulf maritime traffic and naval patrols."
        },
        {
            "_id": "evt_002",
            "title": "Drone attack near Bab-el-Mandeb chokepoint",
            "corridor": "Red Sea / Bab-el-Mandeb",
            "corridor_id": "corr_redsea",
            "severity": 75,
            "source": "manual",
            "category": "shipping_attack",
            "description": "Commercial tankers rerouting around Cape of Good Hope due to safety threats."
        },
        {
            "_id": "evt_003",
            "title": "Naval exercise near Strait of Hormuz",
            "corridor": "Strait of Hormuz",
            "corridor_id": "corr_hormuz",
            "severity": 45,
            "source": "manual",
            "category": "conflict",
            "description": "Temporary military maneuvers causing shipping delay spikes."
        },
        {
            "_id": "evt_004",
            "title": "JNPT Port berth maintenance bottleneck",
            "corridor": "Direct Route",
            "corridor_id": None,
            "severity": 30,
            "source": "manual",
            "category": "other",
            "description": "Offloading queue times increased by 1.5 days."
        },
        {
            "_id": "evt_005",
            "title": "Diplomatic standoff in Persian Gulf",
            "corridor": "Strait of Hormuz",
            "corridor_id": "corr_hormuz",
            "severity": 65,
            "source": "manual",
            "category": "diplomatic",
            "description": "Elevated insurance premiums for tankers transiting Gulf waters."
        }
    ]

    scenario_templates = [
        {
            "_id": "hormuz_closure",
            "label": "Strait of Hormuz Closure (Severe)",
            "event_type": "hormuz_closure",
            "default_severity": 5,
            "default_duration_days": 30,
            "affected_corridor_id": "corr_hormuz",
            "description": "Complete blockade or closure of Strait of Hormuz disrupting 42% of India's crude imports."
        },
        {
            "_id": "redsea_disruption",
            "label": "Red Sea Shipping Suspension",
            "event_type": "redsea_disruption",
            "default_severity": 4,
            "default_duration_days": 45,
            "affected_corridor_id": "corr_redsea",
            "description": "Severe maritime attack risk forcing rerouting of Russian and European crude around Africa."
        },
        {
            "_id": "supplier_disruption",
            "label": "Saudi Export Terminal Outage",
            "event_type": "supplier_disruption",
            "default_severity": 4,
            "default_duration_days": 21,
            "affected_supplier_id": "sup_saudi",
            "description": "Unplanned outage at Ras Tanura export terminal reducing Saudi crude flow by 70%."
        },
        {
            "_id": "port_disruption",
            "label": "JNPT Port Terminal Outage",
            "event_type": "port_disruption",
            "default_severity": 4,
            "default_duration_days": 14,
            "affected_port_id": "port_jnpt",
            "description": "Severe weather damage at JNPT offloading berths slowing crude intake to Mumbai refineries."
        }
    ]

    countries = [
        {
            "_id": "IND",
            "name": "India",
            "iso_code": "IND",
            "is_import_dependent": True,
            "daily_consumption_bpd": 5340000,
            "total_daily_import_bpd": 4700000,
            "strategic_reserve_bbl": 42000000,
            "reserve_safety_floor_bbl": 8000000,
            "reserve_days": 9.5
        }
    ]

    risk_scores = []

    collections = {
        "suppliers": suppliers,
        "ports": ports,
        "refineries": refineries,
        "corridors": corridors,
        "routes": routes,
        "risk_events": risk_events,
        "scenario_templates": scenario_templates,
        "countries": countries,
        "risk_scores": risk_scores
    }

    for name, docs in collections.items():
        coll = db[name]
        coll.delete_many({})
        if docs:
            coll.insert_many(docs)
            print(f"Collection '{name}': seeded {len(docs)} documents into cluster database '{DATABASE_NAME}'.")
        else:
            print(f"Collection '{name}': cleared successfully (0 documents seeded).")

    print("\nDatabase seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
