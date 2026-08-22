import os
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
    print(f"Connecting to MongoDB Atlas Cluster: {MONGODB_URI}")
    client = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]

    suppliers = [
        {
                "_id": "sup_russia",
                "name": "Russia",
                "country_iso": "RUS",
                "lat": 60.35,
                "lng": 28.67,
                "primary_terminal": "Primorsk Oil Terminal",
                "max_capacity_bpd": 10500000,
                "current_export_bpd": 1700000,
                "current_total_export": 4700000,
                "base_price_usd_bbl": 65.0,
                "reliability_score": 0.85,
                "notes": "Crude exporter via Primorsk Oil Terminal",
                "wgi_indicators": {
                        "political_stability": 0.02,
                        "rule_of_law": -0.52,
                        "control_of_corruption": -0.81,
                        "government_effectiveness": -0.2
                }
        },
        {
                "_id": "sup_iraq",
                "name": "Iraq",
                "country_iso": "IRQ",
                "lat": 29.68,
                "lng": 48.8,
                "primary_terminal": "Basra Oil Terminal (ABOT)",
                "max_capacity_bpd": 5000000,
                "current_export_bpd": 950000,
                "current_total_export": 3500000,
                "base_price_usd_bbl": 72.0,
                "reliability_score": 0.82,
                "notes": "Crude exporter via Basra Oil Terminal (ABOT)",
                "wgi_indicators": {
                        "political_stability": -0.77,
                        "rule_of_law": -0.66,
                        "control_of_corruption": -1.06,
                        "government_effectiveness": -0.8
                }
        },
        {
                "_id": "sup_saudi_arabia",
                "name": "Saudi Arabia",
                "country_iso": "SAU",
                "lat": 26.64,
                "lng": 50.16,
                "primary_terminal": "Ras Tanura Port",
                "max_capacity_bpd": 12000000,
                "current_export_bpd": 700000,
                "current_total_export": 6200000,
                "base_price_usd_bbl": 78.0,
                "reliability_score": 0.9,
                "notes": "Crude exporter via Ras Tanura Port",
                "wgi_indicators": {
                        "political_stability": 0.6,
                        "rule_of_law": 0.42,
                        "control_of_corruption": 0.52,
                        "government_effectiveness": 0.66
                }
        },
        {
                "_id": "sup_united_arab_emirates",
                "name": "United Arab Emirates",
                "country_iso": "ARE",
                "lat": 25.12,
                "lng": 56.33,
                "primary_terminal": "Fujairah Oil Terminal",
                "max_capacity_bpd": 5000000,
                "current_export_bpd": 550000,
                "current_total_export": 4000000,
                "base_price_usd_bbl": 76.0,
                "reliability_score": 0.95,
                "notes": "Crude exporter via Fujairah Oil Terminal",
                "wgi_indicators": {
                        "political_stability": 1.17,
                        "rule_of_law": 0.62,
                        "control_of_corruption": 0.86,
                        "government_effectiveness": 1.03
                }
        },
        {
                "_id": "sup_united_states",
                "name": "United States",
                "country_iso": "USA",
                "lat": 29.73,
                "lng": -95.02,
                "primary_terminal": "Houston Ship Channel",
                "max_capacity_bpd": 14500000,
                "current_export_bpd": 450000,
                "current_total_export": 4500000,
                "base_price_usd_bbl": 72.0,
                "reliability_score": 0.98,
                "notes": "Crude exporter via Houston Ship Channel",
                "wgi_indicators": {
                        "political_stability": 0.57,
                        "rule_of_law": 0.94,
                        "control_of_corruption": 0.79,
                        "government_effectiveness": 1.11
                }
        },
        {
                "_id": "sup_kuwait",
                "name": "Kuwait",
                "country_iso": "KWT",
                "lat": 29.08,
                "lng": 48.14,
                "primary_terminal": "Mina Al-Ahmadi Port",
                "max_capacity_bpd": 3000000,
                "current_export_bpd": 200000,
                "current_total_export": 1800000,
                "base_price_usd_bbl": 74.0,
                "reliability_score": 0.91,
                "notes": "Crude exporter via Mina Al-Ahmadi Port",
                "wgi_indicators": {
                        "political_stability": 0.84,
                        "rule_of_law": 0.44,
                        "control_of_corruption": 0.09,
                        "government_effectiveness": 0.31
                }
        },
        {
                "_id": "sup_nigeria",
                "name": "Nigeria",
                "country_iso": "NGA",
                "lat": 4.43,
                "lng": 7.17,
                "primary_terminal": "Bonny Oil Terminal",
                "max_capacity_bpd": 2200000,
                "current_export_bpd": 180000,
                "current_total_export": 1400000,
                "base_price_usd_bbl": 74.0,
                "reliability_score": 0.78,
                "notes": "Crude exporter via Bonny Oil Terminal",
                "wgi_indicators": {
                        "political_stability": -0.73,
                        "rule_of_law": -0.41,
                        "control_of_corruption": -0.99,
                        "government_effectiveness": -0.73
                }
        },
        {
                "_id": "sup_angola",
                "name": "Angola",
                "country_iso": "AGO",
                "lat": -8.8,
                "lng": 13.23,
                "primary_terminal": "Luanda Port",
                "max_capacity_bpd": 1400000,
                "current_export_bpd": 170000,
                "current_total_export": 1000000,
                "base_price_usd_bbl": 72.0,
                "reliability_score": 0.8,
                "notes": "Crude exporter via Luanda Port",
                "wgi_indicators": {
                        "political_stability": 0.0,
                        "rule_of_law": 0.0,
                        "control_of_corruption": 0.0,
                        "government_effectiveness": 0.0
                }
        },
        {
                "_id": "sup_brazil",
                "name": "Brazil",
                "country_iso": "BRA",
                "lat": -23.96,
                "lng": -46.3,
                "primary_terminal": "Santos Port",
                "max_capacity_bpd": 4500000,
                "current_export_bpd": 150000,
                "current_total_export": 1800000,
                "base_price_usd_bbl": 70.0,
                "reliability_score": 0.76,
                "notes": "Crude exporter via Santos Port",
                "wgi_indicators": {
                        "political_stability": 0.0,
                        "rule_of_law": 0.0,
                        "control_of_corruption": 0.0,
                        "government_effectiveness": 0.0
                }
        },
        {
                "_id": "sup_egypt",
                "name": "Egypt",
                "country_iso": "EGY",
                "lat": 29.65,
                "lng": 32.34,
                "primary_terminal": "Suez / Ain Sokhna Port",
                "max_capacity_bpd": 700000,
                "current_export_bpd": 100000,
                "current_total_export": 300000,
                "base_price_usd_bbl": 71.0,
                "reliability_score": 0.71,
                "notes": "Crude exporter via Suez / Ain Sokhna Port",
                "wgi_indicators": {
                        "political_stability": -0.03,
                        "rule_of_law": -0.24,
                        "control_of_corruption": -0.76,
                        "government_effectiveness": -0.02
                }
        },
        {
                "_id": "sup_colombia",
                "name": "Colombia",
                "country_iso": "COL",
                "lat": 9.4,
                "lng": -75.68,
                "primary_terminal": "Cove\u00f1as Port",
                "max_capacity_bpd": 900000,
                "current_export_bpd": 90000,
                "current_total_export": 600000,
                "base_price_usd_bbl": 69.0,
                "reliability_score": 0.67,
                "notes": "Crude exporter via Cove\u00f1as Port",
                "wgi_indicators": {
                        "political_stability": 0.0,
                        "rule_of_law": 0.0,
                        "control_of_corruption": 0.0,
                        "government_effectiveness": 0.0
                }
        },
        {
                "_id": "sup_qatar",
                "name": "Qatar",
                "country_iso": "QAT",
                "lat": 24.99,
                "lng": 51.55,
                "primary_terminal": "Mesaieed Port",
                "max_capacity_bpd": 1500000,
                "current_export_bpd": 85000,
                "current_total_export": 700000,
                "base_price_usd_bbl": 75.0,
                "reliability_score": 0.93,
                "notes": "Crude exporter via Mesaieed Port",
                "wgi_indicators": {
                        "political_stability": 1.29,
                        "rule_of_law": 0.68,
                        "control_of_corruption": 0.53,
                        "government_effectiveness": 0.94
                }
        },
        {
                "_id": "sup_oman",
                "name": "Oman",
                "country_iso": "OMN",
                "lat": 23.62,
                "lng": 58.56,
                "primary_terminal": "Mina Al-Fahal Port",
                "max_capacity_bpd": 1100000,
                "current_export_bpd": 80000,
                "current_total_export": 800000,
                "base_price_usd_bbl": 73.0,
                "reliability_score": 0.81,
                "notes": "Crude exporter via Mina Al-Fahal Port",
                "wgi_indicators": {
                        "political_stability": 1.06,
                        "rule_of_law": 0.59,
                        "control_of_corruption": 0.32,
                        "government_effectiveness": 0.5
                }
        },
        {
                "_id": "sup_mexico",
                "name": "Mexico",
                "country_iso": "MEX",
                "lat": 18.43,
                "lng": -93.2,
                "primary_terminal": "Dos Bocas Port",
                "max_capacity_bpd": 1900000,
                "current_export_bpd": 60000,
                "current_total_export": 900000,
                "base_price_usd_bbl": 69.0,
                "reliability_score": 0.6,
                "notes": "Crude exporter via Dos Bocas Port",
                "wgi_indicators": {
                        "political_stability": 0.0,
                        "rule_of_law": 0.0,
                        "control_of_corruption": 0.0,
                        "government_effectiveness": 0.0
                }
        },
        {
                "_id": "sup_venezuela",
                "name": "Venezuela",
                "country_iso": "VEN",
                "lat": 10.22,
                "lng": -64.68,
                "primary_terminal": "Jose Terminal",
                "max_capacity_bpd": 1500000,
                "current_export_bpd": 50000,
                "current_total_export": 1160000,
                "base_price_usd_bbl": 58.0,
                "reliability_score": 0.68,
                "notes": "Crude exporter via Jose Terminal",
                "wgi_indicators": {
                        "political_stability": 0.0,
                        "rule_of_law": 0.0,
                        "control_of_corruption": 0.0,
                        "government_effectiveness": 0.0
                }
        },
        {
                "_id": "sup_guyana",
                "name": "Guyana",
                "country_iso": "GUY",
                "lat": 7.35,
                "lng": -57.45,
                "primary_terminal": "Liza Destiny FPSO",
                "max_capacity_bpd": 900000,
                "current_export_bpd": 45000,
                "current_total_export": 700000,
                "base_price_usd_bbl": 70.0,
                "reliability_score": 0.76,
                "notes": "Crude exporter via Liza Destiny FPSO",
                "wgi_indicators": {
                        "political_stability": 0.0,
                        "rule_of_law": 0.0,
                        "control_of_corruption": 0.0,
                        "government_effectiveness": 0.0
                }
        },
        {
                "_id": "sup_kazakhstan",
                "name": "Kazakhstan",
                "country_iso": "KAZ",
                "lat": 43.65,
                "lng": 51.16,
                "primary_terminal": "Aktau Port",
                "max_capacity_bpd": 2500000,
                "current_export_bpd": 40000,
                "current_total_export": 1500000,
                "base_price_usd_bbl": 72.0,
                "reliability_score": 0.75,
                "notes": "Crude exporter via Aktau Port",
                "wgi_indicators": {
                        "political_stability": 0.0,
                        "rule_of_law": 0.0,
                        "control_of_corruption": 0.0,
                        "government_effectiveness": 0.0
                }
        },
        {
                "_id": "sup_norway",
                "name": "Norway",
                "country_iso": "NOR",
                "lat": 60.81,
                "lng": 5.03,
                "primary_terminal": "Mongstad Oil Terminal",
                "max_capacity_bpd": 2200000,
                "current_export_bpd": 35000,
                "current_total_export": 1800000,
                "base_price_usd_bbl": 73.0,
                "reliability_score": 0.98,
                "notes": "Crude exporter via Mongstad Oil Terminal",
                "wgi_indicators": {
                        "political_stability": 0.0,
                        "rule_of_law": 0.0,
                        "control_of_corruption": 0.0,
                        "government_effectiveness": 0.0
                }
        },
        {
                "_id": "sup_azerbaijan",
                "name": "Azerbaijan",
                "country_iso": "AZE",
                "lat": 40.17,
                "lng": 49.44,
                "primary_terminal": "Sangachal Terminal",
                "max_capacity_bpd": 700000,
                "current_export_bpd": 30000,
                "current_total_export": 500000,
                "base_price_usd_bbl": 71.0,
                "reliability_score": 0.74,
                "notes": "Crude exporter via Sangachal Terminal",
                "wgi_indicators": {
                        "political_stability": 0.0,
                        "rule_of_law": 0.0,
                        "control_of_corruption": 0.0,
                        "government_effectiveness": 0.0
                }
        },
        {
                "_id": "sup_algeria",
                "name": "Algeria",
                "country_iso": "DZA",
                "lat": 35.85,
                "lng": -0.3,
                "primary_terminal": "Arzew Port",
                "max_capacity_bpd": 1500000,
                "current_export_bpd": 25000,
                "current_total_export": 700000,
                "base_price_usd_bbl": 74.0,
                "reliability_score": 0.75,
                "notes": "Crude exporter via Arzew Port",
                "wgi_indicators": {
                        "political_stability": 0.0,
                        "rule_of_law": 0.0,
                        "control_of_corruption": 0.0,
                        "government_effectiveness": 0.0
                }
        },
        {
                "_id": "sup_libya",
                "name": "Libya",
                "country_iso": "LBY",
                "lat": 30.65,
                "lng": 18.35,
                "primary_terminal": "Es Sider Oil Terminal",
                "max_capacity_bpd": 1400000,
                "current_export_bpd": 20000,
                "current_total_export": 1100000,
                "base_price_usd_bbl": 73.0,
                "reliability_score": 0.74,
                "notes": "Crude exporter via Es Sider Oil Terminal",
                "wgi_indicators": {
                        "political_stability": 0.0,
                        "rule_of_law": 0.0,
                        "control_of_corruption": 0.0,
                        "government_effectiveness": 0.0
                }
        },
        {
                "_id": "sup_ecuador",
                "name": "Ecuador",
                "country_iso": "ECU",
                "lat": 0.97,
                "lng": -79.65,
                "primary_terminal": "Esmeraldas Port",
                "max_capacity_bpd": 500000,
                "current_export_bpd": 15000,
                "current_total_export": 400000,
                "base_price_usd_bbl": 65.0,
                "reliability_score": 0.76,
                "notes": "Crude exporter via Esmeraldas Port",
                "wgi_indicators": {
                        "political_stability": 0.0,
                        "rule_of_law": 0.0,
                        "control_of_corruption": 0.0,
                        "government_effectiveness": 0.0
                }
        },
        {
                "_id": "sup_malaysia",
                "name": "Malaysia",
                "country_iso": "MYS",
                "lat": 1.37,
                "lng": 104.12,
                "primary_terminal": "Pengerang Integrated Petroleum Complex",
                "max_capacity_bpd": 600000,
                "current_export_bpd": 15000,
                "current_total_export": 300000,
                "base_price_usd_bbl": 72.0,
                "reliability_score": 0.8,
                "notes": "Crude exporter via Pengerang Integrated Petroleum Complex",
                "wgi_indicators": {
                        "political_stability": 0.9,
                        "rule_of_law": 0.52,
                        "control_of_corruption": 0.32,
                        "government_effectiveness": 0.77
                }
        },
        {
                "_id": "sup_indonesia",
                "name": "Indonesia",
                "country_iso": "IDN",
                "lat": -6.1,
                "lng": 106.88,
                "primary_terminal": "Tanjung Priok Port",
                "max_capacity_bpd": 700000,
                "current_export_bpd": 10000,
                "current_total_export": 150000,
                "base_price_usd_bbl": 74.0,
                "reliability_score": 0.74,
                "notes": "Crude exporter via Tanjung Priok Port",
                "wgi_indicators": {
                        "political_stability": 0.22,
                        "rule_of_law": 0.14,
                        "control_of_corruption": -0.53,
                        "government_effectiveness": 0.19
                }
        },
        {
                "_id": "sup_canada",
                "name": "Canada",
                "country_iso": "CAN",
                "lat": 49.29,
                "lng": -123.23,
                "primary_terminal": "Vancouver Port (Westridge Marine Terminal)",
                "max_capacity_bpd": 5500000,
                "current_export_bpd": 5000,
                "current_total_export": 4500000,
                "base_price_usd_bbl": 65.0,
                "reliability_score": 0.97,
                "notes": "Crude exporter via Vancouver Port (Westridge Marine Terminal)",
                "wgi_indicators": {
                        "political_stability": 0.0,
                        "rule_of_law": 0.0,
                        "control_of_corruption": 0.0,
                        "government_effectiveness": 0.0
                }
        }
]
    ports = [
        {
                "_id": "port_mundra",
                "name": "Mundra Port",
                "country_iso": "IND",
                "type": "indian_port",
                "lat": 22.7363,
                "lng": 69.7032,
                "throughput_capacity_bpd": 1500000
        },
        {
                "_id": "port_vadinar",
                "name": "Vadinar Port (Sikka/Vadinar)",
                "country_iso": "IND",
                "type": "indian_port",
                "lat": 22.4507,
                "lng": 69.7199,
                "throughput_capacity_bpd": 1400000
        },
        {
                "_id": "port_jnpt",
                "name": "Mumbai Port",
                "country_iso": "IND",
                "type": "indian_port",
                "lat": 18.9498,
                "lng": 72.9477,
                "throughput_capacity_bpd": 650000
        },
        {
                "_id": "port_kochi",
                "name": "Kochi Port (Cochin)",
                "country_iso": "IND",
                "type": "indian_port",
                "lat": 9.9667,
                "lng": 76.05,
                "throughput_capacity_bpd": 320000
        },
        {
                "_id": "port_mangalore",
                "name": "New Mangalore Port",
                "country_iso": "IND",
                "type": "indian_port",
                "lat": 12.9496,
                "lng": 74.809,
                "throughput_capacity_bpd": 350000
        },
        {
                "_id": "port_vizag",
                "name": "Visakhapatnam Port (Vizag)",
                "country_iso": "IND",
                "type": "indian_port",
                "lat": 17.6868,
                "lng": 83.2185,
                "throughput_capacity_bpd": 350000
        },
        {
                "_id": "port_paradip",
                "name": "Paradip Port",
                "country_iso": "IND",
                "type": "indian_port",
                "lat": 20.266,
                "lng": 86.6746,
                "throughput_capacity_bpd": 350000
        },
        {
                "_id": "port_ennore",
                "name": "Kamarajar Port (Ennore)",
                "country_iso": "IND",
                "type": "indian_port",
                "lat": 13.2339,
                "lng": 80.33,
                "throughput_capacity_bpd": 300000
        },
        {
                "_id": "port_chennai",
                "name": "Chennai Port",
                "country_iso": "IND",
                "type": "indian_port",
                "lat": 13.0827,
                "lng": 80.2707,
                "throughput_capacity_bpd": 250000
        },
        {
                "_id": "port_haldia",
                "name": "Haldia Port",
                "country_iso": "IND",
                "type": "indian_port",
                "lat": 22.0257,
                "lng": 88.0583,
                "throughput_capacity_bpd": 170000
        },
        {
                "_id": "port_kakinada",
                "name": "Kakinada Port",
                "country_iso": "IND",
                "type": "indian_port",
                "lat": 16.9891,
                "lng": 82.2475,
                "throughput_capacity_bpd": 150000
        },
        {
                "_id": "port_kandla",
                "name": "Kandla / Deendayal Port",
                "country_iso": "IND",
                "type": "indian_port",
                "lat": 23.0333,
                "lng": 70.2167,
                "throughput_capacity_bpd": 400000
        },
        {
                "_id": "port_primorsk_oil_terminal",
                "name": "Primorsk Oil Terminal",
                "country_iso": "RUS",
                "type": "origin",
                "lat": 60.35,
                "lng": 28.67,
                "throughput_capacity_bpd": 1200000
        },
        {
                "_id": "port_ust_luga_oil",
                "name": "Ust-Luga Oil Terminal",
                "country_iso": "RUS",
                "type": "origin",
                "lat": 59.68,
                "lng": 28.44,
                "throughput_capacity_bpd": 1500000
        },
        {
                "_id": "port_novorossiysk_port_sheskharis",
                "name": "Novorossiysk Port (Sheskharis)",
                "country_iso": "RUS",
                "type": "origin",
                "lat": 44.71,
                "lng": 37.78,
                "throughput_capacity_bpd": 700000
        },
        {
                "_id": "port_kozmino_oil_terminal",
                "name": "Kozmino Oil Terminal",
                "country_iso": "RUS",
                "type": "origin",
                "lat": 42.73,
                "lng": 133.03,
                "throughput_capacity_bpd": 850000
        },
        {
                "_id": "port_de_kastri_oil",
                "name": "De-Kastri Oil Terminal",
                "country_iso": "RUS",
                "type": "origin",
                "lat": 51.47,
                "lng": 140.77,
                "throughput_capacity_bpd": 300000
        },
        {
                "_id": "port_basra_oil_terminal",
                "name": "Basra Oil Terminal (ABOT)",
                "country_iso": "IRQ",
                "type": "origin",
                "lat": 29.68,
                "lng": 48.8,
                "throughput_capacity_bpd": 1800000
        },
        {
                "_id": "port_khor_al_amaya",
                "name": "Khor Al-Amaya Oil Terminal",
                "country_iso": "IRQ",
                "type": "origin",
                "lat": 29.75,
                "lng": 48.8,
                "throughput_capacity_bpd": 600000
        },
        {
                "_id": "port_al_basra_oil",
                "name": "Al-Basra Oil Terminal",
                "country_iso": "IRQ",
                "type": "origin",
                "lat": 29.67,
                "lng": 48.8,
                "throughput_capacity_bpd": 1500000
        },
        {
                "_id": "port_ras_tanura_port",
                "name": "Ras Tanura Port",
                "country_iso": "SAU",
                "type": "origin",
                "lat": 26.64,
                "lng": 50.16,
                "throughput_capacity_bpd": 6500000
        },
        {
                "_id": "port_juaymah_oil_terminal",
                "name": "Juaymah Oil Terminal",
                "country_iso": "SAU",
                "type": "origin",
                "lat": 26.98,
                "lng": 50.05,
                "throughput_capacity_bpd": 3000000
        },
        {
                "_id": "port_yanbu_oil_terminal",
                "name": "Yanbu Oil Terminal",
                "country_iso": "SAU",
                "type": "origin",
                "lat": 24.09,
                "lng": 38.06,
                "throughput_capacity_bpd": 4000000
        },
        {
                "_id": "port_jazan_port",
                "name": "Jazan Port",
                "country_iso": "SAU",
                "type": "origin",
                "lat": 16.9,
                "lng": 42.55,
                "throughput_capacity_bpd": 400000
        },
        {
                "_id": "port_fujairah_oil_terminal",
                "name": "Fujairah Oil Terminal",
                "country_iso": "ARE",
                "type": "origin",
                "lat": 25.12,
                "lng": 56.33,
                "throughput_capacity_bpd": 2000000
        },
        {
                "_id": "port_jebel_ali_port",
                "name": "Jebel Ali Port",
                "country_iso": "ARE",
                "type": "origin",
                "lat": 24.99,
                "lng": 55.06,
                "throughput_capacity_bpd": 1000000
        },
        {
                "_id": "port_mina_al_hamriya",
                "name": "Mina Al Hamriya",
                "country_iso": "ARE",
                "type": "origin",
                "lat": 25.3,
                "lng": 55.33,
                "throughput_capacity_bpd": 500000
        },
        {
                "_id": "port_ruwais_port",
                "name": "Ruwais Port",
                "country_iso": "ARE",
                "type": "origin",
                "lat": 24.11,
                "lng": 52.73,
                "throughput_capacity_bpd": 3000000
        },
        {
                "_id": "port_houston_ship_channel",
                "name": "Houston Ship Channel",
                "country_iso": "USA",
                "type": "origin",
                "lat": 29.73,
                "lng": -95.02,
                "throughput_capacity_bpd": 3000000
        },
        {
                "_id": "port_corpus_christi_port",
                "name": "Corpus Christi Port",
                "country_iso": "USA",
                "type": "origin",
                "lat": 27.8006,
                "lng": -97.3964,
                "throughput_capacity_bpd": 3000000
        },
        {
                "_id": "port_louisiana_offshore_oil",
                "name": "Louisiana Offshore Oil Port (LOOP)",
                "country_iso": "USA",
                "type": "origin",
                "lat": 28.88,
                "lng": -90.03,
                "throughput_capacity_bpd": 1800000
        },
        {
                "_id": "port_port_of_south",
                "name": "Port of South Louisiana",
                "country_iso": "USA",
                "type": "origin",
                "lat": 29.95,
                "lng": -90.3,
                "throughput_capacity_bpd": 2500000
        },
        {
                "_id": "port_beaumont_port_arthur",
                "name": "Beaumont-Port Arthur",
                "country_iso": "USA",
                "type": "origin",
                "lat": 29.94,
                "lng": -94.02,
                "throughput_capacity_bpd": 2000000
        },
        {
                "_id": "port_mina_al_ahmadi",
                "name": "Mina Al-Ahmadi Port",
                "country_iso": "KWT",
                "type": "origin",
                "lat": 29.08,
                "lng": 48.14,
                "throughput_capacity_bpd": 2500000
        },
        {
                "_id": "port_mina_abdullah_port",
                "name": "Mina Abdullah Port",
                "country_iso": "KWT",
                "type": "origin",
                "lat": 28.94,
                "lng": 48.15,
                "throughput_capacity_bpd": 1500000
        },
        {
                "_id": "port_shuaiba_port",
                "name": "Shuaiba Port",
                "country_iso": "KWT",
                "type": "origin",
                "lat": 29.04,
                "lng": 48.16,
                "throughput_capacity_bpd": 500000
        },
        {
                "_id": "port_bonny_oil_terminal",
                "name": "Bonny Oil Terminal",
                "country_iso": "NGA",
                "type": "origin",
                "lat": 4.43,
                "lng": 7.17,
                "throughput_capacity_bpd": 1000000
        },
        {
                "_id": "port_forcados_oil_terminal",
                "name": "Forcados Oil Terminal",
                "country_iso": "NGA",
                "type": "origin",
                "lat": 5.35,
                "lng": 5.35,
                "throughput_capacity_bpd": 400000
        },
        {
                "_id": "port_qua_iboe_terminal",
                "name": "Qua Iboe Terminal",
                "country_iso": "NGA",
                "type": "origin",
                "lat": 4.53,
                "lng": 8.02,
                "throughput_capacity_bpd": 500000
        },
        {
                "_id": "port_escravos_terminal",
                "name": "Escravos Terminal",
                "country_iso": "NGA",
                "type": "origin",
                "lat": 5.6,
                "lng": 5.35,
                "throughput_capacity_bpd": 300000
        },
        {
                "_id": "port_agbami_fpso",
                "name": "Agbami FPSO",
                "country_iso": "NGA",
                "type": "origin",
                "lat": 4.9,
                "lng": 5.8,
                "throughput_capacity_bpd": 250000
        },
        {
                "_id": "port_luanda_port",
                "name": "Luanda Port",
                "country_iso": "AGO",
                "type": "origin",
                "lat": -8.8,
                "lng": 13.23,
                "throughput_capacity_bpd": 500000
        },
        {
                "_id": "port_dalia_fpso",
                "name": "Dalia FPSO",
                "country_iso": "AGO",
                "type": "origin",
                "lat": -6.1,
                "lng": 11.4,
                "throughput_capacity_bpd": 240000
        },
        {
                "_id": "port_girassol_fpso",
                "name": "Girassol FPSO",
                "country_iso": "AGO",
                "type": "origin",
                "lat": -6.5,
                "lng": 11.7,
                "throughput_capacity_bpd": 200000
        },
        {
                "_id": "port_pazflor_fpso",
                "name": "Pazflor FPSO",
                "country_iso": "AGO",
                "type": "origin",
                "lat": -6.0,
                "lng": 11.5,
                "throughput_capacity_bpd": 220000
        },
        {
                "_id": "port_santos_port",
                "name": "Santos Port",
                "country_iso": "BRA",
                "type": "origin",
                "lat": -23.96,
                "lng": -46.3,
                "throughput_capacity_bpd": 1000000
        },
        {
                "_id": "port_rio_de_janeiro",
                "name": "Rio de Janeiro Port",
                "country_iso": "BRA",
                "type": "origin",
                "lat": -22.9,
                "lng": -43.17,
                "throughput_capacity_bpd": 700000
        },
        {
                "_id": "port_itagua\u00ed_port",
                "name": "Itagua\u00ed Port",
                "country_iso": "BRA",
                "type": "origin",
                "lat": -22.92,
                "lng": -43.83,
                "throughput_capacity_bpd": 600000
        },
        {
                "_id": "port_s\u00e3o_sebasti\u00e3o_oil",
                "name": "S\u00e3o Sebasti\u00e3o Oil Terminal",
                "country_iso": "BRA",
                "type": "origin",
                "lat": -23.81,
                "lng": -45.41,
                "throughput_capacity_bpd": 1500000
        },
        {
                "_id": "port_suez_ain_sokhna",
                "name": "Suez / Ain Sokhna Port",
                "country_iso": "EGY",
                "type": "origin",
                "lat": 29.65,
                "lng": 32.34,
                "throughput_capacity_bpd": 600000
        },
        {
                "_id": "port_sidi_kerir_oil",
                "name": "Sidi Kerir Oil Terminal",
                "country_iso": "EGY",
                "type": "origin",
                "lat": 31.09,
                "lng": 29.65,
                "throughput_capacity_bpd": 2500000
        },
        {
                "_id": "port_alexandria_port",
                "name": "Alexandria Port",
                "country_iso": "EGY",
                "type": "origin",
                "lat": 31.2,
                "lng": 29.88,
                "throughput_capacity_bpd": 500000
        },
        {
                "_id": "port_cove\u00f1as_port",
                "name": "Cove\u00f1as Port",
                "country_iso": "COL",
                "type": "origin",
                "lat": 9.4,
                "lng": -75.68,
                "throughput_capacity_bpd": 850000
        },
        {
                "_id": "port_santa_marta_port",
                "name": "Santa Marta Port",
                "country_iso": "COL",
                "type": "origin",
                "lat": 11.24,
                "lng": -74.21,
                "throughput_capacity_bpd": 200000
        },
        {
                "_id": "port_tumaco_port",
                "name": "Tumaco Port",
                "country_iso": "COL",
                "type": "origin",
                "lat": 1.8,
                "lng": -78.77,
                "throughput_capacity_bpd": 200000
        },
        {
                "_id": "port_mesaieed_port",
                "name": "Mesaieed Port",
                "country_iso": "QAT",
                "type": "origin",
                "lat": 24.99,
                "lng": 51.55,
                "throughput_capacity_bpd": 700000
        },
        {
                "_id": "port_ras_laffan_port",
                "name": "Ras Laffan Port",
                "country_iso": "QAT",
                "type": "origin",
                "lat": 25.92,
                "lng": 51.53,
                "throughput_capacity_bpd": 500000
        },
        {
                "_id": "port_mina_al_fahal",
                "name": "Mina Al-Fahal Port",
                "country_iso": "OMN",
                "type": "origin",
                "lat": 23.62,
                "lng": 58.56,
                "throughput_capacity_bpd": 700000
        },
        {
                "_id": "port_duqm_port",
                "name": "Duqm Port",
                "country_iso": "OMN",
                "type": "origin",
                "lat": 19.67,
                "lng": 57.7,
                "throughput_capacity_bpd": 500000
        },
        {
                "_id": "port_salalah_port",
                "name": "Salalah Port",
                "country_iso": "OMN",
                "type": "origin",
                "lat": 16.95,
                "lng": 54.0,
                "throughput_capacity_bpd": 200000
        },
        {
                "_id": "port_dos_bocas_port",
                "name": "Dos Bocas Port",
                "country_iso": "MEX",
                "type": "origin",
                "lat": 18.43,
                "lng": -93.2,
                "throughput_capacity_bpd": 700000
        },
        {
                "_id": "port_cayo_arcas_terminal",
                "name": "Cayo Arcas Terminal",
                "country_iso": "MEX",
                "type": "origin",
                "lat": 20.19,
                "lng": -91.98,
                "throughput_capacity_bpd": 800000
        },
        {
                "_id": "port_pajaritos_port",
                "name": "Pajaritos Port",
                "country_iso": "MEX",
                "type": "origin",
                "lat": 18.15,
                "lng": -94.43,
                "throughput_capacity_bpd": 500000
        },
        {
                "_id": "port_jose_terminal",
                "name": "Jose Terminal",
                "country_iso": "VEN",
                "type": "origin",
                "lat": 10.22,
                "lng": -64.68,
                "throughput_capacity_bpd": 1500000
        },
        {
                "_id": "port_amuay_port",
                "name": "Amuay Port",
                "country_iso": "VEN",
                "type": "origin",
                "lat": 11.75,
                "lng": -70.22,
                "throughput_capacity_bpd": 700000
        },
        {
                "_id": "port_puerto_la_cruz",
                "name": "Puerto La Cruz",
                "country_iso": "VEN",
                "type": "origin",
                "lat": 10.21,
                "lng": -64.63,
                "throughput_capacity_bpd": 500000
        },
        {
                "_id": "port_liza_destiny_fpso",
                "name": "Liza Destiny FPSO",
                "country_iso": "GUY",
                "type": "origin",
                "lat": 7.35,
                "lng": -57.45,
                "throughput_capacity_bpd": 160000
        },
        {
                "_id": "port_liza_unity_fpso",
                "name": "Liza Unity FPSO",
                "country_iso": "GUY",
                "type": "origin",
                "lat": 7.3,
                "lng": -57.5,
                "throughput_capacity_bpd": 250000
        },
        {
                "_id": "port_payara_prosperity_fpso",
                "name": "Payara Prosperity FPSO",
                "country_iso": "GUY",
                "type": "origin",
                "lat": 7.4,
                "lng": -57.3,
                "throughput_capacity_bpd": 250000
        },
        {
                "_id": "port_aktau_port",
                "name": "Aktau Port",
                "country_iso": "KAZ",
                "type": "origin",
                "lat": 43.65,
                "lng": 51.16,
                "throughput_capacity_bpd": 200000
        },
        {
                "_id": "port_kuryk_port",
                "name": "Kuryk Port",
                "country_iso": "KAZ",
                "type": "origin",
                "lat": 43.18,
                "lng": 51.62,
                "throughput_capacity_bpd": 250000
        },
        {
                "_id": "port_mongstad_oil_terminal",
                "name": "Mongstad Oil Terminal",
                "country_iso": "NOR",
                "type": "origin",
                "lat": 60.81,
                "lng": 5.03,
                "throughput_capacity_bpd": 600000
        },
        {
                "_id": "port_sture_oil_terminal",
                "name": "Sture Oil Terminal",
                "country_iso": "NOR",
                "type": "origin",
                "lat": 60.6,
                "lng": 4.88,
                "throughput_capacity_bpd": 600000
        },
        {
                "_id": "port_k\u00e5rst\u00f8_terminal",
                "name": "K\u00e5rst\u00f8 Terminal",
                "country_iso": "NOR",
                "type": "origin",
                "lat": 59.28,
                "lng": 5.52,
                "throughput_capacity_bpd": 300000
        },
        {
                "_id": "port_sangachal_terminal",
                "name": "Sangachal Terminal",
                "country_iso": "AZE",
                "type": "origin",
                "lat": 40.17,
                "lng": 49.44,
                "throughput_capacity_bpd": 1000000
        },
        {
                "_id": "port_baku_port",
                "name": "Baku Port",
                "country_iso": "AZE",
                "type": "origin",
                "lat": 40.37,
                "lng": 49.87,
                "throughput_capacity_bpd": 500000
        },
        {
                "_id": "port_arzew_port",
                "name": "Arzew Port",
                "country_iso": "DZA",
                "type": "origin",
                "lat": 35.85,
                "lng": -0.3,
                "throughput_capacity_bpd": 800000
        },
        {
                "_id": "port_skikda_port",
                "name": "Skikda Port",
                "country_iso": "DZA",
                "type": "origin",
                "lat": 36.88,
                "lng": 6.91,
                "throughput_capacity_bpd": 500000
        },
        {
                "_id": "port_bejaia_port",
                "name": "Bejaia Port",
                "country_iso": "DZA",
                "type": "origin",
                "lat": 36.75,
                "lng": 5.08,
                "throughput_capacity_bpd": 400000
        },
        {
                "_id": "port_es_sider_oil",
                "name": "Es Sider Oil Terminal",
                "country_iso": "LBY",
                "type": "origin",
                "lat": 30.65,
                "lng": 18.35,
                "throughput_capacity_bpd": 600000
        },
        {
                "_id": "port_ras_lanuf_port",
                "name": "Ras Lanuf Port",
                "country_iso": "LBY",
                "type": "origin",
                "lat": 30.48,
                "lng": 18.56,
                "throughput_capacity_bpd": 400000
        },
        {
                "_id": "port_zawiya_port",
                "name": "Zawiya Port",
                "country_iso": "LBY",
                "type": "origin",
                "lat": 32.75,
                "lng": 12.72,
                "throughput_capacity_bpd": 300000
        },
        {
                "_id": "port_brega_oil_terminal",
                "name": "Brega Oil Terminal",
                "country_iso": "LBY",
                "type": "origin",
                "lat": 30.42,
                "lng": 19.57,
                "throughput_capacity_bpd": 300000
        },
        {
                "_id": "port_esmeraldas_port",
                "name": "Esmeraldas Port",
                "country_iso": "ECU",
                "type": "origin",
                "lat": 0.97,
                "lng": -79.65,
                "throughput_capacity_bpd": 400000
        },
        {
                "_id": "port_balao_oil_terminal",
                "name": "Balao Oil Terminal",
                "country_iso": "ECU",
                "type": "origin",
                "lat": 0.93,
                "lng": -79.67,
                "throughput_capacity_bpd": 360000
        },
        {
                "_id": "port_pengerang_integrated_petroleum",
                "name": "Pengerang Integrated Petroleum Complex",
                "country_iso": "MYS",
                "type": "origin",
                "lat": 1.37,
                "lng": 104.12,
                "throughput_capacity_bpd": 1000000
        },
        {
                "_id": "port_port_klang",
                "name": "Port Klang",
                "country_iso": "MYS",
                "type": "origin",
                "lat": 3.0,
                "lng": 101.4,
                "throughput_capacity_bpd": 500000
        },
        {
                "_id": "port_kerteh_port",
                "name": "Kerteh Port",
                "country_iso": "MYS",
                "type": "origin",
                "lat": 4.52,
                "lng": 103.45,
                "throughput_capacity_bpd": 300000
        },
        {
                "_id": "port_tanjung_priok_port",
                "name": "Tanjung Priok Port",
                "country_iso": "IDN",
                "type": "origin",
                "lat": -6.1,
                "lng": 106.88,
                "throughput_capacity_bpd": 500000
        },
        {
                "_id": "port_balikpapan_port",
                "name": "Balikpapan Port",
                "country_iso": "IDN",
                "type": "origin",
                "lat": -1.27,
                "lng": 116.83,
                "throughput_capacity_bpd": 300000
        },
        {
                "_id": "port_dumai_port",
                "name": "Dumai Port",
                "country_iso": "IDN",
                "type": "origin",
                "lat": 1.68,
                "lng": 101.45,
                "throughput_capacity_bpd": 300000
        },
        {
                "_id": "port_vancouver_port_westridge",
                "name": "Vancouver Port (Westridge Marine Terminal)",
                "country_iso": "CAN",
                "type": "origin",
                "lat": 49.29,
                "lng": -123.23,
                "throughput_capacity_bpd": 890000
        },
        {
                "_id": "port_burnaby_oil_terminal",
                "name": "Burnaby Oil Terminal",
                "country_iso": "CAN",
                "type": "origin",
                "lat": 49.29,
                "lng": -122.95,
                "throughput_capacity_bpd": 890000
        },
        {
                "_id": "port_come_by_chance",
                "name": "Come-by-Chance Port",
                "country_iso": "CAN",
                "type": "origin",
                "lat": 47.82,
                "lng": -53.98,
                "throughput_capacity_bpd": 130000
        },
        {
                "_id": "port_whiffen_head_terminal",
                "name": "Whiffen Head Terminal",
                "country_iso": "CAN",
                "type": "origin",
                "lat": 47.12,
                "lng": -52.98,
                "throughput_capacity_bpd": 300000
        }
]
    refineries = [
        {
                "_id": "ref_jamnagar_refinery_reliance",
                "name": "Jamnagar Refinery (Reliance Industries)",
                "lat": 22.338,
                "lng": 69.841,
                "capacity_bpd": 1364000,
                "connected_ports": [
                        "port_mundra",
                        "port_vadinar"
                ]
        },
        {
                "_id": "ref_vadinar_refinery_nayara",
                "name": "Vadinar Refinery (Nayara Energy)",
                "lat": 22.45,
                "lng": 69.71,
                "capacity_bpd": 400000,
                "connected_ports": [
                        "port_vadinar"
                ]
        },
        {
                "_id": "ref_kochi_refinery_bpcl",
                "name": "Kochi Refinery (BPCL)",
                "lat": 10.099,
                "lng": 76.351,
                "capacity_bpd": 310000,
                "connected_ports": [
                        "port_kochi"
                ]
        },
        {
                "_id": "ref_mangalore_refinery_mrpl",
                "name": "Mangalore Refinery (MRPL)",
                "lat": 12.993,
                "lng": 74.858,
                "capacity_bpd": 300000,
                "connected_ports": [
                        "port_mangalore"
                ]
        },
        {
                "_id": "ref_paradip_refinery_iocl",
                "name": "Paradip Refinery (IOCL)",
                "lat": 20.267,
                "lng": 86.675,
                "capacity_bpd": 300000,
                "connected_ports": [
                        "port_paradip"
                ]
        },
        {
                "_id": "ref_panipat_refinery_iocl",
                "name": "Panipat Refinery (IOCL)",
                "lat": 29.39,
                "lng": 76.96,
                "capacity_bpd": 300000,
                "connected_ports": [
                        "port_mundra",
                        "port_kandla",
                        "port_vadinar"
                ]
        },
        {
                "_id": "ref_gujarat_refinery_koyali",
                "name": "Gujarat Refinery / Koyali Refinery (IOCL)",
                "lat": 22.36,
                "lng": 73.14,
                "capacity_bpd": 274000,
                "connected_ports": [
                        "port_vadinar"
                ]
        },
        {
                "_id": "ref_visakhapatnam_refinery_hpcl",
                "name": "Visakhapatnam Refinery (HPCL)",
                "lat": 17.6868,
                "lng": 83.2185,
                "capacity_bpd": 300000,
                "connected_ports": [
                        "port_vizag"
                ]
        },
        {
                "_id": "ref_mumbai_refinery_bpcl",
                "name": "Mumbai Refinery (BPCL)",
                "lat": 19.01,
                "lng": 72.89,
                "capacity_bpd": 240000,
                "connected_ports": [
                        "port_jnpt"
                ]
        },
        {
                "_id": "ref_mumbai_refinery_hpcl",
                "name": "Mumbai Refinery (HPCL)",
                "lat": 19.0,
                "lng": 72.89,
                "capacity_bpd": 190000,
                "connected_ports": [
                        "port_jnpt"
                ]
        },
        {
                "_id": "ref_manali_refinery_cpcl",
                "name": "Manali Refinery (CPCL)",
                "lat": 13.164,
                "lng": 80.261,
                "capacity_bpd": 210000,
                "connected_ports": [
                        "port_ennore",
                        "port_chennai"
                ]
        },
        {
                "_id": "ref_haldia_refinery_iocl",
                "name": "Haldia Refinery (IOCL)",
                "lat": 22.02,
                "lng": 88.06,
                "capacity_bpd": 160000,
                "connected_ports": [
                        "port_paradip",
                        "port_haldia"
                ]
        },
        {
                "_id": "ref_mathura_refinery_iocl",
                "name": "Mathura Refinery (IOCL)",
                "lat": 27.473,
                "lng": 77.673,
                "capacity_bpd": 160000,
                "connected_ports": [
                        "port_vadinar"
                ]
        },
        {
                "_id": "ref_bina_refinery_bpcl",
                "name": "Bina Refinery (BPCL)",
                "lat": 24.175,
                "lng": 78.18,
                "capacity_bpd": 156000,
                "connected_ports": [
                        "port_vadinar"
                ]
        },
        {
                "_id": "ref_hpcl_mittal_energy",
                "name": "HPCL-Mittal Energy Refinery (Bathinda)",
                "lat": 30.14,
                "lng": 74.95,
                "capacity_bpd": 226000,
                "connected_ports": [
                        "port_mundra"
                ]
        },
        {
                "_id": "ref_hpcl_rajasthan_refinery",
                "name": "HPCL Rajasthan Refinery (Pachpadra)",
                "lat": 25.93,
                "lng": 72.7,
                "capacity_bpd": 180000,
                "connected_ports": [
                        "port_mundra"
                ]
        },
        {
                "_id": "ref_barauni_refinery_iocl",
                "name": "Barauni Refinery (IOCL)",
                "lat": 25.42,
                "lng": 85.92,
                "capacity_bpd": 120000,
                "connected_ports": [
                        "port_paradip"
                ]
        },
        {
                "_id": "ref_numaligarh_refinery_nrl",
                "name": "Numaligarh Refinery (NRL)",
                "lat": 26.64,
                "lng": 93.72,
                "capacity_bpd": 60000,
                "connected_ports": [
                        "port_paradip"
                ]
        },
        {
                "_id": "ref_bongaigaon_refinery_iocl",
                "name": "Bongaigaon Refinery (IOCL)",
                "lat": 26.48,
                "lng": 90.53,
                "capacity_bpd": 54000,
                "connected_ports": [
                        "port_paradip"
                ]
        }
]
    corridors = [
        {
                "_id": "corr_hormuz",
                "name": "Strait of Hormuz",
                "lat": 26.5667,
                "lng": 56.25,
                "region": "Persian Gulf / Arabian Sea",
                "daily_volume_bpd": 2485000,
                "share_of_india_imports_pct": 52.9,
                "base_risk": 62.0,
                "importance": "Critical oil and LNG route"
        },
        {
                "_id": "corr_malacca",
                "name": "Strait of Malacca",
                "lat": 2.5,
                "lng": 101.5,
                "region": "Southeast Asia",
                "daily_volume_bpd": 645000,
                "share_of_india_imports_pct": 13.7,
                "base_risk": 32.0,
                "importance": "World's largest maritime oil-transit chokepoint and major container route"
        },
        {
                "_id": "corr_suez",
                "name": "Suez Canal",
                "lat": 30.5852,
                "lng": 32.2654,
                "region": "Egypt",
                "daily_volume_bpd": 1800000,
                "share_of_india_imports_pct": 38.3,
                "base_risk": 38.0,
                "importance": "Major Europe-Asia shipping corridor"
        },
        {
                "_id": "corr_babelmandeb",
                "name": "Bab el-Mandeb Strait",
                "lat": 12.5833,
                "lng": 43.3333,
                "region": "Red Sea / Gulf of Aden",
                "daily_volume_bpd": 1800000,
                "share_of_india_imports_pct": 38.3,
                "base_risk": 54.0,
                "importance": "Critical Europe-Asia energy and container route"
        },
        {
                "_id": "corr_danish",
                "name": "Danish Straits",
                "lat": 55.7,
                "lng": 12.6,
                "region": "Denmark / Baltic Sea",
                "daily_volume_bpd": 1550000,
                "share_of_india_imports_pct": 33.0,
                "base_risk": 28.0,
                "importance": "Major Baltic energy and commercial shipping gateway"
        },
        {
                "_id": "corr_turkish",
                "name": "Turkish Straits",
                "lat": 41.1,
                "lng": 29.05,
                "region": "Turkey",
                "daily_volume_bpd": 70000,
                "share_of_india_imports_pct": 1.5,
                "base_risk": 45.0,
                "importance": "Critical Black Sea energy and grain shipping route"
        },
        {
                "_id": "corr_bosporus",
                "name": "Bosporus",
                "lat": 41.12,
                "lng": 29.08,
                "region": "Turkey",
                "daily_volume_bpd": 0,
                "share_of_india_imports_pct": 0.0,
                "base_risk": 45.0,
                "importance": "Major Black Sea shipping chokepoint"
        },
        {
                "_id": "corr_dardanelles",
                "name": "Dardanelles",
                "lat": 40.2,
                "lng": 26.4,
                "region": "Turkey",
                "daily_volume_bpd": 0,
                "share_of_india_imports_pct": 0.0,
                "base_risk": 42.0,
                "importance": "Gateway between Black Sea and Mediterranean"
        },
        {
                "_id": "corr_panama",
                "name": "Panama Canal",
                "lat": 9.08,
                "lng": -79.68,
                "region": "Panama",
                "daily_volume_bpd": 270000,
                "share_of_india_imports_pct": 5.7,
                "base_risk": 26.0,
                "importance": "Major Atlantic-Pacific commercial shipping route"
        },
        {
                "_id": "corr_gibraltar",
                "name": "Gibraltar Strait",
                "lat": 35.97,
                "lng": -5.6,
                "region": "Spain / Morocco",
                "daily_volume_bpd": 1700000,
                "share_of_india_imports_pct": 36.2,
                "base_risk": 22.0,
                "importance": "Gateway between Atlantic and Mediterranean shipping routes"
        },
        {
                "_id": "corr_dover",
                "name": "English Channel / Dover Strait",
                "lat": 51.0,
                "lng": 1.5,
                "region": "United Kingdom / France",
                "daily_volume_bpd": 35000,
                "share_of_india_imports_pct": 0.7,
                "base_risk": 20.0,
                "importance": "One of the world's busiest commercial shipping corridors"
        },
        {
                "_id": "corr_sunda",
                "name": "Sunda Strait",
                "lat": -5.95,
                "lng": 105.9,
                "region": "Indonesia",
                "daily_volume_bpd": 0,
                "share_of_india_imports_pct": 0.0,
                "base_risk": 25.0,
                "importance": "Alternative route to the Strait of Malacca"
        },
        {
                "_id": "corr_lombok",
                "name": "Lombok Strait",
                "lat": -8.5,
                "lng": 115.75,
                "region": "Indonesia",
                "daily_volume_bpd": 0,
                "share_of_india_imports_pct": 0.0,
                "base_risk": 24.0,
                "importance": "Deep-water alternative to Malacca for large vessels"
        },
        {
                "_id": "corr_makassar",
                "name": "Makassar Strait",
                "lat": -1.5,
                "lng": 117.5,
                "region": "Indonesia",
                "daily_volume_bpd": 0,
                "share_of_india_imports_pct": 0.0,
                "base_risk": 24.0,
                "importance": "Major Indonesian archipelago shipping corridor"
        },
        {
                "_id": "corr_cape",
                "name": "Cape of Good Hope",
                "lat": -34.3587,
                "lng": 18.4741,
                "region": "South Africa",
                "daily_volume_bpd": 945000,
                "share_of_india_imports_pct": 20.1,
                "base_risk": 20.0,
                "importance": "Major alternative route bypassing Suez and Bab el-Mandeb"
        },
        {
                "_id": "corr_cape_agulhas",
                "name": "Cape Agulhas",
                "lat": -34.8333,
                "lng": 20.0,
                "region": "South Africa",
                "daily_volume_bpd": 945000,
                "share_of_india_imports_pct": 20.1,
                "base_risk": 20.0,
                "importance": "Southern Africa shipping route"
        },
        {
                "_id": "corr_kiel",
                "name": "Kiel Canal",
                "lat": 53.95,
                "lng": 9.35,
                "region": "Germany",
                "daily_volume_bpd": 0,
                "share_of_india_imports_pct": 0.0,
                "base_risk": 25.0,
                "importance": "Major shortcut between North Sea and Baltic shipping"
        },
        {
                "_id": "corr_mozambique",
                "name": "Mozambique Channel",
                "lat": -17.0,
                "lng": 41.0,
                "region": "East Africa",
                "daily_volume_bpd": 0,
                "share_of_india_imports_pct": 0.0,
                "base_risk": 22.0,
                "importance": "Major Indian Ocean energy and commercial shipping route"
        },
        {
                "_id": "corr_taiwan",
                "name": "Taiwan Strait",
                "lat": 24.0,
                "lng": 119.5,
                "region": "East Asia",
                "daily_volume_bpd": 0,
                "share_of_india_imports_pct": 0.0,
                "base_risk": 48.0,
                "importance": "Major East Asian container and energy shipping corridor"
        },
        {
                "_id": "corr_tsushima",
                "name": "Tsushima Strait",
                "lat": 34.5,
                "lng": 129.5,
                "region": "Japan / Korea",
                "daily_volume_bpd": 0,
                "share_of_india_imports_pct": 0.0,
                "base_risk": 28.0,
                "importance": "Major Northeast Asian shipping route"
        },
        {
                "_id": "corr_korea",
                "name": "Korea Strait",
                "lat": 34.0,
                "lng": 129.0,
                "region": "Korea / Japan",
                "daily_volume_bpd": 0,
                "share_of_india_imports_pct": 0.0,
                "base_risk": 28.0,
                "importance": "Major Northeast Asian maritime corridor"
        },
        {
                "_id": "corr_tsugaru",
                "name": "Tsugaru Strait",
                "lat": 41.5,
                "lng": 140.5,
                "region": "Japan",
                "daily_volume_bpd": 0,
                "share_of_india_imports_pct": 0.0,
                "base_risk": 25.0,
                "importance": "Important Pacific-Japan Sea shipping route"
        },
        {
                "_id": "corr_bering",
                "name": "Bering Strait",
                "lat": 65.9,
                "lng": -168.95,
                "region": "Russia / United States",
                "daily_volume_bpd": 0,
                "share_of_india_imports_pct": 0.0,
                "base_risk": 20.0,
                "importance": "Strategic Arctic-Pacific gateway"
        },
        {
                "_id": "corr_magellan",
                "name": "Strait of Magellan",
                "lat": -53.5,
                "lng": -70.5,
                "region": "Chile",
                "daily_volume_bpd": 0,
                "share_of_india_imports_pct": 0.0,
                "base_risk": 22.0,
                "importance": "Alternative South American inter-ocean route"
        },
        {
                "_id": "corr_capehorn",
                "name": "Cape Horn",
                "lat": -55.98,
                "lng": -67.27,
                "region": "Chile",
                "daily_volume_bpd": 945000,
                "share_of_india_imports_pct": 20.1,
                "base_risk": 24.0,
                "importance": "Major southern alternative to Panama for certain vessels"
        }
]
    routes = [
        {
                "_id": "route_001",
                "from_node": "sup_russia",
                "to_node": "port_mundra",
                "corridor": "Danish Straits + Gibraltar Strait + Suez Canal + Bab el-Mandeb",
                "corridor_id": "corr_danish",
                "corridors": [
                        "corr_danish",
                        "corr_gibraltar",
                        "corr_suez",
                        "corr_babelmandeb"
                ],
                "capacity_bpd": 715000,
                "current_flow_bpd": 550000,
                "distance_km": 25966,
                "lead_time_days": 43,
                "transport_cost_usd_bbl": 12.39,
                "risk_base": 72.6,
                "status": "active",
                "waypoints": [
                        [
                                60.5937,
                                28.5013
                        ],
                        [
                                60.1798,
                                27.8998
                        ],
                        [
                                59.9523,
                                27.1252
                        ],
                        [
                                59.9715,
                                26.2408
                        ],
                        [
                                59.8,
                                24.7
                        ],
                        [
                                59.7016,
                                24.0114
                        ],
                        [
                                59.5,
                                22.6
                        ],
                        [
                                58.2,
                                20.6
                        ],
                        [
                                56.645,
                                18.1185
                        ],
                        [
                                56.4,
                                17
                        ],
                        [
                                55.9546,
                                16.21
                        ],
                        [
                                55.7271,
                                15.8066
                        ],
                        [
                                55.229,
                                14.3747
                        ],
                        [
                                55.2402,
                                13.8361
                        ],
                        [
                                55.2528,
                                13.2298
                        ],
                        [
                                55.2581,
                                12.9749
                        ],
                        [
                                55.3056,
                                12.6826
                        ],
                        [
                                55.5146,
                                12.7002
                        ],
                        [
                                55.9,
                                12.75
                        ],
                        [
                                56.0639,
                                12.6297
                        ],
                        [
                                56.3374,
                                12.4091
                        ],
                        [
                                56.3374,
                                12.4091
                        ],
                        [
                                56.9053,
                                11.9886
                        ],
                        [
                                57.7,
                                11.4
                        ],
                        [
                                57.8,
                                10.7333
                        ],
                        [
                                57.5999,
                                9.9527
                        ],
                        [
                                57.406,
                                8.9354
                        ],
                        [
                                56.8217,
                                7.9836
                        ],
                        [
                                56.6708,
                                7.7379
                        ],
                        [
                                55.8083,
                                6.8374
                        ],
                        [
                                55.4622,
                                6.476
                        ],
                        [
                                54.7649,
                                5.7953
                        ],
                        [
                                54.1261,
                                5.3432
                        ],
                        [
                                53.5,
                                4.9
                        ],
                        [
                                52.7001,
                                3.9002
                        ],
                        [
                                52.2419,
                                3.3274
                        ],
                        [
                                52.0155,
                                3.0444
                        ],
                        [
                                51.9,
                                2.9
                        ],
                        [
                                51.6089,
                                2.3601
                        ],
                        [
                                51.2359,
                                1.869
                        ],
                        [
                                51.0724,
                                1.6485
                        ],
                        [
                                50.9611,
                                1.4983
                        ],
                        [
                                50.8,
                                1.3
                        ],
                        [
                                50.7653,
                                1.1939
                        ],
                        [
                                50.5034,
                                0.3929
                        ],
                        [
                                50.2627,
                                -0.3434
                        ],
                        [
                                50.1965,
                                -0.546
                        ],
                        [
                                50.1555,
                                -0.6715
                        ],
                        [
                                49.95,
                                -1.3
                        ],
                        [
                                49.8951,
                                -1.4798
                        ],
                        [
                                49.8382,
                                -1.6657
                        ],
                        [
                                49.7564,
                                -1.9337
                        ],
                        [
                                49.7386,
                                -1.992
                        ],
                        [
                                49.6164,
                                -2.3919
                        ],
                        [
                                49.3704,
                                -3.197
                        ],
                        [
                                49.1292,
                                -3.9862
                        ],
                        [
                                49.1157,
                                -4.0304
                        ],
                        [
                                49.0424,
                                -4.2705
                        ],
                        [
                                48.7999,
                                -5.064
                        ],
                        [
                                48.6667,
                                -5.5
                        ],
                        [
                                47.3401,
                                -6.6989
                        ],
                        [
                                45.6688,
                                -7.955
                        ],
                        [
                                44.9348,
                                -8.4958
                        ],
                        [
                                43.9249,
                                -9.0199
                        ],
                        [
                                43.6885,
                                -9.1426
                        ],
                        [
                                43,
                                -9.5
                        ],
                        [
                                40.7798,
                                -9.9844
                        ],
                        [
                                38.5,
                                -9.6
                        ],
                        [
                                37.7816,
                                -9.4521
                        ],
                        [
                                36.8,
                                -9.25
                        ],
                        [
                                36.5497,
                                -8.2195
                        ],
                        [
                                36.3191,
                                -7.2697
                        ],
                        [
                                35.95,
                                -5.75
                        ],
                        [
                                35.9688,
                                -5.3549
                        ],
                        [
                                35.9729,
                                -5.2694
                        ],
                        [
                                36,
                                -4.7
                        ],
                        [
                                36.1565,
                                -3.683
                        ],
                        [
                                36.2209,
                                -3.2642
                        ],
                        [
                                36.3245,
                                -2.5907
                        ],
                        [
                                36.3777,
                                -2.2448
                        ],
                        [
                                36.4732,
                                -1.6244
                        ],
                        [
                                36.6667,
                                -0.3667
                        ],
                        [
                                37.2,
                                3.1
                        ],
                        [
                                37.4,
                                7.5
                        ],
                        [
                                37.4821,
                                10.373
                        ],
                        [
                                37.5,
                                11
                        ],
                        [
                                37.4549,
                                11.1722
                        ],
                        [
                                37.2832,
                                11.8278
                        ],
                        [
                                37.2155,
                                12.0863
                        ],
                        [
                                37.2091,
                                12.1106
                        ],
                        [
                                36.9071,
                                13.2638
                        ],
                        [
                                36.4,
                                15.2
                        ],
                        [
                                36.0869,
                                16.7266
                        ],
                        [
                                35.8457,
                                17.9021
                        ],
                        [
                                35.1267,
                                21.4074
                        ],
                        [
                                34.8,
                                23
                        ],
                        [
                                34.1874,
                                24.9267
                        ],
                        [
                                34.0119,
                                25.4787
                        ],
                        [
                                33.7488,
                                26.3064
                        ],
                        [
                                33.2196,
                                27.9275
                        ],
                        [
                                33.1158,
                                28.2124
                        ],
                        [
                                32.8634,
                                28.9055
                        ],
                        [
                                32.3161,
                                30.4084
                        ],
                        [
                                31.7,
                                32.1
                        ],
                        [
                                31.3364,
                                32.3599
                        ],
                        [
                                31.1029,
                                32.3101
                        ],
                        [
                                30.3184,
                                32.3822
                        ],
                        [
                                30.214,
                                32.558
                        ],
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                14.1436,
                                49.5581
                        ],
                        [
                                16.2,
                                54.2
                        ],
                        [
                                17.3839,
                                56.876
                        ],
                        [
                                18.7425,
                                58.1918
                        ],
                        [
                                20,
                                59
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                22.8425,
                                64.447
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_002",
                "from_node": "sup_russia",
                "to_node": "port_paradip",
                "corridor": "Danish Straits + Gibraltar Strait + Suez Canal + Bab el-Mandeb",
                "corridor_id": "corr_danish",
                "corridors": [
                        "corr_danish",
                        "corr_gibraltar",
                        "corr_suez",
                        "corr_babelmandeb"
                ],
                "capacity_bpd": 585000,
                "current_flow_bpd": 450000,
                "distance_km": 31346,
                "lead_time_days": 52,
                "transport_cost_usd_bbl": 14.54,
                "risk_base": 75.9,
                "status": "active",
                "waypoints": [
                        [
                                60.5937,
                                28.5013
                        ],
                        [
                                60.1798,
                                27.8998
                        ],
                        [
                                59.9523,
                                27.1252
                        ],
                        [
                                59.9715,
                                26.2408
                        ],
                        [
                                59.8,
                                24.7
                        ],
                        [
                                59.7016,
                                24.0114
                        ],
                        [
                                59.5,
                                22.6
                        ],
                        [
                                58.2,
                                20.6
                        ],
                        [
                                56.645,
                                18.1185
                        ],
                        [
                                56.4,
                                17
                        ],
                        [
                                55.9546,
                                16.21
                        ],
                        [
                                55.7271,
                                15.8066
                        ],
                        [
                                55.229,
                                14.3747
                        ],
                        [
                                55.2402,
                                13.8361
                        ],
                        [
                                55.2528,
                                13.2298
                        ],
                        [
                                55.2581,
                                12.9749
                        ],
                        [
                                55.3056,
                                12.6826
                        ],
                        [
                                55.5146,
                                12.7002
                        ],
                        [
                                55.9,
                                12.75
                        ],
                        [
                                56.0639,
                                12.6297
                        ],
                        [
                                56.3374,
                                12.4091
                        ],
                        [
                                56.3374,
                                12.4091
                        ],
                        [
                                56.9053,
                                11.9886
                        ],
                        [
                                57.7,
                                11.4
                        ],
                        [
                                57.8,
                                10.7333
                        ],
                        [
                                57.5999,
                                9.9527
                        ],
                        [
                                57.406,
                                8.9354
                        ],
                        [
                                56.8217,
                                7.9836
                        ],
                        [
                                56.6708,
                                7.7379
                        ],
                        [
                                55.8083,
                                6.8374
                        ],
                        [
                                55.4622,
                                6.476
                        ],
                        [
                                54.7649,
                                5.7953
                        ],
                        [
                                54.1261,
                                5.3432
                        ],
                        [
                                53.5,
                                4.9
                        ],
                        [
                                52.7001,
                                3.9002
                        ],
                        [
                                52.2419,
                                3.3274
                        ],
                        [
                                52.0155,
                                3.0444
                        ],
                        [
                                51.9,
                                2.9
                        ],
                        [
                                51.6089,
                                2.3601
                        ],
                        [
                                51.2359,
                                1.869
                        ],
                        [
                                51.0724,
                                1.6485
                        ],
                        [
                                50.9611,
                                1.4983
                        ],
                        [
                                50.8,
                                1.3
                        ],
                        [
                                50.7653,
                                1.1939
                        ],
                        [
                                50.5034,
                                0.3929
                        ],
                        [
                                50.2627,
                                -0.3434
                        ],
                        [
                                50.1965,
                                -0.546
                        ],
                        [
                                50.1555,
                                -0.6715
                        ],
                        [
                                49.95,
                                -1.3
                        ],
                        [
                                49.8951,
                                -1.4798
                        ],
                        [
                                49.8382,
                                -1.6657
                        ],
                        [
                                49.7564,
                                -1.9337
                        ],
                        [
                                49.7386,
                                -1.992
                        ],
                        [
                                49.6164,
                                -2.3919
                        ],
                        [
                                49.3704,
                                -3.197
                        ],
                        [
                                49.1292,
                                -3.9862
                        ],
                        [
                                49.1157,
                                -4.0304
                        ],
                        [
                                49.0424,
                                -4.2705
                        ],
                        [
                                48.7999,
                                -5.064
                        ],
                        [
                                48.6667,
                                -5.5
                        ],
                        [
                                47.3401,
                                -6.6989
                        ],
                        [
                                45.6688,
                                -7.955
                        ],
                        [
                                44.9348,
                                -8.4958
                        ],
                        [
                                43.9249,
                                -9.0199
                        ],
                        [
                                43.6885,
                                -9.1426
                        ],
                        [
                                43,
                                -9.5
                        ],
                        [
                                40.7798,
                                -9.9844
                        ],
                        [
                                38.5,
                                -9.6
                        ],
                        [
                                37.7816,
                                -9.4521
                        ],
                        [
                                36.8,
                                -9.25
                        ],
                        [
                                36.5497,
                                -8.2195
                        ],
                        [
                                36.3191,
                                -7.2697
                        ],
                        [
                                35.95,
                                -5.75
                        ],
                        [
                                35.9688,
                                -5.3549
                        ],
                        [
                                35.9729,
                                -5.2694
                        ],
                        [
                                36,
                                -4.7
                        ],
                        [
                                36.1565,
                                -3.683
                        ],
                        [
                                36.2209,
                                -3.2642
                        ],
                        [
                                36.3245,
                                -2.5907
                        ],
                        [
                                36.3777,
                                -2.2448
                        ],
                        [
                                36.4732,
                                -1.6244
                        ],
                        [
                                36.6667,
                                -0.3667
                        ],
                        [
                                37.2,
                                3.1
                        ],
                        [
                                37.4,
                                7.5
                        ],
                        [
                                37.4821,
                                10.373
                        ],
                        [
                                37.5,
                                11
                        ],
                        [
                                37.4549,
                                11.1722
                        ],
                        [
                                37.2832,
                                11.8278
                        ],
                        [
                                37.2155,
                                12.0863
                        ],
                        [
                                37.2091,
                                12.1106
                        ],
                        [
                                36.9071,
                                13.2638
                        ],
                        [
                                36.4,
                                15.2
                        ],
                        [
                                36.0869,
                                16.7266
                        ],
                        [
                                35.8457,
                                17.9021
                        ],
                        [
                                35.1267,
                                21.4074
                        ],
                        [
                                34.8,
                                23
                        ],
                        [
                                34.1874,
                                24.9267
                        ],
                        [
                                34.0119,
                                25.4787
                        ],
                        [
                                33.7488,
                                26.3064
                        ],
                        [
                                33.2196,
                                27.9275
                        ],
                        [
                                33.1158,
                                28.2124
                        ],
                        [
                                32.8634,
                                28.9055
                        ],
                        [
                                32.3161,
                                30.4084
                        ],
                        [
                                31.7,
                                32.1
                        ],
                        [
                                31.3364,
                                32.3599
                        ],
                        [
                                31.1029,
                                32.3101
                        ],
                        [
                                30.3184,
                                32.3822
                        ],
                        [
                                30.214,
                                32.558
                        ],
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                12.884,
                                50.8561
                        ],
                        [
                                13.3,
                                53.6189
                        ],
                        [
                                12.7475,
                                55.0415
                        ],
                        [
                                11.0835,
                                59.894
                        ],
                        [
                                10.867,
                                60.8257
                        ],
                        [
                                10.5802,
                                62.0601
                        ],
                        [
                                10.0316,
                                64.3032
                        ],
                        [
                                9.9348,
                                64.6989
                        ],
                        [
                                9.8629,
                                64.9928
                        ],
                        [
                                9.6889,
                                65.7044
                        ],
                        [
                                8.8816,
                                68.859
                        ],
                        [
                                8.7613,
                                69.3291
                        ],
                        [
                                8.6701,
                                69.6717
                        ],
                        [
                                8.5827,
                                69.9999
                        ],
                        [
                                8.3651,
                                70.8174
                        ],
                        [
                                6.9668,
                                75.9668
                        ],
                        [
                                6.3878,
                                78.019
                        ],
                        [
                                5.8,
                                80.1
                        ],
                        [
                                5.9,
                                81.9
                        ],
                        [
                                7.25,
                                82.25
                        ],
                        [
                                10.7006,
                                83.6282
                        ],
                        [
                                11.5565,
                                83.9786
                        ],
                        [
                                14.1441,
                                85.038
                        ],
                        [
                                14.4222,
                                85.1557
                        ],
                        [
                                15.7917,
                                85.7351
                        ],
                        [
                                17.5782,
                                86.491
                        ],
                        [
                                21,
                                88
                        ]
                ]
        },
        {
                "_id": "route_003",
                "from_node": "sup_russia",
                "to_node": "port_vizag",
                "corridor": "Strait of Malacca",
                "corridor_id": "corr_malacca",
                "corridors": [
                        "corr_malacca"
                ],
                "capacity_bpd": 195000,
                "current_flow_bpd": 150000,
                "distance_km": 30472,
                "lead_time_days": 51,
                "transport_cost_usd_bbl": 13.39,
                "risk_base": 38.8,
                "status": "active",
                "waypoints": [
                        [
                                60.5937,
                                28.5013
                        ],
                        [
                                60.1798,
                                27.8998
                        ],
                        [
                                59.9523,
                                27.1252
                        ],
                        [
                                59.9715,
                                26.2408
                        ],
                        [
                                59.8,
                                24.7
                        ],
                        [
                                59.7016,
                                24.0114
                        ],
                        [
                                59.5,
                                22.6
                        ],
                        [
                                58.2,
                                20.6
                        ],
                        [
                                56.645,
                                18.1185
                        ],
                        [
                                56.4,
                                17
                        ],
                        [
                                55.9546,
                                16.21
                        ],
                        [
                                55.7271,
                                15.8066
                        ],
                        [
                                55.229,
                                14.3747
                        ],
                        [
                                55.2402,
                                13.8361
                        ],
                        [
                                55.2528,
                                13.2298
                        ],
                        [
                                55.2581,
                                12.9749
                        ],
                        [
                                55.3056,
                                12.6826
                        ],
                        [
                                55.5146,
                                12.7002
                        ],
                        [
                                55.9,
                                12.75
                        ],
                        [
                                56.0639,
                                12.6297
                        ],
                        [
                                56.3374,
                                12.4091
                        ],
                        [
                                56.3374,
                                12.4091
                        ],
                        [
                                56.9053,
                                11.9886
                        ],
                        [
                                57.7,
                                11.4
                        ],
                        [
                                57.8,
                                10.7333
                        ],
                        [
                                57.5999,
                                9.9527
                        ],
                        [
                                57.406,
                                8.9354
                        ],
                        [
                                56.8217,
                                7.9836
                        ],
                        [
                                56.6708,
                                7.7379
                        ],
                        [
                                55.8083,
                                6.8374
                        ],
                        [
                                55.4622,
                                6.476
                        ],
                        [
                                54.7649,
                                5.7953
                        ],
                        [
                                54.1261,
                                5.3432
                        ],
                        [
                                53.5,
                                4.9
                        ],
                        [
                                52.7001,
                                3.9002
                        ],
                        [
                                52.2419,
                                3.3274
                        ],
                        [
                                52.0155,
                                3.0444
                        ],
                        [
                                51.9,
                                2.9
                        ],
                        [
                                51.6089,
                                2.3601
                        ],
                        [
                                51.2359,
                                1.869
                        ],
                        [
                                51.0724,
                                1.6485
                        ],
                        [
                                50.9611,
                                1.4983
                        ],
                        [
                                50.8,
                                1.3
                        ],
                        [
                                50.7653,
                                1.1939
                        ],
                        [
                                50.5034,
                                0.3929
                        ],
                        [
                                50.2627,
                                -0.3434
                        ],
                        [
                                50.1965,
                                -0.546
                        ],
                        [
                                50.1555,
                                -0.6715
                        ],
                        [
                                49.95,
                                -1.3
                        ],
                        [
                                49.8951,
                                -1.4798
                        ],
                        [
                                49.8382,
                                -1.6657
                        ],
                        [
                                49.7564,
                                -1.9337
                        ],
                        [
                                49.7386,
                                -1.992
                        ],
                        [
                                49.6164,
                                -2.3919
                        ],
                        [
                                49.3704,
                                -3.197
                        ],
                        [
                                49.1292,
                                -3.9862
                        ],
                        [
                                49.1157,
                                -4.0304
                        ],
                        [
                                49.0424,
                                -4.2705
                        ],
                        [
                                48.7999,
                                -5.064
                        ],
                        [
                                48.6667,
                                -5.5
                        ],
                        [
                                47.3401,
                                -6.6989
                        ],
                        [
                                45.6688,
                                -7.955
                        ],
                        [
                                44.9348,
                                -8.4958
                        ],
                        [
                                43.9249,
                                -9.0199
                        ],
                        [
                                43.6885,
                                -9.1426
                        ],
                        [
                                43,
                                -9.5
                        ],
                        [
                                40.7798,
                                -9.9844
                        ],
                        [
                                38.5,
                                -9.6
                        ],
                        [
                                37.7816,
                                -9.4521
                        ],
                        [
                                36.8,
                                -9.25
                        ],
                        [
                                36.5497,
                                -8.2195
                        ],
                        [
                                36.3191,
                                -7.2697
                        ],
                        [
                                35.95,
                                -5.75
                        ],
                        [
                                35.9688,
                                -5.3549
                        ],
                        [
                                35.9729,
                                -5.2694
                        ],
                        [
                                36,
                                -4.7
                        ],
                        [
                                36.1565,
                                -3.683
                        ],
                        [
                                36.2209,
                                -3.2642
                        ],
                        [
                                36.3245,
                                -2.5907
                        ],
                        [
                                36.3777,
                                -2.2448
                        ],
                        [
                                36.4732,
                                -1.6244
                        ],
                        [
                                36.6667,
                                -0.3667
                        ],
                        [
                                37.2,
                                3.1
                        ],
                        [
                                37.4,
                                7.5
                        ],
                        [
                                37.4821,
                                10.373
                        ],
                        [
                                37.5,
                                11
                        ],
                        [
                                37.4549,
                                11.1722
                        ],
                        [
                                37.2832,
                                11.8278
                        ],
                        [
                                37.2155,
                                12.0863
                        ],
                        [
                                37.2091,
                                12.1106
                        ],
                        [
                                36.9071,
                                13.2638
                        ],
                        [
                                36.4,
                                15.2
                        ],
                        [
                                36.0869,
                                16.7266
                        ],
                        [
                                35.8457,
                                17.9021
                        ],
                        [
                                35.1267,
                                21.4074
                        ],
                        [
                                34.8,
                                23
                        ],
                        [
                                34.1874,
                                24.9267
                        ],
                        [
                                34.0119,
                                25.4787
                        ],
                        [
                                33.7488,
                                26.3064
                        ],
                        [
                                33.2196,
                                27.9275
                        ],
                        [
                                33.1158,
                                28.2124
                        ],
                        [
                                32.8634,
                                28.9055
                        ],
                        [
                                32.3161,
                                30.4084
                        ],
                        [
                                31.7,
                                32.1
                        ],
                        [
                                31.3364,
                                32.3599
                        ],
                        [
                                31.1029,
                                32.3101
                        ],
                        [
                                30.3184,
                                32.3822
                        ],
                        [
                                30.214,
                                32.558
                        ],
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                12.884,
                                50.8561
                        ],
                        [
                                13.3,
                                53.6189
                        ],
                        [
                                12.7475,
                                55.0415
                        ],
                        [
                                11.0835,
                                59.894
                        ],
                        [
                                10.867,
                                60.8257
                        ],
                        [
                                10.5802,
                                62.0601
                        ],
                        [
                                10.0316,
                                64.3032
                        ],
                        [
                                9.9348,
                                64.6989
                        ],
                        [
                                9.8629,
                                64.9928
                        ],
                        [
                                9.6889,
                                65.7044
                        ],
                        [
                                8.8816,
                                68.859
                        ],
                        [
                                8.7613,
                                69.3291
                        ],
                        [
                                8.6701,
                                69.6717
                        ],
                        [
                                8.5827,
                                69.9999
                        ],
                        [
                                8.3651,
                                70.8174
                        ],
                        [
                                6.9668,
                                75.9668
                        ],
                        [
                                6.3878,
                                78.019
                        ],
                        [
                                5.8,
                                80.1
                        ],
                        [
                                5.9,
                                81.9
                        ],
                        [
                                7.25,
                                82.25
                        ],
                        [
                                12.0325,
                                82.9983
                        ],
                        [
                                15.2718,
                                83.4593
                        ],
                        [
                                17.414,
                                83.6565
                        ],
                        [
                                17.6221,
                                83.3898
                        ]
                ]
        },
        {
                "_id": "route_004",
                "from_node": "sup_russia",
                "to_node": "port_kochi",
                "corridor": "Danish Straits + Gibraltar Strait + Suez Canal + Bab el-Mandeb",
                "corridor_id": "corr_danish",
                "corridors": [
                        "corr_danish",
                        "corr_gibraltar",
                        "corr_suez",
                        "corr_babelmandeb"
                ],
                "capacity_bpd": 325000,
                "current_flow_bpd": 250000,
                "distance_km": 26716,
                "lead_time_days": 45,
                "transport_cost_usd_bbl": 12.69,
                "risk_base": 72.6,
                "status": "active",
                "waypoints": [
                        [
                                60.5937,
                                28.5013
                        ],
                        [
                                60.1798,
                                27.8998
                        ],
                        [
                                59.9523,
                                27.1252
                        ],
                        [
                                59.9715,
                                26.2408
                        ],
                        [
                                59.8,
                                24.7
                        ],
                        [
                                59.7016,
                                24.0114
                        ],
                        [
                                59.5,
                                22.6
                        ],
                        [
                                58.2,
                                20.6
                        ],
                        [
                                56.645,
                                18.1185
                        ],
                        [
                                56.4,
                                17
                        ],
                        [
                                55.9546,
                                16.21
                        ],
                        [
                                55.7271,
                                15.8066
                        ],
                        [
                                55.229,
                                14.3747
                        ],
                        [
                                55.2402,
                                13.8361
                        ],
                        [
                                55.2528,
                                13.2298
                        ],
                        [
                                55.2581,
                                12.9749
                        ],
                        [
                                55.3056,
                                12.6826
                        ],
                        [
                                55.5146,
                                12.7002
                        ],
                        [
                                55.9,
                                12.75
                        ],
                        [
                                56.0639,
                                12.6297
                        ],
                        [
                                56.3374,
                                12.4091
                        ],
                        [
                                56.3374,
                                12.4091
                        ],
                        [
                                56.9053,
                                11.9886
                        ],
                        [
                                57.7,
                                11.4
                        ],
                        [
                                57.8,
                                10.7333
                        ],
                        [
                                57.5999,
                                9.9527
                        ],
                        [
                                57.406,
                                8.9354
                        ],
                        [
                                56.8217,
                                7.9836
                        ],
                        [
                                56.6708,
                                7.7379
                        ],
                        [
                                55.8083,
                                6.8374
                        ],
                        [
                                55.4622,
                                6.476
                        ],
                        [
                                54.7649,
                                5.7953
                        ],
                        [
                                54.1261,
                                5.3432
                        ],
                        [
                                53.5,
                                4.9
                        ],
                        [
                                52.7001,
                                3.9002
                        ],
                        [
                                52.2419,
                                3.3274
                        ],
                        [
                                52.0155,
                                3.0444
                        ],
                        [
                                51.9,
                                2.9
                        ],
                        [
                                51.6089,
                                2.3601
                        ],
                        [
                                51.2359,
                                1.869
                        ],
                        [
                                51.0724,
                                1.6485
                        ],
                        [
                                50.9611,
                                1.4983
                        ],
                        [
                                50.8,
                                1.3
                        ],
                        [
                                50.7653,
                                1.1939
                        ],
                        [
                                50.5034,
                                0.3929
                        ],
                        [
                                50.2627,
                                -0.3434
                        ],
                        [
                                50.1965,
                                -0.546
                        ],
                        [
                                50.1555,
                                -0.6715
                        ],
                        [
                                49.95,
                                -1.3
                        ],
                        [
                                49.8951,
                                -1.4798
                        ],
                        [
                                49.8382,
                                -1.6657
                        ],
                        [
                                49.7564,
                                -1.9337
                        ],
                        [
                                49.7386,
                                -1.992
                        ],
                        [
                                49.6164,
                                -2.3919
                        ],
                        [
                                49.3704,
                                -3.197
                        ],
                        [
                                49.1292,
                                -3.9862
                        ],
                        [
                                49.1157,
                                -4.0304
                        ],
                        [
                                49.0424,
                                -4.2705
                        ],
                        [
                                48.7999,
                                -5.064
                        ],
                        [
                                48.6667,
                                -5.5
                        ],
                        [
                                47.3401,
                                -6.6989
                        ],
                        [
                                45.6688,
                                -7.955
                        ],
                        [
                                44.9348,
                                -8.4958
                        ],
                        [
                                43.9249,
                                -9.0199
                        ],
                        [
                                43.6885,
                                -9.1426
                        ],
                        [
                                43,
                                -9.5
                        ],
                        [
                                40.7798,
                                -9.9844
                        ],
                        [
                                38.5,
                                -9.6
                        ],
                        [
                                37.7816,
                                -9.4521
                        ],
                        [
                                36.8,
                                -9.25
                        ],
                        [
                                36.5497,
                                -8.2195
                        ],
                        [
                                36.3191,
                                -7.2697
                        ],
                        [
                                35.95,
                                -5.75
                        ],
                        [
                                35.9688,
                                -5.3549
                        ],
                        [
                                35.9729,
                                -5.2694
                        ],
                        [
                                36,
                                -4.7
                        ],
                        [
                                36.1565,
                                -3.683
                        ],
                        [
                                36.2209,
                                -3.2642
                        ],
                        [
                                36.3245,
                                -2.5907
                        ],
                        [
                                36.3777,
                                -2.2448
                        ],
                        [
                                36.4732,
                                -1.6244
                        ],
                        [
                                36.6667,
                                -0.3667
                        ],
                        [
                                37.2,
                                3.1
                        ],
                        [
                                37.4,
                                7.5
                        ],
                        [
                                37.4821,
                                10.373
                        ],
                        [
                                37.5,
                                11
                        ],
                        [
                                37.4549,
                                11.1722
                        ],
                        [
                                37.2832,
                                11.8278
                        ],
                        [
                                37.2155,
                                12.0863
                        ],
                        [
                                37.2091,
                                12.1106
                        ],
                        [
                                36.9071,
                                13.2638
                        ],
                        [
                                36.4,
                                15.2
                        ],
                        [
                                36.0869,
                                16.7266
                        ],
                        [
                                35.8457,
                                17.9021
                        ],
                        [
                                35.1267,
                                21.4074
                        ],
                        [
                                34.8,
                                23
                        ],
                        [
                                34.1874,
                                24.9267
                        ],
                        [
                                34.0119,
                                25.4787
                        ],
                        [
                                33.7488,
                                26.3064
                        ],
                        [
                                33.2196,
                                27.9275
                        ],
                        [
                                33.1158,
                                28.2124
                        ],
                        [
                                32.8634,
                                28.9055
                        ],
                        [
                                32.3161,
                                30.4084
                        ],
                        [
                                31.7,
                                32.1
                        ],
                        [
                                31.3364,
                                32.3599
                        ],
                        [
                                31.1029,
                                32.3101
                        ],
                        [
                                30.3184,
                                32.3822
                        ],
                        [
                                30.214,
                                32.558
                        ],
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                12.884,
                                50.8561
                        ],
                        [
                                13.3,
                                53.6189
                        ],
                        [
                                12.7475,
                                55.0415
                        ],
                        [
                                11.0835,
                                59.894
                        ],
                        [
                                10.867,
                                60.8257
                        ],
                        [
                                10.5802,
                                62.0601
                        ],
                        [
                                10.0316,
                                64.3032
                        ],
                        [
                                10.0345,
                                64.6969
                        ],
                        [
                                10.0367,
                                65.0002
                        ],
                        [
                                10.0358,
                                65.1268
                        ],
                        [
                                10,
                                70
                        ],
                        [
                                9.7,
                                75.3
                        ],
                        [
                                9.8769,
                                76.1957
                        ]
                ]
        },
        {
                "_id": "route_005",
                "from_node": "sup_russia",
                "to_node": "port_vadinar",
                "corridor": "Danish Straits + Gibraltar Strait + Suez Canal + Bab el-Mandeb",
                "corridor_id": "corr_danish",
                "corridors": [
                        "corr_danish",
                        "corr_gibraltar",
                        "corr_suez",
                        "corr_babelmandeb"
                ],
                "capacity_bpd": 390000,
                "current_flow_bpd": 300000,
                "distance_km": 25966,
                "lead_time_days": 43,
                "transport_cost_usd_bbl": 12.39,
                "risk_base": 72.6,
                "status": "active",
                "waypoints": [
                        [
                                60.5937,
                                28.5013
                        ],
                        [
                                60.1798,
                                27.8998
                        ],
                        [
                                59.9523,
                                27.1252
                        ],
                        [
                                59.9715,
                                26.2408
                        ],
                        [
                                59.8,
                                24.7
                        ],
                        [
                                59.7016,
                                24.0114
                        ],
                        [
                                59.5,
                                22.6
                        ],
                        [
                                58.2,
                                20.6
                        ],
                        [
                                56.645,
                                18.1185
                        ],
                        [
                                56.4,
                                17
                        ],
                        [
                                55.9546,
                                16.21
                        ],
                        [
                                55.7271,
                                15.8066
                        ],
                        [
                                55.229,
                                14.3747
                        ],
                        [
                                55.2402,
                                13.8361
                        ],
                        [
                                55.2528,
                                13.2298
                        ],
                        [
                                55.2581,
                                12.9749
                        ],
                        [
                                55.3056,
                                12.6826
                        ],
                        [
                                55.5146,
                                12.7002
                        ],
                        [
                                55.9,
                                12.75
                        ],
                        [
                                56.0639,
                                12.6297
                        ],
                        [
                                56.3374,
                                12.4091
                        ],
                        [
                                56.3374,
                                12.4091
                        ],
                        [
                                56.9053,
                                11.9886
                        ],
                        [
                                57.7,
                                11.4
                        ],
                        [
                                57.8,
                                10.7333
                        ],
                        [
                                57.5999,
                                9.9527
                        ],
                        [
                                57.406,
                                8.9354
                        ],
                        [
                                56.8217,
                                7.9836
                        ],
                        [
                                56.6708,
                                7.7379
                        ],
                        [
                                55.8083,
                                6.8374
                        ],
                        [
                                55.4622,
                                6.476
                        ],
                        [
                                54.7649,
                                5.7953
                        ],
                        [
                                54.1261,
                                5.3432
                        ],
                        [
                                53.5,
                                4.9
                        ],
                        [
                                52.7001,
                                3.9002
                        ],
                        [
                                52.2419,
                                3.3274
                        ],
                        [
                                52.0155,
                                3.0444
                        ],
                        [
                                51.9,
                                2.9
                        ],
                        [
                                51.6089,
                                2.3601
                        ],
                        [
                                51.2359,
                                1.869
                        ],
                        [
                                51.0724,
                                1.6485
                        ],
                        [
                                50.9611,
                                1.4983
                        ],
                        [
                                50.8,
                                1.3
                        ],
                        [
                                50.7653,
                                1.1939
                        ],
                        [
                                50.5034,
                                0.3929
                        ],
                        [
                                50.2627,
                                -0.3434
                        ],
                        [
                                50.1965,
                                -0.546
                        ],
                        [
                                50.1555,
                                -0.6715
                        ],
                        [
                                49.95,
                                -1.3
                        ],
                        [
                                49.8951,
                                -1.4798
                        ],
                        [
                                49.8382,
                                -1.6657
                        ],
                        [
                                49.7564,
                                -1.9337
                        ],
                        [
                                49.7386,
                                -1.992
                        ],
                        [
                                49.6164,
                                -2.3919
                        ],
                        [
                                49.3704,
                                -3.197
                        ],
                        [
                                49.1292,
                                -3.9862
                        ],
                        [
                                49.1157,
                                -4.0304
                        ],
                        [
                                49.0424,
                                -4.2705
                        ],
                        [
                                48.7999,
                                -5.064
                        ],
                        [
                                48.6667,
                                -5.5
                        ],
                        [
                                47.3401,
                                -6.6989
                        ],
                        [
                                45.6688,
                                -7.955
                        ],
                        [
                                44.9348,
                                -8.4958
                        ],
                        [
                                43.9249,
                                -9.0199
                        ],
                        [
                                43.6885,
                                -9.1426
                        ],
                        [
                                43,
                                -9.5
                        ],
                        [
                                40.7798,
                                -9.9844
                        ],
                        [
                                38.5,
                                -9.6
                        ],
                        [
                                37.7816,
                                -9.4521
                        ],
                        [
                                36.8,
                                -9.25
                        ],
                        [
                                36.5497,
                                -8.2195
                        ],
                        [
                                36.3191,
                                -7.2697
                        ],
                        [
                                35.95,
                                -5.75
                        ],
                        [
                                35.9688,
                                -5.3549
                        ],
                        [
                                35.9729,
                                -5.2694
                        ],
                        [
                                36,
                                -4.7
                        ],
                        [
                                36.1565,
                                -3.683
                        ],
                        [
                                36.2209,
                                -3.2642
                        ],
                        [
                                36.3245,
                                -2.5907
                        ],
                        [
                                36.3777,
                                -2.2448
                        ],
                        [
                                36.4732,
                                -1.6244
                        ],
                        [
                                36.6667,
                                -0.3667
                        ],
                        [
                                37.2,
                                3.1
                        ],
                        [
                                37.4,
                                7.5
                        ],
                        [
                                37.4821,
                                10.373
                        ],
                        [
                                37.5,
                                11
                        ],
                        [
                                37.4549,
                                11.1722
                        ],
                        [
                                37.2832,
                                11.8278
                        ],
                        [
                                37.2155,
                                12.0863
                        ],
                        [
                                37.2091,
                                12.1106
                        ],
                        [
                                36.9071,
                                13.2638
                        ],
                        [
                                36.4,
                                15.2
                        ],
                        [
                                36.0869,
                                16.7266
                        ],
                        [
                                35.8457,
                                17.9021
                        ],
                        [
                                35.1267,
                                21.4074
                        ],
                        [
                                34.8,
                                23
                        ],
                        [
                                34.1874,
                                24.9267
                        ],
                        [
                                34.0119,
                                25.4787
                        ],
                        [
                                33.7488,
                                26.3064
                        ],
                        [
                                33.2196,
                                27.9275
                        ],
                        [
                                33.1158,
                                28.2124
                        ],
                        [
                                32.8634,
                                28.9055
                        ],
                        [
                                32.3161,
                                30.4084
                        ],
                        [
                                31.7,
                                32.1
                        ],
                        [
                                31.3364,
                                32.3599
                        ],
                        [
                                31.1029,
                                32.3101
                        ],
                        [
                                30.3184,
                                32.3822
                        ],
                        [
                                30.214,
                                32.558
                        ],
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                14.1436,
                                49.5581
                        ],
                        [
                                16.2,
                                54.2
                        ],
                        [
                                17.3839,
                                56.876
                        ],
                        [
                                18.7425,
                                58.1918
                        ],
                        [
                                20,
                                59
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                22.8425,
                                64.447
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_006",
                "from_node": "sup_iraq",
                "to_node": "port_mundra",
                "corridor": "Strait of Hormuz",
                "corridor_id": "corr_hormuz",
                "corridors": [
                        "corr_hormuz"
                ],
                "capacity_bpd": 390000,
                "current_flow_bpd": 300000,
                "distance_km": 4442,
                "lead_time_days": 7,
                "transport_cost_usd_bbl": 2.98,
                "risk_base": 46.9,
                "status": "active",
                "waypoints": [
                        [
                                29.8055,
                                48.7931
                        ],
                        [
                                28.6,
                                50.1
                        ],
                        [
                                27.1816,
                                51.222
                        ],
                        [
                                26.5789,
                                53.3693
                        ],
                        [
                                26.1949,
                                54.3991
                        ],
                        [
                                26.1511,
                                55.0643
                        ],
                        [
                                26.1327,
                                55.345
                        ],
                        [
                                26.4411,
                                56.3434
                        ],
                        [
                                26.5111,
                                56.5472
                        ],
                        [
                                26.4221,
                                56.7631
                        ],
                        [
                                25.962,
                                56.9315
                        ],
                        [
                                25.5,
                                57.1
                        ],
                        [
                                24.6,
                                63.3
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_007",
                "from_node": "sup_iraq",
                "to_node": "port_vadinar",
                "corridor": "Strait of Hormuz",
                "corridor_id": "corr_hormuz",
                "corridors": [
                        "corr_hormuz"
                ],
                "capacity_bpd": 455000,
                "current_flow_bpd": 350000,
                "distance_km": 4442,
                "lead_time_days": 7,
                "transport_cost_usd_bbl": 2.98,
                "risk_base": 46.9,
                "status": "active",
                "waypoints": [
                        [
                                29.8055,
                                48.7931
                        ],
                        [
                                28.6,
                                50.1
                        ],
                        [
                                27.1816,
                                51.222
                        ],
                        [
                                26.5789,
                                53.3693
                        ],
                        [
                                26.1949,
                                54.3991
                        ],
                        [
                                26.1511,
                                55.0643
                        ],
                        [
                                26.1327,
                                55.345
                        ],
                        [
                                26.4411,
                                56.3434
                        ],
                        [
                                26.5111,
                                56.5472
                        ],
                        [
                                26.4221,
                                56.7631
                        ],
                        [
                                25.962,
                                56.9315
                        ],
                        [
                                25.5,
                                57.1
                        ],
                        [
                                24.6,
                                63.3
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_008",
                "from_node": "sup_iraq",
                "to_node": "port_kochi",
                "corridor": "Strait of Hormuz",
                "corridor_id": "corr_hormuz",
                "corridors": [
                        "corr_hormuz"
                ],
                "capacity_bpd": 195000,
                "current_flow_bpd": 150000,
                "distance_km": 7024,
                "lead_time_days": 12,
                "transport_cost_usd_bbl": 4.01,
                "risk_base": 49.0,
                "status": "active",
                "waypoints": [
                        [
                                29.8055,
                                48.7931
                        ],
                        [
                                28.6,
                                50.1
                        ],
                        [
                                27.1816,
                                51.222
                        ],
                        [
                                26.5789,
                                53.3693
                        ],
                        [
                                26.1949,
                                54.3991
                        ],
                        [
                                26.1511,
                                55.0643
                        ],
                        [
                                26.1327,
                                55.345
                        ],
                        [
                                26.4411,
                                56.3434
                        ],
                        [
                                26.5111,
                                56.5472
                        ],
                        [
                                26.4221,
                                56.7631
                        ],
                        [
                                25.962,
                                56.9315
                        ],
                        [
                                25.5,
                                57.1
                        ],
                        [
                                24,
                                59
                        ],
                        [
                                22.7,
                                60.4
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                20.0838,
                                64.5005
                        ],
                        [
                                19.4262,
                                64.9526
                        ],
                        [
                                17.5275,
                                66.2579
                        ],
                        [
                                16.9017,
                                66.6882
                        ],
                        [
                                15.7182,
                                67.6538
                        ],
                        [
                                14.6786,
                                68.8018
                        ],
                        [
                                13.7657,
                                69.9994
                        ],
                        [
                                9.7,
                                75.3
                        ],
                        [
                                9.8769,
                                76.1957
                        ]
                ]
        },
        {
                "_id": "route_009",
                "from_node": "sup_iraq",
                "to_node": "port_mangalore",
                "corridor": "Strait of Hormuz",
                "corridor_id": "corr_hormuz",
                "corridors": [
                        "corr_hormuz"
                ],
                "capacity_bpd": 195000,
                "current_flow_bpd": 150000,
                "distance_km": 6743,
                "lead_time_days": 11,
                "transport_cost_usd_bbl": 3.9,
                "risk_base": 48.6,
                "status": "active",
                "waypoints": [
                        [
                                29.8055,
                                48.7931
                        ],
                        [
                                28.6,
                                50.1
                        ],
                        [
                                27.1816,
                                51.222
                        ],
                        [
                                26.5789,
                                53.3693
                        ],
                        [
                                26.1949,
                                54.3991
                        ],
                        [
                                26.1511,
                                55.0643
                        ],
                        [
                                26.1327,
                                55.345
                        ],
                        [
                                26.4411,
                                56.3434
                        ],
                        [
                                26.5111,
                                56.5472
                        ],
                        [
                                26.4221,
                                56.7631
                        ],
                        [
                                25.962,
                                56.9315
                        ],
                        [
                                25.5,
                                57.1
                        ],
                        [
                                24,
                                59
                        ],
                        [
                                23.457,
                                61.5554
                        ],
                        [
                                22.8425,
                                64.447
                        ],
                        [
                                22.5708,
                                65.7258
                        ],
                        [
                                22.3,
                                67
                        ],
                        [
                                20.8093,
                                69.5925
                        ],
                        [
                                20,
                                70
                        ],
                        [
                                19,
                                72.4
                        ],
                        [
                                15.3,
                                73
                        ],
                        [
                                12.7734,
                                74.1335
                        ],
                        [
                                12.8172,
                                74.7784
                        ]
                ]
        },
        {
                "_id": "route_010",
                "from_node": "sup_saudi_arabia",
                "to_node": "port_mundra",
                "corridor": "Strait of Hormuz",
                "corridor_id": "corr_hormuz",
                "corridors": [
                        "corr_hormuz"
                ],
                "capacity_bpd": 325000,
                "current_flow_bpd": 250000,
                "distance_km": 3965,
                "lead_time_days": 7,
                "transport_cost_usd_bbl": 2.79,
                "risk_base": 45.3,
                "status": "active",
                "waypoints": [
                        [
                                26.5566,
                                50.191
                        ],
                        [
                                26.8052,
                                50.2434
                        ],
                        [
                                26.3,
                                51.6
                        ],
                        [
                                26.2549,
                                53.149
                        ],
                        [
                                26.1949,
                                54.3991
                        ],
                        [
                                26.1511,
                                55.0643
                        ],
                        [
                                26.1327,
                                55.345
                        ],
                        [
                                26.4411,
                                56.3434
                        ],
                        [
                                26.5111,
                                56.5472
                        ],
                        [
                                26.4221,
                                56.7631
                        ],
                        [
                                25.962,
                                56.9315
                        ],
                        [
                                25.5,
                                57.1
                        ],
                        [
                                24.6,
                                63.3
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_011",
                "from_node": "sup_saudi_arabia",
                "to_node": "port_vadinar",
                "corridor": "Strait of Hormuz",
                "corridor_id": "corr_hormuz",
                "corridors": [
                        "corr_hormuz"
                ],
                "capacity_bpd": 325000,
                "current_flow_bpd": 250000,
                "distance_km": 3965,
                "lead_time_days": 7,
                "transport_cost_usd_bbl": 2.79,
                "risk_base": 45.3,
                "status": "active",
                "waypoints": [
                        [
                                26.5566,
                                50.191
                        ],
                        [
                                26.8052,
                                50.2434
                        ],
                        [
                                26.3,
                                51.6
                        ],
                        [
                                26.2549,
                                53.149
                        ],
                        [
                                26.1949,
                                54.3991
                        ],
                        [
                                26.1511,
                                55.0643
                        ],
                        [
                                26.1327,
                                55.345
                        ],
                        [
                                26.4411,
                                56.3434
                        ],
                        [
                                26.5111,
                                56.5472
                        ],
                        [
                                26.4221,
                                56.7631
                        ],
                        [
                                25.962,
                                56.9315
                        ],
                        [
                                25.5,
                                57.1
                        ],
                        [
                                24.6,
                                63.3
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_012",
                "from_node": "sup_saudi_arabia",
                "to_node": "port_kochi",
                "corridor": "Strait of Hormuz",
                "corridor_id": "corr_hormuz",
                "corridors": [
                        "corr_hormuz"
                ],
                "capacity_bpd": 260000,
                "current_flow_bpd": 200000,
                "distance_km": 6546,
                "lead_time_days": 11,
                "transport_cost_usd_bbl": 3.82,
                "risk_base": 47.0,
                "status": "active",
                "waypoints": [
                        [
                                26.5566,
                                50.191
                        ],
                        [
                                26.8052,
                                50.2434
                        ],
                        [
                                26.3,
                                51.6
                        ],
                        [
                                26.2549,
                                53.149
                        ],
                        [
                                26.1949,
                                54.3991
                        ],
                        [
                                26.1511,
                                55.0643
                        ],
                        [
                                26.1327,
                                55.345
                        ],
                        [
                                26.4411,
                                56.3434
                        ],
                        [
                                26.5111,
                                56.5472
                        ],
                        [
                                26.4221,
                                56.7631
                        ],
                        [
                                25.962,
                                56.9315
                        ],
                        [
                                25.5,
                                57.1
                        ],
                        [
                                24,
                                59
                        ],
                        [
                                22.7,
                                60.4
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                20.0838,
                                64.5005
                        ],
                        [
                                19.4262,
                                64.9526
                        ],
                        [
                                17.5275,
                                66.2579
                        ],
                        [
                                16.9017,
                                66.6882
                        ],
                        [
                                15.7182,
                                67.6538
                        ],
                        [
                                14.6786,
                                68.8018
                        ],
                        [
                                13.7657,
                                69.9994
                        ],
                        [
                                9.7,
                                75.3
                        ],
                        [
                                9.8769,
                                76.1957
                        ]
                ]
        },
        {
                "_id": "route_013",
                "from_node": "sup_united_arab_emirates",
                "to_node": "port_mundra",
                "corridor": "Strait of Hormuz",
                "corridor_id": "corr_hormuz",
                "corridors": [
                        "corr_hormuz"
                ],
                "capacity_bpd": 325000,
                "current_flow_bpd": 250000,
                "distance_km": 2620,
                "lead_time_days": 4,
                "transport_cost_usd_bbl": 2.25,
                "risk_base": 43.0,
                "status": "active",
                "waypoints": [
                        [
                                25.1378,
                                56.4038
                        ],
                        [
                                25.5,
                                57.1
                        ],
                        [
                                24.6,
                                63.3
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_014",
                "from_node": "sup_united_arab_emirates",
                "to_node": "port_vadinar",
                "corridor": "Strait of Hormuz",
                "corridor_id": "corr_hormuz",
                "corridors": [
                        "corr_hormuz"
                ],
                "capacity_bpd": 260000,
                "current_flow_bpd": 200000,
                "distance_km": 2620,
                "lead_time_days": 4,
                "transport_cost_usd_bbl": 2.25,
                "risk_base": 43.0,
                "status": "active",
                "waypoints": [
                        [
                                25.1378,
                                56.4038
                        ],
                        [
                                25.5,
                                57.1
                        ],
                        [
                                24.6,
                                63.3
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_015",
                "from_node": "sup_united_arab_emirates",
                "to_node": "port_kochi",
                "corridor": "Strait of Hormuz",
                "corridor_id": "corr_hormuz",
                "corridors": [
                        "corr_hormuz"
                ],
                "capacity_bpd": 130000,
                "current_flow_bpd": 100000,
                "distance_km": 5201,
                "lead_time_days": 9,
                "transport_cost_usd_bbl": 3.28,
                "risk_base": 45.2,
                "status": "active",
                "waypoints": [
                        [
                                25.1378,
                                56.4038
                        ],
                        [
                                25.5,
                                57.1
                        ],
                        [
                                24,
                                59
                        ],
                        [
                                22.7,
                                60.4
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                20.0838,
                                64.5005
                        ],
                        [
                                19.4262,
                                64.9526
                        ],
                        [
                                17.5275,
                                66.2579
                        ],
                        [
                                16.9017,
                                66.6882
                        ],
                        [
                                15.7182,
                                67.6538
                        ],
                        [
                                14.6786,
                                68.8018
                        ],
                        [
                                13.7657,
                                69.9994
                        ],
                        [
                                9.7,
                                75.3
                        ],
                        [
                                9.8769,
                                76.1957
                        ]
                ]
        },
        {
                "_id": "route_016",
                "from_node": "sup_united_states",
                "to_node": "port_mundra",
                "corridor": "Panama Canal",
                "corridor_id": "corr_panama",
                "corridors": [
                        "corr_panama"
                ],
                "capacity_bpd": 325000,
                "current_flow_bpd": 250000,
                "distance_km": 33417,
                "lead_time_days": 56,
                "transport_cost_usd_bbl": 15.37,
                "risk_base": 32.3,
                "status": "active",
                "waypoints": [
                        [
                                29.7086,
                                -95.0455
                        ],
                        [
                                29.701,
                                -95.0014
                        ],
                        [
                                29.6835,
                                -94.9823
                        ],
                        [
                                29.6065,
                                -94.9523
                        ],
                        [
                                29.4996,
                                -94.8699
                        ],
                        [
                                29.3675,
                                -94.8021
                        ],
                        [
                                29.3423,
                                -94.7696
                        ],
                        [
                                29.3379,
                                -94.6878
                        ],
                        [
                                29.3068,
                                -94.6251
                        ],
                        [
                                29.1479,
                                -94.3779
                        ],
                        [
                                29.1321,
                                -93.6685
                        ],
                        [
                                29.13,
                                -93.214
                        ],
                        [
                                28.8674,
                                -92.4116
                        ],
                        [
                                28.7823,
                                -92.1518
                        ],
                        [
                                28.6457,
                                -91.8429
                        ],
                        [
                                28.5158,
                                -91.5493
                        ],
                        [
                                28.4094,
                                -91.3089
                        ],
                        [
                                27.9988,
                                -90.3808
                        ],
                        [
                                27.783,
                                -89.893
                        ],
                        [
                                27.727,
                                -89.7664
                        ],
                        [
                                27.2281,
                                -88.6387
                        ],
                        [
                                27.0297,
                                -88.194
                        ],
                        [
                                26.6179,
                                -87.3651
                        ],
                        [
                                26.3671,
                                -86.8602
                        ],
                        [
                                26.2803,
                                -86.6856
                        ],
                        [
                                25.8745,
                                -85.8688
                        ],
                        [
                                25.1603,
                                -84.4316
                        ],
                        [
                                24.3,
                                -82.7
                        ],
                        [
                                24.2187,
                                -81.825
                        ],
                        [
                                24.504,
                                -80.8143
                        ],
                        [
                                24.5133,
                                -80.7971
                        ],
                        [
                                24.7537,
                                -80.3533
                        ],
                        [
                                25.1148,
                                -80.0294
                        ],
                        [
                                25.2125,
                                -79.6463
                        ],
                        [
                                25.3971,
                                -78.9213
                        ],
                        [
                                25.3345,
                                -77.9031
                        ],
                        [
                                25.3142,
                                -77.3712
                        ],
                        [
                                25.6237,
                                -77.2401
                        ],
                        [
                                25.7702,
                                -77.179
                        ],
                        [
                                25.946,
                                -76.6183
                        ],
                        [
                                26.0029,
                                -76.3001
                        ],
                        [
                                26.0676,
                                -76.3271
                        ],
                        [
                                26.347,
                                -75.6577
                        ],
                        [
                                26.452,
                                -75.4059
                        ],
                        [
                                26.8917,
                                -74.3524
                        ],
                        [
                                27.0149,
                                -74.0572
                        ],
                        [
                                27.0911,
                                -73.8746
                        ],
                        [
                                27.1088,
                                -73.8321
                        ],
                        [
                                27.331,
                                -73.2997
                        ],
                        [
                                27.4184,
                                -73.0902
                        ],
                        [
                                27.5319,
                                -72.8183
                        ],
                        [
                                27.8048,
                                -72.1643
                        ],
                        [
                                28.4221,
                                -70.6852
                        ],
                        [
                                28.7049,
                                -70.0074
                        ],
                        [
                                28.7655,
                                -69.8624
                        ],
                        [
                                29.1039,
                                -69.0514
                        ],
                        [
                                29.1243,
                                -69.0025
                        ],
                        [
                                29.3034,
                                -68.3964
                        ],
                        [
                                29.6134,
                                -67.3474
                        ],
                        [
                                30.0791,
                                -65.7715
                        ],
                        [
                                30.3389,
                                -64.8921
                        ],
                        [
                                31.1038,
                                -62.3036
                        ],
                        [
                                31.1862,
                                -62.0247
                        ],
                        [
                                31.7843,
                                -60.0007
                        ],
                        [
                                32.4247,
                                -57.8335
                        ],
                        [
                                32.4371,
                                -57.7916
                        ],
                        [
                                32.4544,
                                -57.7424
                        ],
                        [
                                33.9128,
                                -53.5989
                        ],
                        [
                                34.6437,
                                -51.5223
                        ],
                        [
                                34.8293,
                                -50.002
                        ],
                        [
                                35.0063,
                                -48.5528
                        ],
                        [
                                35.4337,
                                -45.052
                        ],
                        [
                                35.4483,
                                -44.9322
                        ],
                        [
                                36.0503,
                                -40.0017
                        ],
                        [
                                36.1836,
                                -38.91
                        ],
                        [
                                36.2713,
                                -35.9596
                        ],
                        [
                                36.3302,
                                -33.9766
                        ],
                        [
                                36.4483,
                                -30.0015
                        ],
                        [
                                36.5022,
                                -28.1874
                        ],
                        [
                                36.4092,
                                -23.891
                        ],
                        [
                                36.3788,
                                -22.4866
                        ],
                        [
                                36.3249,
                                -20.0015
                        ],
                        [
                                36.29,
                                -18.3875
                        ],
                        [
                                36.2012,
                                -15.0878
                        ],
                        [
                                36.1437,
                                -12.9487
                        ],
                        [
                                36.1345,
                                -12.6085
                        ],
                        [
                                36.041,
                                -9.1308
                        ],
                        [
                                36.0355,
                                -8.929
                        ],
                        [
                                36.0331,
                                -8.8382
                        ],
                        [
                                36.0158,
                                -8.1962
                        ],
                        [
                                35.9957,
                                -7.4473
                        ],
                        [
                                35.95,
                                -5.75
                        ],
                        [
                                35.9688,
                                -5.3549
                        ],
                        [
                                35.9729,
                                -5.2694
                        ],
                        [
                                36,
                                -4.7
                        ],
                        [
                                36.1565,
                                -3.683
                        ],
                        [
                                36.2209,
                                -3.2642
                        ],
                        [
                                36.3245,
                                -2.5907
                        ],
                        [
                                36.3777,
                                -2.2448
                        ],
                        [
                                36.4732,
                                -1.6244
                        ],
                        [
                                36.6667,
                                -0.3667
                        ],
                        [
                                37.2,
                                3.1
                        ],
                        [
                                37.4,
                                7.5
                        ],
                        [
                                37.4821,
                                10.373
                        ],
                        [
                                37.5,
                                11
                        ],
                        [
                                37.4549,
                                11.1722
                        ],
                        [
                                37.2832,
                                11.8278
                        ],
                        [
                                37.2155,
                                12.0863
                        ],
                        [
                                37.2091,
                                12.1106
                        ],
                        [
                                36.9071,
                                13.2638
                        ],
                        [
                                36.4,
                                15.2
                        ],
                        [
                                36.0869,
                                16.7266
                        ],
                        [
                                35.8457,
                                17.9021
                        ],
                        [
                                35.1267,
                                21.4074
                        ],
                        [
                                34.8,
                                23
                        ],
                        [
                                34.1874,
                                24.9267
                        ],
                        [
                                34.0119,
                                25.4787
                        ],
                        [
                                33.7488,
                                26.3064
                        ],
                        [
                                33.2196,
                                27.9275
                        ],
                        [
                                33.1158,
                                28.2124
                        ],
                        [
                                32.8634,
                                28.9055
                        ],
                        [
                                32.3161,
                                30.4084
                        ],
                        [
                                31.7,
                                32.1
                        ],
                        [
                                31.3364,
                                32.3599
                        ],
                        [
                                31.1029,
                                32.3101
                        ],
                        [
                                30.3184,
                                32.3822
                        ],
                        [
                                30.214,
                                32.558
                        ],
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                14.1436,
                                49.5581
                        ],
                        [
                                16.2,
                                54.2
                        ],
                        [
                                17.3839,
                                56.876
                        ],
                        [
                                18.7425,
                                58.1918
                        ],
                        [
                                20,
                                59
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                22.8425,
                                64.447
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_017",
                "from_node": "sup_united_states",
                "to_node": "port_kochi",
                "corridor": "Cape of Good Hope",
                "corridor_id": "corr_cape",
                "corridors": [
                        "corr_cape"
                ],
                "capacity_bpd": 130000,
                "current_flow_bpd": 100000,
                "distance_km": 34167,
                "lead_time_days": 57,
                "transport_cost_usd_bbl": 14.87,
                "risk_base": 28.4,
                "status": "active",
                "waypoints": [
                        [
                                29.7086,
                                -95.0455
                        ],
                        [
                                29.701,
                                -95.0014
                        ],
                        [
                                29.6835,
                                -94.9823
                        ],
                        [
                                29.6065,
                                -94.9523
                        ],
                        [
                                29.4996,
                                -94.8699
                        ],
                        [
                                29.3675,
                                -94.8021
                        ],
                        [
                                29.3423,
                                -94.7696
                        ],
                        [
                                29.3379,
                                -94.6878
                        ],
                        [
                                29.3068,
                                -94.6251
                        ],
                        [
                                29.1479,
                                -94.3779
                        ],
                        [
                                29.1321,
                                -93.6685
                        ],
                        [
                                29.13,
                                -93.214
                        ],
                        [
                                28.8674,
                                -92.4116
                        ],
                        [
                                28.7823,
                                -92.1518
                        ],
                        [
                                28.6457,
                                -91.8429
                        ],
                        [
                                28.5158,
                                -91.5493
                        ],
                        [
                                28.4094,
                                -91.3089
                        ],
                        [
                                27.9988,
                                -90.3808
                        ],
                        [
                                27.783,
                                -89.893
                        ],
                        [
                                27.727,
                                -89.7664
                        ],
                        [
                                27.2281,
                                -88.6387
                        ],
                        [
                                27.0297,
                                -88.194
                        ],
                        [
                                26.6179,
                                -87.3651
                        ],
                        [
                                26.3671,
                                -86.8602
                        ],
                        [
                                26.2803,
                                -86.6856
                        ],
                        [
                                25.8745,
                                -85.8688
                        ],
                        [
                                25.1603,
                                -84.4316
                        ],
                        [
                                24.3,
                                -82.7
                        ],
                        [
                                24.2187,
                                -81.825
                        ],
                        [
                                24.504,
                                -80.8143
                        ],
                        [
                                24.5133,
                                -80.7971
                        ],
                        [
                                24.7537,
                                -80.3533
                        ],
                        [
                                25.1148,
                                -80.0294
                        ],
                        [
                                25.2125,
                                -79.6463
                        ],
                        [
                                25.3971,
                                -78.9213
                        ],
                        [
                                25.3345,
                                -77.9031
                        ],
                        [
                                25.3142,
                                -77.3712
                        ],
                        [
                                25.6237,
                                -77.2401
                        ],
                        [
                                25.7702,
                                -77.179
                        ],
                        [
                                25.946,
                                -76.6183
                        ],
                        [
                                26.0029,
                                -76.3001
                        ],
                        [
                                26.0676,
                                -76.3271
                        ],
                        [
                                26.347,
                                -75.6577
                        ],
                        [
                                26.452,
                                -75.4059
                        ],
                        [
                                26.8917,
                                -74.3524
                        ],
                        [
                                27.0149,
                                -74.0572
                        ],
                        [
                                27.0911,
                                -73.8746
                        ],
                        [
                                27.1088,
                                -73.8321
                        ],
                        [
                                27.331,
                                -73.2997
                        ],
                        [
                                27.4184,
                                -73.0902
                        ],
                        [
                                27.5319,
                                -72.8183
                        ],
                        [
                                27.8048,
                                -72.1643
                        ],
                        [
                                28.4221,
                                -70.6852
                        ],
                        [
                                28.7049,
                                -70.0074
                        ],
                        [
                                28.7655,
                                -69.8624
                        ],
                        [
                                29.1039,
                                -69.0514
                        ],
                        [
                                29.1243,
                                -69.0025
                        ],
                        [
                                29.3034,
                                -68.3964
                        ],
                        [
                                29.6134,
                                -67.3474
                        ],
                        [
                                30.0791,
                                -65.7715
                        ],
                        [
                                30.3389,
                                -64.8921
                        ],
                        [
                                31.1038,
                                -62.3036
                        ],
                        [
                                31.1862,
                                -62.0247
                        ],
                        [
                                31.7843,
                                -60.0007
                        ],
                        [
                                32.4247,
                                -57.8335
                        ],
                        [
                                32.4371,
                                -57.7916
                        ],
                        [
                                32.4544,
                                -57.7424
                        ],
                        [
                                33.9128,
                                -53.5989
                        ],
                        [
                                34.6437,
                                -51.5223
                        ],
                        [
                                34.8293,
                                -50.002
                        ],
                        [
                                35.0063,
                                -48.5528
                        ],
                        [
                                35.4337,
                                -45.052
                        ],
                        [
                                35.4483,
                                -44.9322
                        ],
                        [
                                36.0503,
                                -40.0017
                        ],
                        [
                                36.1836,
                                -38.91
                        ],
                        [
                                36.2713,
                                -35.9596
                        ],
                        [
                                36.3302,
                                -33.9766
                        ],
                        [
                                36.4483,
                                -30.0015
                        ],
                        [
                                36.5022,
                                -28.1874
                        ],
                        [
                                36.4092,
                                -23.891
                        ],
                        [
                                36.3788,
                                -22.4866
                        ],
                        [
                                36.3249,
                                -20.0015
                        ],
                        [
                                36.29,
                                -18.3875
                        ],
                        [
                                36.2012,
                                -15.0878
                        ],
                        [
                                36.1437,
                                -12.9487
                        ],
                        [
                                36.1345,
                                -12.6085
                        ],
                        [
                                36.041,
                                -9.1308
                        ],
                        [
                                36.0355,
                                -8.929
                        ],
                        [
                                36.0331,
                                -8.8382
                        ],
                        [
                                36.0158,
                                -8.1962
                        ],
                        [
                                35.9957,
                                -7.4473
                        ],
                        [
                                35.95,
                                -5.75
                        ],
                        [
                                35.9688,
                                -5.3549
                        ],
                        [
                                35.9729,
                                -5.2694
                        ],
                        [
                                36,
                                -4.7
                        ],
                        [
                                36.1565,
                                -3.683
                        ],
                        [
                                36.2209,
                                -3.2642
                        ],
                        [
                                36.3245,
                                -2.5907
                        ],
                        [
                                36.3777,
                                -2.2448
                        ],
                        [
                                36.4732,
                                -1.6244
                        ],
                        [
                                36.6667,
                                -0.3667
                        ],
                        [
                                37.2,
                                3.1
                        ],
                        [
                                37.4,
                                7.5
                        ],
                        [
                                37.4821,
                                10.373
                        ],
                        [
                                37.5,
                                11
                        ],
                        [
                                37.4549,
                                11.1722
                        ],
                        [
                                37.2832,
                                11.8278
                        ],
                        [
                                37.2155,
                                12.0863
                        ],
                        [
                                37.2091,
                                12.1106
                        ],
                        [
                                36.9071,
                                13.2638
                        ],
                        [
                                36.4,
                                15.2
                        ],
                        [
                                36.0869,
                                16.7266
                        ],
                        [
                                35.8457,
                                17.9021
                        ],
                        [
                                35.1267,
                                21.4074
                        ],
                        [
                                34.8,
                                23
                        ],
                        [
                                34.1874,
                                24.9267
                        ],
                        [
                                34.0119,
                                25.4787
                        ],
                        [
                                33.7488,
                                26.3064
                        ],
                        [
                                33.2196,
                                27.9275
                        ],
                        [
                                33.1158,
                                28.2124
                        ],
                        [
                                32.8634,
                                28.9055
                        ],
                        [
                                32.3161,
                                30.4084
                        ],
                        [
                                31.7,
                                32.1
                        ],
                        [
                                31.3364,
                                32.3599
                        ],
                        [
                                31.1029,
                                32.3101
                        ],
                        [
                                30.3184,
                                32.3822
                        ],
                        [
                                30.214,
                                32.558
                        ],
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                12.884,
                                50.8561
                        ],
                        [
                                13.3,
                                53.6189
                        ],
                        [
                                12.7475,
                                55.0415
                        ],
                        [
                                11.0835,
                                59.894
                        ],
                        [
                                10.867,
                                60.8257
                        ],
                        [
                                10.5802,
                                62.0601
                        ],
                        [
                                10.0316,
                                64.3032
                        ],
                        [
                                10.0345,
                                64.6969
                        ],
                        [
                                10.0367,
                                65.0002
                        ],
                        [
                                10.0358,
                                65.1268
                        ],
                        [
                                10,
                                70
                        ],
                        [
                                9.7,
                                75.3
                        ],
                        [
                                9.8769,
                                76.1957
                        ]
                ]
        },
        {
                "_id": "route_018",
                "from_node": "sup_united_states",
                "to_node": "port_mangalore",
                "corridor": "Cape of Good Hope",
                "corridor_id": "corr_cape",
                "corridors": [
                        "corr_cape"
                ],
                "capacity_bpd": 130000,
                "current_flow_bpd": 100000,
                "distance_km": 34787,
                "lead_time_days": 58,
                "transport_cost_usd_bbl": 15.11,
                "risk_base": 28.4,
                "status": "active",
                "waypoints": [
                        [
                                29.7086,
                                -95.0455
                        ],
                        [
                                29.701,
                                -95.0014
                        ],
                        [
                                29.6835,
                                -94.9823
                        ],
                        [
                                29.6065,
                                -94.9523
                        ],
                        [
                                29.4996,
                                -94.8699
                        ],
                        [
                                29.3675,
                                -94.8021
                        ],
                        [
                                29.3423,
                                -94.7696
                        ],
                        [
                                29.3379,
                                -94.6878
                        ],
                        [
                                29.3068,
                                -94.6251
                        ],
                        [
                                29.1479,
                                -94.3779
                        ],
                        [
                                29.1321,
                                -93.6685
                        ],
                        [
                                29.13,
                                -93.214
                        ],
                        [
                                28.8674,
                                -92.4116
                        ],
                        [
                                28.7823,
                                -92.1518
                        ],
                        [
                                28.6457,
                                -91.8429
                        ],
                        [
                                28.5158,
                                -91.5493
                        ],
                        [
                                28.4094,
                                -91.3089
                        ],
                        [
                                27.9988,
                                -90.3808
                        ],
                        [
                                27.783,
                                -89.893
                        ],
                        [
                                27.727,
                                -89.7664
                        ],
                        [
                                27.2281,
                                -88.6387
                        ],
                        [
                                27.0297,
                                -88.194
                        ],
                        [
                                26.6179,
                                -87.3651
                        ],
                        [
                                26.3671,
                                -86.8602
                        ],
                        [
                                26.2803,
                                -86.6856
                        ],
                        [
                                25.8745,
                                -85.8688
                        ],
                        [
                                25.1603,
                                -84.4316
                        ],
                        [
                                24.3,
                                -82.7
                        ],
                        [
                                24.2187,
                                -81.825
                        ],
                        [
                                24.504,
                                -80.8143
                        ],
                        [
                                24.5133,
                                -80.7971
                        ],
                        [
                                24.7537,
                                -80.3533
                        ],
                        [
                                25.1148,
                                -80.0294
                        ],
                        [
                                25.2125,
                                -79.6463
                        ],
                        [
                                25.3971,
                                -78.9213
                        ],
                        [
                                25.3345,
                                -77.9031
                        ],
                        [
                                25.3142,
                                -77.3712
                        ],
                        [
                                25.6237,
                                -77.2401
                        ],
                        [
                                25.7702,
                                -77.179
                        ],
                        [
                                25.946,
                                -76.6183
                        ],
                        [
                                26.0029,
                                -76.3001
                        ],
                        [
                                26.0676,
                                -76.3271
                        ],
                        [
                                26.347,
                                -75.6577
                        ],
                        [
                                26.452,
                                -75.4059
                        ],
                        [
                                26.8917,
                                -74.3524
                        ],
                        [
                                27.0149,
                                -74.0572
                        ],
                        [
                                27.0911,
                                -73.8746
                        ],
                        [
                                27.1088,
                                -73.8321
                        ],
                        [
                                27.331,
                                -73.2997
                        ],
                        [
                                27.4184,
                                -73.0902
                        ],
                        [
                                27.5319,
                                -72.8183
                        ],
                        [
                                27.8048,
                                -72.1643
                        ],
                        [
                                28.4221,
                                -70.6852
                        ],
                        [
                                28.7049,
                                -70.0074
                        ],
                        [
                                28.7655,
                                -69.8624
                        ],
                        [
                                29.1039,
                                -69.0514
                        ],
                        [
                                29.1243,
                                -69.0025
                        ],
                        [
                                29.3034,
                                -68.3964
                        ],
                        [
                                29.6134,
                                -67.3474
                        ],
                        [
                                30.0791,
                                -65.7715
                        ],
                        [
                                30.3389,
                                -64.8921
                        ],
                        [
                                31.1038,
                                -62.3036
                        ],
                        [
                                31.1862,
                                -62.0247
                        ],
                        [
                                31.7843,
                                -60.0007
                        ],
                        [
                                32.4247,
                                -57.8335
                        ],
                        [
                                32.4371,
                                -57.7916
                        ],
                        [
                                32.4544,
                                -57.7424
                        ],
                        [
                                33.9128,
                                -53.5989
                        ],
                        [
                                34.6437,
                                -51.5223
                        ],
                        [
                                34.8293,
                                -50.002
                        ],
                        [
                                35.0063,
                                -48.5528
                        ],
                        [
                                35.4337,
                                -45.052
                        ],
                        [
                                35.4483,
                                -44.9322
                        ],
                        [
                                36.0503,
                                -40.0017
                        ],
                        [
                                36.1836,
                                -38.91
                        ],
                        [
                                36.2713,
                                -35.9596
                        ],
                        [
                                36.3302,
                                -33.9766
                        ],
                        [
                                36.4483,
                                -30.0015
                        ],
                        [
                                36.5022,
                                -28.1874
                        ],
                        [
                                36.4092,
                                -23.891
                        ],
                        [
                                36.3788,
                                -22.4866
                        ],
                        [
                                36.3249,
                                -20.0015
                        ],
                        [
                                36.29,
                                -18.3875
                        ],
                        [
                                36.2012,
                                -15.0878
                        ],
                        [
                                36.1437,
                                -12.9487
                        ],
                        [
                                36.1345,
                                -12.6085
                        ],
                        [
                                36.041,
                                -9.1308
                        ],
                        [
                                36.0355,
                                -8.929
                        ],
                        [
                                36.0331,
                                -8.8382
                        ],
                        [
                                36.0158,
                                -8.1962
                        ],
                        [
                                35.9957,
                                -7.4473
                        ],
                        [
                                35.95,
                                -5.75
                        ],
                        [
                                35.9688,
                                -5.3549
                        ],
                        [
                                35.9729,
                                -5.2694
                        ],
                        [
                                36,
                                -4.7
                        ],
                        [
                                36.1565,
                                -3.683
                        ],
                        [
                                36.2209,
                                -3.2642
                        ],
                        [
                                36.3245,
                                -2.5907
                        ],
                        [
                                36.3777,
                                -2.2448
                        ],
                        [
                                36.4732,
                                -1.6244
                        ],
                        [
                                36.6667,
                                -0.3667
                        ],
                        [
                                37.2,
                                3.1
                        ],
                        [
                                37.4,
                                7.5
                        ],
                        [
                                37.4821,
                                10.373
                        ],
                        [
                                37.5,
                                11
                        ],
                        [
                                37.4549,
                                11.1722
                        ],
                        [
                                37.2832,
                                11.8278
                        ],
                        [
                                37.2155,
                                12.0863
                        ],
                        [
                                37.2091,
                                12.1106
                        ],
                        [
                                36.9071,
                                13.2638
                        ],
                        [
                                36.4,
                                15.2
                        ],
                        [
                                36.0869,
                                16.7266
                        ],
                        [
                                35.8457,
                                17.9021
                        ],
                        [
                                35.1267,
                                21.4074
                        ],
                        [
                                34.8,
                                23
                        ],
                        [
                                34.1874,
                                24.9267
                        ],
                        [
                                34.0119,
                                25.4787
                        ],
                        [
                                33.7488,
                                26.3064
                        ],
                        [
                                33.2196,
                                27.9275
                        ],
                        [
                                33.1158,
                                28.2124
                        ],
                        [
                                32.8634,
                                28.9055
                        ],
                        [
                                32.3161,
                                30.4084
                        ],
                        [
                                31.7,
                                32.1
                        ],
                        [
                                31.3364,
                                32.3599
                        ],
                        [
                                31.1029,
                                32.3101
                        ],
                        [
                                30.3184,
                                32.3822
                        ],
                        [
                                30.214,
                                32.558
                        ],
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                12.884,
                                50.8561
                        ],
                        [
                                13.3,
                                53.6189
                        ],
                        [
                                12.7475,
                                55.0415
                        ],
                        [
                                11.0835,
                                59.894
                        ],
                        [
                                10.867,
                                60.8257
                        ],
                        [
                                10.5802,
                                62.0601
                        ],
                        [
                                10.0316,
                                64.3032
                        ],
                        [
                                10.0345,
                                64.6969
                        ],
                        [
                                10.0367,
                                65.0002
                        ],
                        [
                                10.0358,
                                65.1268
                        ],
                        [
                                10,
                                70
                        ],
                        [
                                9.7,
                                75.3
                        ],
                        [
                                12.7734,
                                74.1335
                        ],
                        [
                                12.8172,
                                74.7784
                        ]
                ]
        },
        {
                "_id": "route_019",
                "from_node": "sup_kuwait",
                "to_node": "port_mundra",
                "corridor": "Strait of Hormuz",
                "corridor_id": "corr_hormuz",
                "corridors": [
                        "corr_hormuz"
                ],
                "capacity_bpd": 130000,
                "current_flow_bpd": 100000,
                "distance_km": 4448,
                "lead_time_days": 7,
                "transport_cost_usd_bbl": 2.98,
                "risk_base": 45.1,
                "status": "active",
                "waypoints": [
                        [
                                29.0595,
                                48.1546
                        ],
                        [
                                29.1,
                                48.3
                        ],
                        [
                                28.2146,
                                49.0551
                        ],
                        [
                                27.1816,
                                51.222
                        ],
                        [
                                26.5789,
                                53.3693
                        ],
                        [
                                26.1949,
                                54.3991
                        ],
                        [
                                26.1511,
                                55.0643
                        ],
                        [
                                26.1327,
                                55.345
                        ],
                        [
                                26.4411,
                                56.3434
                        ],
                        [
                                26.5111,
                                56.5472
                        ],
                        [
                                26.4221,
                                56.7631
                        ],
                        [
                                25.962,
                                56.9315
                        ],
                        [
                                25.5,
                                57.1
                        ],
                        [
                                24.6,
                                63.3
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_020",
                "from_node": "sup_kuwait",
                "to_node": "port_vadinar",
                "corridor": "Strait of Hormuz",
                "corridor_id": "corr_hormuz",
                "corridors": [
                        "corr_hormuz"
                ],
                "capacity_bpd": 130000,
                "current_flow_bpd": 100000,
                "distance_km": 4448,
                "lead_time_days": 7,
                "transport_cost_usd_bbl": 2.98,
                "risk_base": 45.1,
                "status": "active",
                "waypoints": [
                        [
                                29.0595,
                                48.1546
                        ],
                        [
                                29.1,
                                48.3
                        ],
                        [
                                28.2146,
                                49.0551
                        ],
                        [
                                27.1816,
                                51.222
                        ],
                        [
                                26.5789,
                                53.3693
                        ],
                        [
                                26.1949,
                                54.3991
                        ],
                        [
                                26.1511,
                                55.0643
                        ],
                        [
                                26.1327,
                                55.345
                        ],
                        [
                                26.4411,
                                56.3434
                        ],
                        [
                                26.5111,
                                56.5472
                        ],
                        [
                                26.4221,
                                56.7631
                        ],
                        [
                                25.962,
                                56.9315
                        ],
                        [
                                25.5,
                                57.1
                        ],
                        [
                                24.6,
                                63.3
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_021",
                "from_node": "sup_nigeria",
                "to_node": "port_mundra",
                "corridor": "Cape of Good Hope",
                "corridor_id": "corr_cape",
                "corridors": [
                        "corr_cape"
                ],
                "capacity_bpd": 130000,
                "current_flow_bpd": 100000,
                "distance_km": 25231,
                "lead_time_days": 42,
                "transport_cost_usd_bbl": 11.29,
                "risk_base": 32.4,
                "status": "active",
                "waypoints": [
                        [
                                4.3902,
                                7.0958
                        ],
                        [
                                4.1547,
                                7.1027
                        ],
                        [
                                0.9777,
                                8.6133
                        ],
                        [
                                0.0934,
                                8.2562
                        ],
                        [
                                -1.0327,
                                8.02
                        ],
                        [
                                -4.9924,
                                11.1401
                        ],
                        [
                                -5.9597,
                                11.5437
                        ],
                        [
                                -9,
                                12
                        ],
                        [
                                -15.5,
                                11
                        ],
                        [
                                -19,
                                11
                        ],
                        [
                                -22.9092,
                                13.8094
                        ],
                        [
                                -26.8633,
                                14.5349
                        ],
                        [
                                -35,
                                18
                        ],
                        [
                                -35,
                                22
                        ],
                        [
                                -34.5,
                                26
                        ],
                        [
                                -33.5,
                                28.5
                        ],
                        [
                                -30,
                                32
                        ],
                        [
                                -28.4494,
                                32.9205
                        ],
                        [
                                -25.7496,
                                34.437
                        ],
                        [
                                -24.861,
                                35.143
                        ],
                        [
                                -24,
                                36
                        ],
                        [
                                -16.6783,
                                42.5171
                        ],
                        [
                                -12.7839,
                                46.9055
                        ],
                        [
                                -10,
                                50
                        ],
                        [
                                -6.3666,
                                52.7787
                        ],
                        [
                                -4.9773,
                                53.822
                        ],
                        [
                                -3.9723,
                                54.5768
                        ],
                        [
                                -2.7181,
                                55.5186
                        ],
                        [
                                -0.0,
                                57.544
                        ],
                        [
                                0.9368,
                                58.2421
                        ],
                        [
                                1.8048,
                                58.8907
                        ],
                        [
                                3.2894,
                                59.9998
                        ],
                        [
                                3.997,
                                60.5285
                        ],
                        [
                                4.5895,
                                60.9712
                        ],
                        [
                                7.1453,
                                62.906
                        ],
                        [
                                8.2314,
                                63.7282
                        ],
                        [
                                8.5686,
                                63.9895
                        ],
                        [
                                9.4951,
                                64.7077
                        ],
                        [
                                9.8629,
                                64.9928
                        ],
                        [
                                10.0358,
                                65.1268
                        ],
                        [
                                11.8535,
                                66.5357
                        ],
                        [
                                12.66,
                                67.1826
                        ],
                        [
                                14.6786,
                                68.8018
                        ],
                        [
                                15.4465,
                                69.4177
                        ],
                        [
                                16.1396,
                                69.9994
                        ],
                        [
                                18.4327,
                                69.9997
                        ],
                        [
                                20,
                                70
                        ],
                        [
                                20.8093,
                                69.5925
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_022",
                "from_node": "sup_nigeria",
                "to_node": "port_kochi",
                "corridor": "Cape of Good Hope",
                "corridor_id": "corr_cape",
                "corridors": [
                        "corr_cape"
                ],
                "capacity_bpd": 104000,
                "current_flow_bpd": 80000,
                "distance_km": 24040,
                "lead_time_days": 40,
                "transport_cost_usd_bbl": 10.82,
                "risk_base": 32.4,
                "status": "active",
                "waypoints": [
                        [
                                4.3902,
                                7.0958
                        ],
                        [
                                4.1547,
                                7.1027
                        ],
                        [
                                0.9777,
                                8.6133
                        ],
                        [
                                0.0934,
                                8.2562
                        ],
                        [
                                -1.0327,
                                8.02
                        ],
                        [
                                -4.9924,
                                11.1401
                        ],
                        [
                                -5.9597,
                                11.5437
                        ],
                        [
                                -9,
                                12
                        ],
                        [
                                -15.5,
                                11
                        ],
                        [
                                -19,
                                11
                        ],
                        [
                                -22.9092,
                                13.8094
                        ],
                        [
                                -26.8633,
                                14.5349
                        ],
                        [
                                -35,
                                18
                        ],
                        [
                                -35,
                                22
                        ],
                        [
                                -34.5,
                                26
                        ],
                        [
                                -33.5,
                                28.5
                        ],
                        [
                                -30,
                                32
                        ],
                        [
                                -28.4494,
                                32.9205
                        ],
                        [
                                -25.7496,
                                34.437
                        ],
                        [
                                -24.861,
                                35.143
                        ],
                        [
                                -24,
                                36
                        ],
                        [
                                -16.6783,
                                42.5171
                        ],
                        [
                                -12.7839,
                                46.9055
                        ],
                        [
                                -10,
                                50
                        ],
                        [
                                -7.3078,
                                52.6658
                        ],
                        [
                                -6.0208,
                                53.9178
                        ],
                        [
                                -4.6,
                                55.3
                        ],
                        [
                                -0.0,
                                60
                        ],
                        [
                                2.325,
                                62.292
                        ],
                        [
                                2.512,
                                62.4763
                        ],
                        [
                                4.8565,
                                64.8008
                        ],
                        [
                                5.0192,
                                64.9621
                        ],
                        [
                                5.0571,
                                65.0001
                        ],
                        [
                                7.3463,
                                67.2956
                        ],
                        [
                                7.5169,
                                67.4667
                        ],
                        [
                                8.8816,
                                68.859
                        ],
                        [
                                10,
                                70
                        ],
                        [
                                9.7,
                                75.3
                        ],
                        [
                                9.8769,
                                76.1957
                        ]
                ]
        },
        {
                "_id": "route_023",
                "from_node": "sup_angola",
                "to_node": "port_mundra",
                "corridor": "Cape of Good Hope",
                "corridor_id": "corr_cape",
                "corridors": [
                        "corr_cape"
                ],
                "capacity_bpd": 130000,
                "current_flow_bpd": 100000,
                "distance_km": 22375,
                "lead_time_days": 37,
                "transport_cost_usd_bbl": 10.15,
                "risk_base": 32.0,
                "status": "active",
                "waypoints": [
                        [
                                -8.5593,
                                13.0737
                        ],
                        [
                                -9,
                                12
                        ],
                        [
                                -15.5,
                                11
                        ],
                        [
                                -19,
                                11
                        ],
                        [
                                -22.9092,
                                13.8094
                        ],
                        [
                                -26.8633,
                                14.5349
                        ],
                        [
                                -35,
                                18
                        ],
                        [
                                -35,
                                22
                        ],
                        [
                                -34.5,
                                26
                        ],
                        [
                                -33.5,
                                28.5
                        ],
                        [
                                -30,
                                32
                        ],
                        [
                                -28.4494,
                                32.9205
                        ],
                        [
                                -25.7496,
                                34.437
                        ],
                        [
                                -24.861,
                                35.143
                        ],
                        [
                                -24,
                                36
                        ],
                        [
                                -16.6783,
                                42.5171
                        ],
                        [
                                -12.7839,
                                46.9055
                        ],
                        [
                                -10,
                                50
                        ],
                        [
                                -6.3666,
                                52.7787
                        ],
                        [
                                -4.9773,
                                53.822
                        ],
                        [
                                -3.9723,
                                54.5768
                        ],
                        [
                                -2.7181,
                                55.5186
                        ],
                        [
                                -0.0,
                                57.544
                        ],
                        [
                                0.9368,
                                58.2421
                        ],
                        [
                                1.8048,
                                58.8907
                        ],
                        [
                                3.2894,
                                59.9998
                        ],
                        [
                                3.997,
                                60.5285
                        ],
                        [
                                4.5895,
                                60.9712
                        ],
                        [
                                7.1453,
                                62.906
                        ],
                        [
                                8.2314,
                                63.7282
                        ],
                        [
                                8.5686,
                                63.9895
                        ],
                        [
                                9.4951,
                                64.7077
                        ],
                        [
                                9.8629,
                                64.9928
                        ],
                        [
                                10.0358,
                                65.1268
                        ],
                        [
                                11.8535,
                                66.5357
                        ],
                        [
                                12.66,
                                67.1826
                        ],
                        [
                                14.6786,
                                68.8018
                        ],
                        [
                                15.4465,
                                69.4177
                        ],
                        [
                                16.1396,
                                69.9994
                        ],
                        [
                                18.4327,
                                69.9997
                        ],
                        [
                                20,
                                70
                        ],
                        [
                                20.8093,
                                69.5925
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_024",
                "from_node": "sup_angola",
                "to_node": "port_kochi",
                "corridor": "Cape of Good Hope",
                "corridor_id": "corr_cape",
                "corridors": [
                        "corr_cape"
                ],
                "capacity_bpd": 91000,
                "current_flow_bpd": 70000,
                "distance_km": 21184,
                "lead_time_days": 35,
                "transport_cost_usd_bbl": 9.67,
                "risk_base": 32.0,
                "status": "active",
                "waypoints": [
                        [
                                -8.5593,
                                13.0737
                        ],
                        [
                                -9,
                                12
                        ],
                        [
                                -15.5,
                                11
                        ],
                        [
                                -19,
                                11
                        ],
                        [
                                -22.9092,
                                13.8094
                        ],
                        [
                                -26.8633,
                                14.5349
                        ],
                        [
                                -35,
                                18
                        ],
                        [
                                -35,
                                22
                        ],
                        [
                                -34.5,
                                26
                        ],
                        [
                                -33.5,
                                28.5
                        ],
                        [
                                -30,
                                32
                        ],
                        [
                                -28.4494,
                                32.9205
                        ],
                        [
                                -25.7496,
                                34.437
                        ],
                        [
                                -24.861,
                                35.143
                        ],
                        [
                                -24,
                                36
                        ],
                        [
                                -16.6783,
                                42.5171
                        ],
                        [
                                -12.7839,
                                46.9055
                        ],
                        [
                                -10,
                                50
                        ],
                        [
                                -7.3078,
                                52.6658
                        ],
                        [
                                -6.0208,
                                53.9178
                        ],
                        [
                                -4.6,
                                55.3
                        ],
                        [
                                -0.0,
                                60
                        ],
                        [
                                2.325,
                                62.292
                        ],
                        [
                                2.512,
                                62.4763
                        ],
                        [
                                4.8565,
                                64.8008
                        ],
                        [
                                5.0192,
                                64.9621
                        ],
                        [
                                5.0571,
                                65.0001
                        ],
                        [
                                7.3463,
                                67.2956
                        ],
                        [
                                7.5169,
                                67.4667
                        ],
                        [
                                8.8816,
                                68.859
                        ],
                        [
                                10,
                                70
                        ],
                        [
                                9.7,
                                75.3
                        ],
                        [
                                9.8769,
                                76.1957
                        ]
                ]
        },
        {
                "_id": "route_025",
                "from_node": "sup_brazil",
                "to_node": "port_mundra",
                "corridor": "Cape of Good Hope",
                "corridor_id": "corr_cape",
                "corridors": [
                        "corr_cape"
                ],
                "capacity_bpd": 91000,
                "current_flow_bpd": 70000,
                "distance_km": 28244,
                "lead_time_days": 47,
                "transport_cost_usd_bbl": 12.5,
                "risk_base": 32.8,
                "status": "active",
                "waypoints": [
                        [
                                -23.9815,
                                -46.3479
                        ],
                        [
                                -24.3,
                                -46.3
                        ],
                        [
                                -25.7725,
                                -44.6766
                        ],
                        [
                                -26.0859,
                                -42.873
                        ],
                        [
                                -26.3569,
                                -41.2891
                        ],
                        [
                                -26.6079,
                                -39.8226
                        ],
                        [
                                -27.1024,
                                -36.9327
                        ],
                        [
                                -27.9338,
                                -32.0745
                        ],
                        [
                                -28.2888,
                                -29.9995
                        ],
                        [
                                -28.5512,
                                -28.4664
                        ],
                        [
                                -30,
                                -20
                        ],
                        [
                                -30.9131,
                                -10.8398
                        ],
                        [
                                -31.0097,
                                -9.9996
                        ],
                        [
                                -31.162,
                                -8.9312
                        ],
                        [
                                -32.1526,
                                -1.98
                        ],
                        [
                                -32.4349,
                                0.001
                        ],
                        [
                                -32.8021,
                                2.5773
                        ],
                        [
                                -33.4126,
                                6.8611
                        ],
                        [
                                -33.8601,
                                10.0016
                        ],
                        [
                                -35,
                                18
                        ],
                        [
                                -35,
                                22
                        ],
                        [
                                -34.5,
                                26
                        ],
                        [
                                -33.5,
                                28.5
                        ],
                        [
                                -30,
                                32
                        ],
                        [
                                -28.4494,
                                32.9205
                        ],
                        [
                                -25.7496,
                                34.437
                        ],
                        [
                                -24.861,
                                35.143
                        ],
                        [
                                -24,
                                36
                        ],
                        [
                                -16.6783,
                                42.5171
                        ],
                        [
                                -12.7839,
                                46.9055
                        ],
                        [
                                -10,
                                50
                        ],
                        [
                                -6.3666,
                                52.7787
                        ],
                        [
                                -4.9773,
                                53.822
                        ],
                        [
                                -3.9723,
                                54.5768
                        ],
                        [
                                -2.7181,
                                55.5186
                        ],
                        [
                                -0.0,
                                57.544
                        ],
                        [
                                0.9368,
                                58.2421
                        ],
                        [
                                1.8048,
                                58.8907
                        ],
                        [
                                3.2894,
                                59.9998
                        ],
                        [
                                3.997,
                                60.5285
                        ],
                        [
                                4.5895,
                                60.9712
                        ],
                        [
                                7.1453,
                                62.906
                        ],
                        [
                                8.2314,
                                63.7282
                        ],
                        [
                                8.5686,
                                63.9895
                        ],
                        [
                                9.4951,
                                64.7077
                        ],
                        [
                                9.8629,
                                64.9928
                        ],
                        [
                                10.0358,
                                65.1268
                        ],
                        [
                                11.8535,
                                66.5357
                        ],
                        [
                                12.66,
                                67.1826
                        ],
                        [
                                14.6786,
                                68.8018
                        ],
                        [
                                15.4465,
                                69.4177
                        ],
                        [
                                16.1396,
                                69.9994
                        ],
                        [
                                18.4327,
                                69.9997
                        ],
                        [
                                20,
                                70
                        ],
                        [
                                20.8093,
                                69.5925
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_026",
                "from_node": "sup_brazil",
                "to_node": "port_kochi",
                "corridor": "Cape of Good Hope",
                "corridor_id": "corr_cape",
                "corridors": [
                        "corr_cape"
                ],
                "capacity_bpd": 104000,
                "current_flow_bpd": 80000,
                "distance_km": 27052,
                "lead_time_days": 45,
                "transport_cost_usd_bbl": 12.02,
                "risk_base": 32.8,
                "status": "active",
                "waypoints": [
                        [
                                -23.9815,
                                -46.3479
                        ],
                        [
                                -24.3,
                                -46.3
                        ],
                        [
                                -25.7725,
                                -44.6766
                        ],
                        [
                                -26.0859,
                                -42.873
                        ],
                        [
                                -26.3569,
                                -41.2891
                        ],
                        [
                                -26.6079,
                                -39.8226
                        ],
                        [
                                -27.1024,
                                -36.9327
                        ],
                        [
                                -27.9338,
                                -32.0745
                        ],
                        [
                                -28.2888,
                                -29.9995
                        ],
                        [
                                -28.5512,
                                -28.4664
                        ],
                        [
                                -30,
                                -20
                        ],
                        [
                                -30.9131,
                                -10.8398
                        ],
                        [
                                -31.0097,
                                -9.9996
                        ],
                        [
                                -31.162,
                                -8.9312
                        ],
                        [
                                -32.1526,
                                -1.98
                        ],
                        [
                                -32.4349,
                                0.001
                        ],
                        [
                                -32.8021,
                                2.5773
                        ],
                        [
                                -33.4126,
                                6.8611
                        ],
                        [
                                -33.8601,
                                10.0016
                        ],
                        [
                                -35,
                                18
                        ],
                        [
                                -35,
                                22
                        ],
                        [
                                -34.5,
                                26
                        ],
                        [
                                -33.5,
                                28.5
                        ],
                        [
                                -30,
                                32
                        ],
                        [
                                -28.4494,
                                32.9205
                        ],
                        [
                                -25.7496,
                                34.437
                        ],
                        [
                                -24.861,
                                35.143
                        ],
                        [
                                -24,
                                36
                        ],
                        [
                                -16.6783,
                                42.5171
                        ],
                        [
                                -12.7839,
                                46.9055
                        ],
                        [
                                -10,
                                50
                        ],
                        [
                                -7.3078,
                                52.6658
                        ],
                        [
                                -6.0208,
                                53.9178
                        ],
                        [
                                -4.6,
                                55.3
                        ],
                        [
                                -0.0,
                                60
                        ],
                        [
                                2.325,
                                62.292
                        ],
                        [
                                2.512,
                                62.4763
                        ],
                        [
                                4.8565,
                                64.8008
                        ],
                        [
                                5.0192,
                                64.9621
                        ],
                        [
                                5.0571,
                                65.0001
                        ],
                        [
                                7.3463,
                                67.2956
                        ],
                        [
                                7.5169,
                                67.4667
                        ],
                        [
                                8.8816,
                                68.859
                        ],
                        [
                                10,
                                70
                        ],
                        [
                                9.7,
                                75.3
                        ],
                        [
                                9.8769,
                                76.1957
                        ]
                ]
        },
        {
                "_id": "route_027",
                "from_node": "sup_egypt",
                "to_node": "port_mundra",
                "corridor": "Suez Canal + Bab el-Mandeb",
                "corridor_id": "corr_suez",
                "corridors": [
                        "corr_suez",
                        "corr_babelmandeb"
                ],
                "capacity_bpd": 78000,
                "current_flow_bpd": 60000,
                "distance_km": 10126,
                "lead_time_days": 17,
                "transport_cost_usd_bbl": 6.05,
                "risk_base": 59.5,
                "status": "active",
                "waypoints": [
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                14.1436,
                                49.5581
                        ],
                        [
                                16.2,
                                54.2
                        ],
                        [
                                17.3839,
                                56.876
                        ],
                        [
                                18.7425,
                                58.1918
                        ],
                        [
                                20,
                                59
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                22.8425,
                                64.447
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_028",
                "from_node": "sup_egypt",
                "to_node": "port_vadinar",
                "corridor": "Suez Canal + Bab el-Mandeb",
                "corridor_id": "corr_suez",
                "corridors": [
                        "corr_suez",
                        "corr_babelmandeb"
                ],
                "capacity_bpd": 52000,
                "current_flow_bpd": 40000,
                "distance_km": 10126,
                "lead_time_days": 17,
                "transport_cost_usd_bbl": 6.05,
                "risk_base": 59.5,
                "status": "active",
                "waypoints": [
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                14.1436,
                                49.5581
                        ],
                        [
                                16.2,
                                54.2
                        ],
                        [
                                17.3839,
                                56.876
                        ],
                        [
                                18.7425,
                                58.1918
                        ],
                        [
                                20,
                                59
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                22.8425,
                                64.447
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_029",
                "from_node": "sup_colombia",
                "to_node": "port_mundra",
                "corridor": "Cape of Good Hope",
                "corridor_id": "corr_cape",
                "corridors": [
                        "corr_cape"
                ],
                "capacity_bpd": 117000,
                "current_flow_bpd": 90000,
                "distance_km": 31210,
                "lead_time_days": 52,
                "transport_cost_usd_bbl": 13.68,
                "risk_base": 34.6,
                "status": "active",
                "waypoints": [
                        [
                                10.3109,
                                -75.6313
                        ],
                        [
                                10.8897,
                                -75.7315
                        ],
                        [
                                11.5988,
                                -74.6858
                        ],
                        [
                                12.447,
                                -72.2363
                        ],
                        [
                                12.7425,
                                -71.0422
                        ],
                        [
                                13,
                                -70
                        ],
                        [
                                13.6822,
                                -68.4885
                        ],
                        [
                                13.7598,
                                -68.3165
                        ],
                        [
                                14.047,
                                -67.6801
                        ],
                        [
                                14.27,
                                -67.186
                        ],
                        [
                                14.4296,
                                -66.8326
                        ],
                        [
                                15.3062,
                                -64.8915
                        ],
                        [
                                15.5777,
                                -64.2885
                        ],
                        [
                                16.1047,
                                -63.1209
                        ],
                        [
                                16.5272,
                                -62.1849
                        ],
                        [
                                16.6566,
                                -61.8986
                        ],
                        [
                                17.3628,
                                -60.3334
                        ],
                        [
                                18.4778,
                                -58.3925
                        ],
                        [
                                20.0447,
                                -55.665
                        ],
                        [
                                20.0604,
                                -55.6376
                        ],
                        [
                                22.1396,
                                -52.0183
                        ],
                        [
                                22.551,
                                -51.302
                        ],
                        [
                                22.8284,
                                -50.8192
                        ],
                        [
                                23.1973,
                                -50.0009
                        ],
                        [
                                25.3954,
                                -45.1255
                        ],
                        [
                                25.6122,
                                -44.6447
                        ],
                        [
                                27.7059,
                                -40.0006
                        ],
                        [
                                28.2769,
                                -38.7342
                        ],
                        [
                                28.4042,
                                -38.3107
                        ],
                        [
                                30.0529,
                                -32.8269
                        ],
                        [
                                30.7072,
                                -30.6505
                        ],
                        [
                                30.9026,
                                -30.0004
                        ],
                        [
                                31.2478,
                                -28.8523
                        ],
                        [
                                32.5575,
                                -24.4959
                        ],
                        [
                                33.1495,
                                -21.3679
                        ],
                        [
                                33.4081,
                                -20.0014
                        ],
                        [
                                33.7506,
                                -18.1915
                        ],
                        [
                                34.1005,
                                -16.3426
                        ],
                        [
                                34.2859,
                                -15.3633
                        ],
                        [
                                34.6797,
                                -13.1149
                        ],
                        [
                                35.3847,
                                -9.0277
                        ],
                        [
                                35.4622,
                                -8.578
                        ],
                        [
                                35.4695,
                                -8.5356
                        ],
                        [
                                35.5317,
                                -8.1751
                        ],
                        [
                                35.6218,
                                -7.6526
                        ],
                        [
                                35.95,
                                -5.75
                        ],
                        [
                                35.9688,
                                -5.3549
                        ],
                        [
                                35.9729,
                                -5.2694
                        ],
                        [
                                36,
                                -4.7
                        ],
                        [
                                36.1565,
                                -3.683
                        ],
                        [
                                36.2209,
                                -3.2642
                        ],
                        [
                                36.3245,
                                -2.5907
                        ],
                        [
                                36.3777,
                                -2.2448
                        ],
                        [
                                36.4732,
                                -1.6244
                        ],
                        [
                                36.6667,
                                -0.3667
                        ],
                        [
                                37.2,
                                3.1
                        ],
                        [
                                37.4,
                                7.5
                        ],
                        [
                                37.4821,
                                10.373
                        ],
                        [
                                37.5,
                                11
                        ],
                        [
                                37.4549,
                                11.1722
                        ],
                        [
                                37.2832,
                                11.8278
                        ],
                        [
                                37.2155,
                                12.0863
                        ],
                        [
                                37.2091,
                                12.1106
                        ],
                        [
                                36.9071,
                                13.2638
                        ],
                        [
                                36.4,
                                15.2
                        ],
                        [
                                36.0869,
                                16.7266
                        ],
                        [
                                35.8457,
                                17.9021
                        ],
                        [
                                35.1267,
                                21.4074
                        ],
                        [
                                34.8,
                                23
                        ],
                        [
                                34.1874,
                                24.9267
                        ],
                        [
                                34.0119,
                                25.4787
                        ],
                        [
                                33.7488,
                                26.3064
                        ],
                        [
                                33.2196,
                                27.9275
                        ],
                        [
                                33.1158,
                                28.2124
                        ],
                        [
                                32.8634,
                                28.9055
                        ],
                        [
                                32.3161,
                                30.4084
                        ],
                        [
                                31.7,
                                32.1
                        ],
                        [
                                31.3364,
                                32.3599
                        ],
                        [
                                31.1029,
                                32.3101
                        ],
                        [
                                30.3184,
                                32.3822
                        ],
                        [
                                30.214,
                                32.558
                        ],
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                14.1436,
                                49.5581
                        ],
                        [
                                16.2,
                                54.2
                        ],
                        [
                                17.3839,
                                56.876
                        ],
                        [
                                18.7425,
                                58.1918
                        ],
                        [
                                20,
                                59
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                22.8425,
                                64.447
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_030",
                "from_node": "sup_qatar",
                "to_node": "port_mundra",
                "corridor": "Strait of Hormuz",
                "corridor_id": "corr_hormuz",
                "corridors": [
                        "corr_hormuz"
                ],
                "capacity_bpd": 65000,
                "current_flow_bpd": 50000,
                "distance_km": 3709,
                "lead_time_days": 6,
                "transport_cost_usd_bbl": 2.68,
                "risk_base": 44.3,
                "status": "active",
                "waypoints": [
                        [
                                25.3142,
                                51.5547
                        ],
                        [
                                25.3316,
                                51.8431
                        ],
                        [
                                25.3791,
                                52.5565
                        ],
                        [
                                25.6,
                                55.2
                        ],
                        [
                                25.7787,
                                55.4674
                        ],
                        [
                                26.0257,
                                55.8375
                        ],
                        [
                                26.4411,
                                56.3434
                        ],
                        [
                                26.5111,
                                56.5472
                        ],
                        [
                                26.4221,
                                56.7631
                        ],
                        [
                                25.962,
                                56.9315
                        ],
                        [
                                25.5,
                                57.1
                        ],
                        [
                                24.6,
                                63.3
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_031",
                "from_node": "sup_qatar",
                "to_node": "port_kochi",
                "corridor": "Strait of Hormuz",
                "corridor_id": "corr_hormuz",
                "corridors": [
                        "corr_hormuz"
                ],
                "capacity_bpd": 45500,
                "current_flow_bpd": 35000,
                "distance_km": 6290,
                "lead_time_days": 10,
                "transport_cost_usd_bbl": 3.72,
                "risk_base": 46.0,
                "status": "active",
                "waypoints": [
                        [
                                25.3142,
                                51.5547
                        ],
                        [
                                25.3316,
                                51.8431
                        ],
                        [
                                25.3791,
                                52.5565
                        ],
                        [
                                25.6,
                                55.2
                        ],
                        [
                                25.7787,
                                55.4674
                        ],
                        [
                                26.0257,
                                55.8375
                        ],
                        [
                                26.4411,
                                56.3434
                        ],
                        [
                                26.5111,
                                56.5472
                        ],
                        [
                                26.4221,
                                56.7631
                        ],
                        [
                                25.962,
                                56.9315
                        ],
                        [
                                25.5,
                                57.1
                        ],
                        [
                                24,
                                59
                        ],
                        [
                                22.7,
                                60.4
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                20.0838,
                                64.5005
                        ],
                        [
                                19.4262,
                                64.9526
                        ],
                        [
                                17.5275,
                                66.2579
                        ],
                        [
                                16.9017,
                                66.6882
                        ],
                        [
                                15.7182,
                                67.6538
                        ],
                        [
                                14.6786,
                                68.8018
                        ],
                        [
                                13.7657,
                                69.9994
                        ],
                        [
                                9.7,
                                75.3
                        ],
                        [
                                9.8769,
                                76.1957
                        ]
                ]
        },
        {
                "_id": "route_032",
                "from_node": "sup_oman",
                "to_node": "port_kochi",
                "corridor": "Direct / Arabian Sea",
                "corridor_id": null,
                "corridors": [],
                "capacity_bpd": 52000,
                "current_flow_bpd": 40000,
                "distance_km": 4693,
                "lead_time_days": 8,
                "transport_cost_usd_bbl": 3.08,
                "risk_base": 17.0,
                "status": "active",
                "waypoints": [
                        [
                                23.6268,
                                58.5669
                        ],
                        [
                                24,
                                59
                        ],
                        [
                                22.7,
                                60.4
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                20.0838,
                                64.5005
                        ],
                        [
                                19.4262,
                                64.9526
                        ],
                        [
                                17.5275,
                                66.2579
                        ],
                        [
                                16.9017,
                                66.6882
                        ],
                        [
                                15.7182,
                                67.6538
                        ],
                        [
                                14.6786,
                                68.8018
                        ],
                        [
                                13.7657,
                                69.9994
                        ],
                        [
                                9.7,
                                75.3
                        ],
                        [
                                9.8769,
                                76.1957
                        ]
                ]
        },
        {
                "_id": "route_033",
                "from_node": "sup_oman",
                "to_node": "port_mangalore",
                "corridor": "Direct / Arabian Sea",
                "corridor_id": null,
                "corridors": [],
                "capacity_bpd": 52000,
                "current_flow_bpd": 40000,
                "distance_km": 4412,
                "lead_time_days": 7,
                "transport_cost_usd_bbl": 2.96,
                "risk_base": 16.5,
                "status": "active",
                "waypoints": [
                        [
                                23.6268,
                                58.5669
                        ],
                        [
                                24,
                                59
                        ],
                        [
                                23.457,
                                61.5554
                        ],
                        [
                                22.8425,
                                64.447
                        ],
                        [
                                22.5708,
                                65.7258
                        ],
                        [
                                22.3,
                                67
                        ],
                        [
                                20.8093,
                                69.5925
                        ],
                        [
                                20,
                                70
                        ],
                        [
                                19,
                                72.4
                        ],
                        [
                                15.3,
                                73
                        ],
                        [
                                12.7734,
                                74.1335
                        ],
                        [
                                12.8172,
                                74.7784
                        ]
                ]
        },
        {
                "_id": "route_034",
                "from_node": "sup_mexico",
                "to_node": "port_mundra",
                "corridor": "Cape of Good Hope",
                "corridor_id": "corr_cape",
                "corridors": [
                        "corr_cape"
                ],
                "capacity_bpd": 78000,
                "current_flow_bpd": 60000,
                "distance_km": 33283,
                "lead_time_days": 55,
                "transport_cost_usd_bbl": 14.51,
                "risk_base": 36.0,
                "status": "active",
                "waypoints": [
                        [
                                18.5708,
                                -93.3179
                        ],
                        [
                                18.7685,
                                -92.774
                        ],
                        [
                                22.1,
                                -89.8
                        ],
                        [
                                22.7208,
                                -87.8819
                        ],
                        [
                                22.7233,
                                -87.8742
                        ],
                        [
                                22.8436,
                                -87.5023
                        ],
                        [
                                22.9049,
                                -87.3128
                        ],
                        [
                                22.9468,
                                -87.1835
                        ],
                        [
                                22.97,
                                -87.1117
                        ],
                        [
                                23.1091,
                                -86.6821
                        ],
                        [
                                23.1683,
                                -86.499
                        ],
                        [
                                23.1883,
                                -86.4373
                        ],
                        [
                                23.23,
                                -86.3084
                        ],
                        [
                                23.2396,
                                -86.2788
                        ],
                        [
                                23.3373,
                                -85.9492
                        ],
                        [
                                23.5635,
                                -85.1857
                        ],
                        [
                                24.3,
                                -82.7
                        ],
                        [
                                24.2187,
                                -81.825
                        ],
                        [
                                24.504,
                                -80.8143
                        ],
                        [
                                24.5133,
                                -80.7971
                        ],
                        [
                                24.7537,
                                -80.3533
                        ],
                        [
                                25.1148,
                                -80.0294
                        ],
                        [
                                25.2125,
                                -79.6463
                        ],
                        [
                                25.3971,
                                -78.9213
                        ],
                        [
                                25.3345,
                                -77.9031
                        ],
                        [
                                25.3142,
                                -77.3712
                        ],
                        [
                                25.6237,
                                -77.2401
                        ],
                        [
                                25.7702,
                                -77.179
                        ],
                        [
                                25.946,
                                -76.6183
                        ],
                        [
                                26.0029,
                                -76.3001
                        ],
                        [
                                26.0676,
                                -76.3271
                        ],
                        [
                                26.347,
                                -75.6577
                        ],
                        [
                                26.452,
                                -75.4059
                        ],
                        [
                                26.8917,
                                -74.3524
                        ],
                        [
                                27.0149,
                                -74.0572
                        ],
                        [
                                27.0911,
                                -73.8746
                        ],
                        [
                                27.1088,
                                -73.8321
                        ],
                        [
                                27.331,
                                -73.2997
                        ],
                        [
                                27.4184,
                                -73.0902
                        ],
                        [
                                27.5319,
                                -72.8183
                        ],
                        [
                                27.8048,
                                -72.1643
                        ],
                        [
                                28.4221,
                                -70.6852
                        ],
                        [
                                28.7049,
                                -70.0074
                        ],
                        [
                                28.7655,
                                -69.8624
                        ],
                        [
                                29.1039,
                                -69.0514
                        ],
                        [
                                29.1243,
                                -69.0025
                        ],
                        [
                                29.3034,
                                -68.3964
                        ],
                        [
                                29.6134,
                                -67.3474
                        ],
                        [
                                30.0791,
                                -65.7715
                        ],
                        [
                                30.3389,
                                -64.8921
                        ],
                        [
                                31.1038,
                                -62.3036
                        ],
                        [
                                31.1862,
                                -62.0247
                        ],
                        [
                                31.7843,
                                -60.0007
                        ],
                        [
                                32.4247,
                                -57.8335
                        ],
                        [
                                32.4371,
                                -57.7916
                        ],
                        [
                                32.4544,
                                -57.7424
                        ],
                        [
                                33.9128,
                                -53.5989
                        ],
                        [
                                34.6437,
                                -51.5223
                        ],
                        [
                                34.8293,
                                -50.002
                        ],
                        [
                                35.0063,
                                -48.5528
                        ],
                        [
                                35.4337,
                                -45.052
                        ],
                        [
                                35.4483,
                                -44.9322
                        ],
                        [
                                36.0503,
                                -40.0017
                        ],
                        [
                                36.1836,
                                -38.91
                        ],
                        [
                                36.2713,
                                -35.9596
                        ],
                        [
                                36.3302,
                                -33.9766
                        ],
                        [
                                36.4483,
                                -30.0015
                        ],
                        [
                                36.5022,
                                -28.1874
                        ],
                        [
                                36.4092,
                                -23.891
                        ],
                        [
                                36.3788,
                                -22.4866
                        ],
                        [
                                36.3249,
                                -20.0015
                        ],
                        [
                                36.29,
                                -18.3875
                        ],
                        [
                                36.2012,
                                -15.0878
                        ],
                        [
                                36.1437,
                                -12.9487
                        ],
                        [
                                36.1345,
                                -12.6085
                        ],
                        [
                                36.041,
                                -9.1308
                        ],
                        [
                                36.0355,
                                -8.929
                        ],
                        [
                                36.0331,
                                -8.8382
                        ],
                        [
                                36.0158,
                                -8.1962
                        ],
                        [
                                35.9957,
                                -7.4473
                        ],
                        [
                                35.95,
                                -5.75
                        ],
                        [
                                35.9688,
                                -5.3549
                        ],
                        [
                                35.9729,
                                -5.2694
                        ],
                        [
                                36,
                                -4.7
                        ],
                        [
                                36.1565,
                                -3.683
                        ],
                        [
                                36.2209,
                                -3.2642
                        ],
                        [
                                36.3245,
                                -2.5907
                        ],
                        [
                                36.3777,
                                -2.2448
                        ],
                        [
                                36.4732,
                                -1.6244
                        ],
                        [
                                36.6667,
                                -0.3667
                        ],
                        [
                                37.2,
                                3.1
                        ],
                        [
                                37.4,
                                7.5
                        ],
                        [
                                37.4821,
                                10.373
                        ],
                        [
                                37.5,
                                11
                        ],
                        [
                                37.4549,
                                11.1722
                        ],
                        [
                                37.2832,
                                11.8278
                        ],
                        [
                                37.2155,
                                12.0863
                        ],
                        [
                                37.2091,
                                12.1106
                        ],
                        [
                                36.9071,
                                13.2638
                        ],
                        [
                                36.4,
                                15.2
                        ],
                        [
                                36.0869,
                                16.7266
                        ],
                        [
                                35.8457,
                                17.9021
                        ],
                        [
                                35.1267,
                                21.4074
                        ],
                        [
                                34.8,
                                23
                        ],
                        [
                                34.1874,
                                24.9267
                        ],
                        [
                                34.0119,
                                25.4787
                        ],
                        [
                                33.7488,
                                26.3064
                        ],
                        [
                                33.2196,
                                27.9275
                        ],
                        [
                                33.1158,
                                28.2124
                        ],
                        [
                                32.8634,
                                28.9055
                        ],
                        [
                                32.3161,
                                30.4084
                        ],
                        [
                                31.7,
                                32.1
                        ],
                        [
                                31.3364,
                                32.3599
                        ],
                        [
                                31.1029,
                                32.3101
                        ],
                        [
                                30.3184,
                                32.3822
                        ],
                        [
                                30.214,
                                32.558
                        ],
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                14.1436,
                                49.5581
                        ],
                        [
                                16.2,
                                54.2
                        ],
                        [
                                17.3839,
                                56.876
                        ],
                        [
                                18.7425,
                                58.1918
                        ],
                        [
                                20,
                                59
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                22.8425,
                                64.447
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_035",
                "from_node": "sup_venezuela",
                "to_node": "port_mundra",
                "corridor": "Cape of Good Hope",
                "corridor_id": "corr_cape",
                "corridors": [
                        "corr_cape"
                ],
                "capacity_bpd": 65000,
                "current_flow_bpd": 50000,
                "distance_km": 29657,
                "lead_time_days": 49,
                "transport_cost_usd_bbl": 13.06,
                "risk_base": 34.4,
                "status": "active",
                "waypoints": [
                        [
                                10.271,
                                -64.7023
                        ],
                        [
                                11.3161,
                                -64.8127
                        ],
                        [
                                11.3508,
                                -64.0393
                        ],
                        [
                                12,
                                -61.9
                        ],
                        [
                                11.4868,
                                -61.4369
                        ],
                        [
                                12.6231,
                                -59.1333
                        ],
                        [
                                12.787,
                                -58.9303
                        ],
                        [
                                15.6054,
                                -55.4409
                        ],
                        [
                                17.3529,
                                -53.2774
                        ],
                        [
                                20,
                                -50
                        ],
                        [
                                20.8402,
                                -49.2073
                        ],
                        [
                                25.0849,
                                -45.2028
                        ],
                        [
                                25.2766,
                                -44.9998
                        ],
                        [
                                25.6122,
                                -44.6447
                        ],
                        [
                                27.7059,
                                -40.0006
                        ],
                        [
                                28.2769,
                                -38.7342
                        ],
                        [
                                28.4042,
                                -38.3107
                        ],
                        [
                                30.0529,
                                -32.8269
                        ],
                        [
                                30.7072,
                                -30.6505
                        ],
                        [
                                30.9026,
                                -30.0004
                        ],
                        [
                                31.2478,
                                -28.8523
                        ],
                        [
                                32.5575,
                                -24.4959
                        ],
                        [
                                33.1495,
                                -21.3679
                        ],
                        [
                                33.4081,
                                -20.0014
                        ],
                        [
                                33.7506,
                                -18.1915
                        ],
                        [
                                34.1005,
                                -16.3426
                        ],
                        [
                                34.2859,
                                -15.3633
                        ],
                        [
                                34.6797,
                                -13.1149
                        ],
                        [
                                35.3847,
                                -9.0277
                        ],
                        [
                                35.4622,
                                -8.578
                        ],
                        [
                                35.4695,
                                -8.5356
                        ],
                        [
                                35.5317,
                                -8.1751
                        ],
                        [
                                35.6218,
                                -7.6526
                        ],
                        [
                                35.95,
                                -5.75
                        ],
                        [
                                35.9688,
                                -5.3549
                        ],
                        [
                                35.9729,
                                -5.2694
                        ],
                        [
                                36,
                                -4.7
                        ],
                        [
                                36.1565,
                                -3.683
                        ],
                        [
                                36.2209,
                                -3.2642
                        ],
                        [
                                36.3245,
                                -2.5907
                        ],
                        [
                                36.3777,
                                -2.2448
                        ],
                        [
                                36.4732,
                                -1.6244
                        ],
                        [
                                36.6667,
                                -0.3667
                        ],
                        [
                                37.2,
                                3.1
                        ],
                        [
                                37.4,
                                7.5
                        ],
                        [
                                37.4821,
                                10.373
                        ],
                        [
                                37.5,
                                11
                        ],
                        [
                                37.4549,
                                11.1722
                        ],
                        [
                                37.2832,
                                11.8278
                        ],
                        [
                                37.2155,
                                12.0863
                        ],
                        [
                                37.2091,
                                12.1106
                        ],
                        [
                                36.9071,
                                13.2638
                        ],
                        [
                                36.4,
                                15.2
                        ],
                        [
                                36.0869,
                                16.7266
                        ],
                        [
                                35.8457,
                                17.9021
                        ],
                        [
                                35.1267,
                                21.4074
                        ],
                        [
                                34.8,
                                23
                        ],
                        [
                                34.1874,
                                24.9267
                        ],
                        [
                                34.0119,
                                25.4787
                        ],
                        [
                                33.7488,
                                26.3064
                        ],
                        [
                                33.2196,
                                27.9275
                        ],
                        [
                                33.1158,
                                28.2124
                        ],
                        [
                                32.8634,
                                28.9055
                        ],
                        [
                                32.3161,
                                30.4084
                        ],
                        [
                                31.7,
                                32.1
                        ],
                        [
                                31.3364,
                                32.3599
                        ],
                        [
                                31.1029,
                                32.3101
                        ],
                        [
                                30.3184,
                                32.3822
                        ],
                        [
                                30.214,
                                32.558
                        ],
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                14.1436,
                                49.5581
                        ],
                        [
                                16.2,
                                54.2
                        ],
                        [
                                17.3839,
                                56.876
                        ],
                        [
                                18.7425,
                                58.1918
                        ],
                        [
                                20,
                                59
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                22.8425,
                                64.447
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_036",
                "from_node": "sup_guyana",
                "to_node": "port_mundra",
                "corridor": "Cape of Good Hope",
                "corridor_id": "corr_cape",
                "corridors": [
                        "corr_cape"
                ],
                "capacity_bpd": 58500,
                "current_flow_bpd": 45000,
                "distance_km": 29392,
                "lead_time_days": 49,
                "transport_cost_usd_bbl": 12.96,
                "risk_base": 32.8,
                "status": "active",
                "waypoints": [
                        [
                                7,
                                -57.9
                        ],
                        [
                                6.1,
                                -55.4
                        ],
                        [
                                5.4,
                                -51.9
                        ],
                        [
                                7.8004,
                                -50.9085
                        ],
                        [
                                10,
                                -50
                        ],
                        [
                                11.7364,
                                -48.3462
                        ],
                        [
                                15.1704,
                                -44.9998
                        ],
                        [
                                16.3769,
                                -43.7764
                        ],
                        [
                                20,
                                -40
                        ],
                        [
                                22.0815,
                                -38.0362
                        ],
                        [
                                24.0855,
                                -33.8539
                        ],
                        [
                                25.9315,
                                -30.0011
                        ],
                        [
                                26.4426,
                                -28.9344
                        ],
                        [
                                27.4241,
                                -26.4693
                        ],
                        [
                                30,
                                -20
                        ],
                        [
                                33.1162,
                                -17.1838
                        ],
                        [
                                34.0652,
                                -13.3287
                        ],
                        [
                                34.6035,
                                -11.4737
                        ],
                        [
                                35.1862,
                                -8.9966
                        ],
                        [
                                35.3071,
                                -8.483
                        ],
                        [
                                35.3143,
                                -8.4522
                        ],
                        [
                                35.381,
                                -8.1685
                        ],
                        [
                                35.4847,
                                -7.7279
                        ],
                        [
                                35.95,
                                -5.75
                        ],
                        [
                                35.9688,
                                -5.3549
                        ],
                        [
                                35.9729,
                                -5.2694
                        ],
                        [
                                36,
                                -4.7
                        ],
                        [
                                36.1565,
                                -3.683
                        ],
                        [
                                36.2209,
                                -3.2642
                        ],
                        [
                                36.3245,
                                -2.5907
                        ],
                        [
                                36.3777,
                                -2.2448
                        ],
                        [
                                36.4732,
                                -1.6244
                        ],
                        [
                                36.6667,
                                -0.3667
                        ],
                        [
                                37.2,
                                3.1
                        ],
                        [
                                37.4,
                                7.5
                        ],
                        [
                                37.4821,
                                10.373
                        ],
                        [
                                37.5,
                                11
                        ],
                        [
                                37.4549,
                                11.1722
                        ],
                        [
                                37.2832,
                                11.8278
                        ],
                        [
                                37.2155,
                                12.0863
                        ],
                        [
                                37.2091,
                                12.1106
                        ],
                        [
                                36.9071,
                                13.2638
                        ],
                        [
                                36.4,
                                15.2
                        ],
                        [
                                36.0869,
                                16.7266
                        ],
                        [
                                35.8457,
                                17.9021
                        ],
                        [
                                35.1267,
                                21.4074
                        ],
                        [
                                34.8,
                                23
                        ],
                        [
                                34.1874,
                                24.9267
                        ],
                        [
                                34.0119,
                                25.4787
                        ],
                        [
                                33.7488,
                                26.3064
                        ],
                        [
                                33.2196,
                                27.9275
                        ],
                        [
                                33.1158,
                                28.2124
                        ],
                        [
                                32.8634,
                                28.9055
                        ],
                        [
                                32.3161,
                                30.4084
                        ],
                        [
                                31.7,
                                32.1
                        ],
                        [
                                31.3364,
                                32.3599
                        ],
                        [
                                31.1029,
                                32.3101
                        ],
                        [
                                30.3184,
                                32.3822
                        ],
                        [
                                30.214,
                                32.558
                        ],
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                14.1436,
                                49.5581
                        ],
                        [
                                16.2,
                                54.2
                        ],
                        [
                                17.3839,
                                56.876
                        ],
                        [
                                18.7425,
                                58.1918
                        ],
                        [
                                20,
                                59
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                22.8425,
                                64.447
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_037",
                "from_node": "sup_kazakhstan",
                "to_node": "port_mundra",
                "corridor": "Turkish Straits + Gibraltar Strait + Suez Canal + Bab el-Mandeb",
                "corridor_id": "corr_turkish",
                "corridors": [
                        "corr_turkish",
                        "corr_gibraltar",
                        "corr_suez",
                        "corr_babelmandeb"
                ],
                "capacity_bpd": 52000,
                "current_flow_bpd": 40000,
                "distance_km": 17808,
                "lead_time_days": 30,
                "transport_cost_usd_bbl": 9.12,
                "risk_base": 74.9,
                "status": "active",
                "waypoints": [
                        [
                                43.6122,
                                51.1386
                        ],
                        [
                                43.5576,
                                50.818
                        ],
                        [
                                45.1174,
                                47.8023
                        ],
                        [
                                45.3943,
                                47.7826
                        ],
                        [
                                45.682,
                                47.6988
                        ],
                        [
                                45.7219,
                                47.6375
                        ],
                        [
                                45.7682,
                                47.6457
                        ],
                        [
                                45.8065,
                                47.6842
                        ],
                        [
                                45.8477,
                                47.6715
                        ],
                        [
                                45.8803,
                                47.6224
                        ],
                        [
                                45.9386,
                                47.6623
                        ],
                        [
                                45.9749,
                                47.63
                        ],
                        [
                                45.9816,
                                47.6945
                        ],
                        [
                                46.0283,
                                47.7048
                        ],
                        [
                                46.0993,
                                47.7426
                        ],
                        [
                                46.1502,
                                47.8174
                        ],
                        [
                                46.1926,
                                47.849
                        ],
                        [
                                46.2126,
                                47.9088
                        ],
                        [
                                46.3921,
                                48.0394
                        ],
                        [
                                46.4603,
                                47.9762
                        ],
                        [
                                46.5246,
                                48.0339
                        ],
                        [
                                46.5416,
                                48.0174
                        ],
                        [
                                46.5813,
                                47.9062
                        ],
                        [
                                46.653,
                                47.8924
                        ],
                        [
                                46.7473,
                                47.832
                        ],
                        [
                                46.8589,
                                47.7147
                        ],
                        [
                                46.8439,
                                47.6049
                        ],
                        [
                                46.9565,
                                47.6049
                        ],
                        [
                                47.2185,
                                47.0775
                        ],
                        [
                                47.2968,
                                47.1215
                        ],
                        [
                                47.4271,
                                46.9786
                        ],
                        [
                                47.4271,
                                46.8743
                        ],
                        [
                                47.7237,
                                46.5502
                        ],
                        [
                                47.8603,
                                46.3524
                        ],
                        [
                                47.9487,
                                46.1547
                        ],
                        [
                                48.2058,
                                46.1766
                        ],
                        [
                                48.2409,
                                46.0042
                        ],
                        [
                                48.3232,
                                45.8888
                        ],
                        [
                                48.4664,
                                45.5633
                        ],
                        [
                                48.4081,
                                45.3683
                        ],
                        [
                                48.4746,
                                45.0978
                        ],
                        [
                                48.438,
                                44.9769
                        ],
                        [
                                48.4772,
                                44.9055
                        ],
                        [
                                48.5382,
                                44.6254
                        ],
                        [
                                48.5305,
                                44.5571
                        ],
                        [
                                48.4846,
                                44.552
                        ],
                        [
                                48.425,
                                44.5036
                        ],
                        [
                                48.422,
                                44.483
                        ],
                        [
                                48.4685,
                                44.3471
                        ],
                        [
                                48.494,
                                44.2068
                        ],
                        [
                                48.5486,
                                44.1601
                        ],
                        [
                                48.625,
                                44.064
                        ],
                        [
                                48.6822,
                                43.9674
                        ],
                        [
                                48.6541,
                                43.6948
                        ],
                        [
                                48.4861,
                                43.3202
                        ],
                        [
                                47.7673,
                                42.728
                        ],
                        [
                                47.56,
                                42.0908
                        ],
                        [
                                47.5823,
                                40.9153
                        ],
                        [
                                47.4635,
                                40.5088
                        ],
                        [
                                47.2252,
                                40.2012
                        ],
                        [
                                47.1953,
                                39.6958
                        ],
                        [
                                47.0757,
                                39.2673
                        ],
                        [
                                47.104,
                                39.0431
                        ],
                        [
                                46.8238,
                                37.6629
                        ],
                        [
                                45.6212,
                                36.8592
                        ],
                        [
                                45,
                                36.4
                        ],
                        [
                                43,
                                33
                        ],
                        [
                                41.2424,
                                29.1324
                        ],
                        [
                                41.1863,
                                29.096
                        ],
                        [
                                41.1521,
                                29.0505
                        ],
                        [
                                41.1178,
                                29.0705
                        ],
                        [
                                41.0505,
                                29.0423
                        ],
                        [
                                41.0279,
                                28.995
                        ],
                        [
                                40.9716,
                                28.9777
                        ],
                        [
                                40.8222,
                                28.5015
                        ],
                        [
                                40.8058,
                                28.4495
                        ],
                        [
                                40.605,
                                27.2776
                        ],
                        [
                                40.4407,
                                26.7682
                        ],
                        [
                                40.1,
                                26.2
                        ],
                        [
                                39.9929,
                                26.1436
                        ],
                        [
                                39.7844,
                                26.0975
                        ],
                        [
                                39.495,
                                25.9535
                        ],
                        [
                                39.2374,
                                25.8253
                        ],
                        [
                                39.136,
                                25.8305
                        ],
                        [
                                38.8895,
                                26.023
                        ],
                        [
                                38.7165,
                                26.158
                        ],
                        [
                                38.5234,
                                26.3087
                        ],
                        [
                                38.4379,
                                26.2698
                        ],
                        [
                                38.339,
                                26.1849
                        ],
                        [
                                38.2533,
                                26.1727
                        ],
                        [
                                37.8134,
                                26.3662
                        ],
                        [
                                37.2667,
                                26.4301
                        ],
                        [
                                37.009,
                                26.6359
                        ],
                        [
                                36.5471,
                                27.0028
                        ],
                        [
                                36.4985,
                                27.0304
                        ],
                        [
                                36.2,
                                27.2
                        ],
                        [
                                35.8802,
                                27.5482
                        ],
                        [
                                35.2993,
                                28.1807
                        ],
                        [
                                34.656,
                                28.8812
                        ],
                        [
                                34.5797,
                                28.9643
                        ],
                        [
                                34.0004,
                                29.5952
                        ],
                        [
                                33.9013,
                                29.703
                        ],
                        [
                                32.9863,
                                30.6994
                        ],
                        [
                                32.9251,
                                30.766
                        ],
                        [
                                31.7,
                                32.1
                        ],
                        [
                                31.3364,
                                32.3599
                        ],
                        [
                                31.1029,
                                32.3101
                        ],
                        [
                                30.3184,
                                32.3822
                        ],
                        [
                                30.214,
                                32.558
                        ],
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                14.1436,
                                49.5581
                        ],
                        [
                                16.2,
                                54.2
                        ],
                        [
                                17.3839,
                                56.876
                        ],
                        [
                                18.7425,
                                58.1918
                        ],
                        [
                                20,
                                59
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                22.8425,
                                64.447
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_038",
                "from_node": "sup_norway",
                "to_node": "port_mundra",
                "corridor": "English Channel / Dover Strait + Gibraltar Strait + Suez Canal + Bab el-Mandeb",
                "corridor_id": "corr_dover",
                "corridors": [
                        "corr_dover",
                        "corr_gibraltar",
                        "corr_suez",
                        "corr_babelmandeb"
                ],
                "capacity_bpd": 45500,
                "current_flow_bpd": 35000,
                "distance_km": 23568,
                "lead_time_days": 39,
                "transport_cost_usd_bbl": 11.43,
                "risk_base": 68.8,
                "status": "active",
                "waypoints": [
                        [
                                60.8543,
                                4.7049
                        ],
                        [
                                60.9164,
                                4.1602
                        ],
                        [
                                60.2,
                                4.2
                        ],
                        [
                                59.3054,
                                4.5834
                        ],
                        [
                                58.8,
                                4.8
                        ],
                        [
                                58.068,
                                4.5984
                        ],
                        [
                                56.5696,
                                4.1858
                        ],
                        [
                                56.2498,
                                4.0978
                        ],
                        [
                                55.4414,
                                3.8752
                        ],
                        [
                                55.0956,
                                3.7799
                        ],
                        [
                                54.3066,
                                3.5627
                        ],
                        [
                                53.958,
                                3.4667
                        ],
                        [
                                53.5,
                                3.3406
                        ],
                        [
                                53.0161,
                                3.2073
                        ],
                        [
                                52.368,
                                3.0289
                        ],
                        [
                                52.0175,
                                2.9324
                        ],
                        [
                                51.9,
                                2.9
                        ],
                        [
                                51.6089,
                                2.3601
                        ],
                        [
                                51.2359,
                                1.869
                        ],
                        [
                                51.0724,
                                1.6485
                        ],
                        [
                                50.9611,
                                1.4983
                        ],
                        [
                                50.8,
                                1.3
                        ],
                        [
                                50.7653,
                                1.1939
                        ],
                        [
                                50.5034,
                                0.3929
                        ],
                        [
                                50.2627,
                                -0.3434
                        ],
                        [
                                50.1965,
                                -0.546
                        ],
                        [
                                50.1555,
                                -0.6715
                        ],
                        [
                                49.95,
                                -1.3
                        ],
                        [
                                49.8951,
                                -1.4798
                        ],
                        [
                                49.8382,
                                -1.6657
                        ],
                        [
                                49.7564,
                                -1.9337
                        ],
                        [
                                49.7386,
                                -1.992
                        ],
                        [
                                49.6164,
                                -2.3919
                        ],
                        [
                                49.3704,
                                -3.197
                        ],
                        [
                                49.1292,
                                -3.9862
                        ],
                        [
                                49.1157,
                                -4.0304
                        ],
                        [
                                49.0424,
                                -4.2705
                        ],
                        [
                                48.7999,
                                -5.064
                        ],
                        [
                                48.6667,
                                -5.5
                        ],
                        [
                                47.3401,
                                -6.6989
                        ],
                        [
                                45.6688,
                                -7.955
                        ],
                        [
                                44.9348,
                                -8.4958
                        ],
                        [
                                43.9249,
                                -9.0199
                        ],
                        [
                                43.6885,
                                -9.1426
                        ],
                        [
                                43,
                                -9.5
                        ],
                        [
                                40.7798,
                                -9.9844
                        ],
                        [
                                38.5,
                                -9.6
                        ],
                        [
                                37.7816,
                                -9.4521
                        ],
                        [
                                36.8,
                                -9.25
                        ],
                        [
                                36.5497,
                                -8.2195
                        ],
                        [
                                36.3191,
                                -7.2697
                        ],
                        [
                                35.95,
                                -5.75
                        ],
                        [
                                35.9688,
                                -5.3549
                        ],
                        [
                                35.9729,
                                -5.2694
                        ],
                        [
                                36,
                                -4.7
                        ],
                        [
                                36.1565,
                                -3.683
                        ],
                        [
                                36.2209,
                                -3.2642
                        ],
                        [
                                36.3245,
                                -2.5907
                        ],
                        [
                                36.3777,
                                -2.2448
                        ],
                        [
                                36.4732,
                                -1.6244
                        ],
                        [
                                36.6667,
                                -0.3667
                        ],
                        [
                                37.2,
                                3.1
                        ],
                        [
                                37.4,
                                7.5
                        ],
                        [
                                37.4821,
                                10.373
                        ],
                        [
                                37.5,
                                11
                        ],
                        [
                                37.4549,
                                11.1722
                        ],
                        [
                                37.2832,
                                11.8278
                        ],
                        [
                                37.2155,
                                12.0863
                        ],
                        [
                                37.2091,
                                12.1106
                        ],
                        [
                                36.9071,
                                13.2638
                        ],
                        [
                                36.4,
                                15.2
                        ],
                        [
                                36.0869,
                                16.7266
                        ],
                        [
                                35.8457,
                                17.9021
                        ],
                        [
                                35.1267,
                                21.4074
                        ],
                        [
                                34.8,
                                23
                        ],
                        [
                                34.1874,
                                24.9267
                        ],
                        [
                                34.0119,
                                25.4787
                        ],
                        [
                                33.7488,
                                26.3064
                        ],
                        [
                                33.2196,
                                27.9275
                        ],
                        [
                                33.1158,
                                28.2124
                        ],
                        [
                                32.8634,
                                28.9055
                        ],
                        [
                                32.3161,
                                30.4084
                        ],
                        [
                                31.7,
                                32.1
                        ],
                        [
                                31.3364,
                                32.3599
                        ],
                        [
                                31.1029,
                                32.3101
                        ],
                        [
                                30.3184,
                                32.3822
                        ],
                        [
                                30.214,
                                32.558
                        ],
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                14.1436,
                                49.5581
                        ],
                        [
                                16.2,
                                54.2
                        ],
                        [
                                17.3839,
                                56.876
                        ],
                        [
                                18.7425,
                                58.1918
                        ],
                        [
                                20,
                                59
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                22.8425,
                                64.447
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_039",
                "from_node": "sup_azerbaijan",
                "to_node": "port_mundra",
                "corridor": "Turkish Straits + Gibraltar Strait + Suez Canal + Bab el-Mandeb",
                "corridor_id": "corr_turkish",
                "corridors": [
                        "corr_turkish",
                        "corr_gibraltar",
                        "corr_suez",
                        "corr_babelmandeb"
                ],
                "capacity_bpd": 39000,
                "current_flow_bpd": 30000,
                "distance_km": 18472,
                "lead_time_days": 31,
                "transport_cost_usd_bbl": 9.39,
                "risk_base": 75.5,
                "status": "active",
                "waypoints": [
                        [
                                40.2124,
                                49.9329
                        ],
                        [
                                40.2967,
                                50.8503
                        ],
                        [
                                41.5061,
                                50.7656
                        ],
                        [
                                43.2649,
                                49.3444
                        ],
                        [
                                45.1174,
                                47.8023
                        ],
                        [
                                45.3943,
                                47.7826
                        ],
                        [
                                45.682,
                                47.6988
                        ],
                        [
                                45.7219,
                                47.6375
                        ],
                        [
                                45.7682,
                                47.6457
                        ],
                        [
                                45.8065,
                                47.6842
                        ],
                        [
                                45.8477,
                                47.6715
                        ],
                        [
                                45.8803,
                                47.6224
                        ],
                        [
                                45.9386,
                                47.6623
                        ],
                        [
                                45.9749,
                                47.63
                        ],
                        [
                                45.9816,
                                47.6945
                        ],
                        [
                                46.0283,
                                47.7048
                        ],
                        [
                                46.0993,
                                47.7426
                        ],
                        [
                                46.1502,
                                47.8174
                        ],
                        [
                                46.1926,
                                47.849
                        ],
                        [
                                46.2126,
                                47.9088
                        ],
                        [
                                46.3921,
                                48.0394
                        ],
                        [
                                46.4603,
                                47.9762
                        ],
                        [
                                46.5246,
                                48.0339
                        ],
                        [
                                46.5416,
                                48.0174
                        ],
                        [
                                46.5813,
                                47.9062
                        ],
                        [
                                46.653,
                                47.8924
                        ],
                        [
                                46.7473,
                                47.832
                        ],
                        [
                                46.8589,
                                47.7147
                        ],
                        [
                                46.8439,
                                47.6049
                        ],
                        [
                                46.9565,
                                47.6049
                        ],
                        [
                                47.2185,
                                47.0775
                        ],
                        [
                                47.2968,
                                47.1215
                        ],
                        [
                                47.4271,
                                46.9786
                        ],
                        [
                                47.4271,
                                46.8743
                        ],
                        [
                                47.7237,
                                46.5502
                        ],
                        [
                                47.8603,
                                46.3524
                        ],
                        [
                                47.9487,
                                46.1547
                        ],
                        [
                                48.2058,
                                46.1766
                        ],
                        [
                                48.2409,
                                46.0042
                        ],
                        [
                                48.3232,
                                45.8888
                        ],
                        [
                                48.4664,
                                45.5633
                        ],
                        [
                                48.4081,
                                45.3683
                        ],
                        [
                                48.4746,
                                45.0978
                        ],
                        [
                                48.438,
                                44.9769
                        ],
                        [
                                48.4772,
                                44.9055
                        ],
                        [
                                48.5382,
                                44.6254
                        ],
                        [
                                48.5305,
                                44.5571
                        ],
                        [
                                48.4846,
                                44.552
                        ],
                        [
                                48.425,
                                44.5036
                        ],
                        [
                                48.422,
                                44.483
                        ],
                        [
                                48.4685,
                                44.3471
                        ],
                        [
                                48.494,
                                44.2068
                        ],
                        [
                                48.5486,
                                44.1601
                        ],
                        [
                                48.625,
                                44.064
                        ],
                        [
                                48.6822,
                                43.9674
                        ],
                        [
                                48.6541,
                                43.6948
                        ],
                        [
                                48.4861,
                                43.3202
                        ],
                        [
                                47.7673,
                                42.728
                        ],
                        [
                                47.56,
                                42.0908
                        ],
                        [
                                47.5823,
                                40.9153
                        ],
                        [
                                47.4635,
                                40.5088
                        ],
                        [
                                47.2252,
                                40.2012
                        ],
                        [
                                47.1953,
                                39.6958
                        ],
                        [
                                47.0757,
                                39.2673
                        ],
                        [
                                47.104,
                                39.0431
                        ],
                        [
                                46.8238,
                                37.6629
                        ],
                        [
                                45.6212,
                                36.8592
                        ],
                        [
                                45,
                                36.4
                        ],
                        [
                                43,
                                33
                        ],
                        [
                                41.2424,
                                29.1324
                        ],
                        [
                                41.1863,
                                29.096
                        ],
                        [
                                41.1521,
                                29.0505
                        ],
                        [
                                41.1178,
                                29.0705
                        ],
                        [
                                41.0505,
                                29.0423
                        ],
                        [
                                41.0279,
                                28.995
                        ],
                        [
                                40.9716,
                                28.9777
                        ],
                        [
                                40.8222,
                                28.5015
                        ],
                        [
                                40.8058,
                                28.4495
                        ],
                        [
                                40.605,
                                27.2776
                        ],
                        [
                                40.4407,
                                26.7682
                        ],
                        [
                                40.1,
                                26.2
                        ],
                        [
                                39.9929,
                                26.1436
                        ],
                        [
                                39.7844,
                                26.0975
                        ],
                        [
                                39.495,
                                25.9535
                        ],
                        [
                                39.2374,
                                25.8253
                        ],
                        [
                                39.136,
                                25.8305
                        ],
                        [
                                38.8895,
                                26.023
                        ],
                        [
                                38.7165,
                                26.158
                        ],
                        [
                                38.5234,
                                26.3087
                        ],
                        [
                                38.4379,
                                26.2698
                        ],
                        [
                                38.339,
                                26.1849
                        ],
                        [
                                38.2533,
                                26.1727
                        ],
                        [
                                37.8134,
                                26.3662
                        ],
                        [
                                37.2667,
                                26.4301
                        ],
                        [
                                37.009,
                                26.6359
                        ],
                        [
                                36.5471,
                                27.0028
                        ],
                        [
                                36.4985,
                                27.0304
                        ],
                        [
                                36.2,
                                27.2
                        ],
                        [
                                35.8802,
                                27.5482
                        ],
                        [
                                35.2993,
                                28.1807
                        ],
                        [
                                34.656,
                                28.8812
                        ],
                        [
                                34.5797,
                                28.9643
                        ],
                        [
                                34.0004,
                                29.5952
                        ],
                        [
                                33.9013,
                                29.703
                        ],
                        [
                                32.9863,
                                30.6994
                        ],
                        [
                                32.9251,
                                30.766
                        ],
                        [
                                31.7,
                                32.1
                        ],
                        [
                                31.3364,
                                32.3599
                        ],
                        [
                                31.1029,
                                32.3101
                        ],
                        [
                                30.3184,
                                32.3822
                        ],
                        [
                                30.214,
                                32.558
                        ],
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                14.1436,
                                49.5581
                        ],
                        [
                                16.2,
                                54.2
                        ],
                        [
                                17.3839,
                                56.876
                        ],
                        [
                                18.7425,
                                58.1918
                        ],
                        [
                                20,
                                59
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                22.8425,
                                64.447
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_040",
                "from_node": "sup_algeria",
                "to_node": "port_mundra",
                "corridor": "Gibraltar Strait + Suez Canal + Bab el-Mandeb",
                "corridor_id": "corr_gibraltar",
                "corridors": [
                        "corr_gibraltar",
                        "corr_suez",
                        "corr_babelmandeb"
                ],
                "capacity_bpd": 32500,
                "current_flow_bpd": 25000,
                "distance_km": 16379,
                "lead_time_days": 27,
                "transport_cost_usd_bbl": 8.55,
                "risk_base": 67.1,
                "status": "active",
                "waypoints": [
                        [
                                35.8523,
                                -0.1387
                        ],
                        [
                                36.2,
                                -0.6
                        ],
                        [
                                37.2,
                                3.1
                        ],
                        [
                                37.4,
                                7.5
                        ],
                        [
                                37.4821,
                                10.373
                        ],
                        [
                                37.5,
                                11
                        ],
                        [
                                37.4549,
                                11.1722
                        ],
                        [
                                37.2832,
                                11.8278
                        ],
                        [
                                37.2155,
                                12.0863
                        ],
                        [
                                37.2091,
                                12.1106
                        ],
                        [
                                36.9071,
                                13.2638
                        ],
                        [
                                36.4,
                                15.2
                        ],
                        [
                                36.0869,
                                16.7266
                        ],
                        [
                                35.8457,
                                17.9021
                        ],
                        [
                                35.1267,
                                21.4074
                        ],
                        [
                                34.8,
                                23
                        ],
                        [
                                34.1874,
                                24.9267
                        ],
                        [
                                34.0119,
                                25.4787
                        ],
                        [
                                33.7488,
                                26.3064
                        ],
                        [
                                33.2196,
                                27.9275
                        ],
                        [
                                33.1158,
                                28.2124
                        ],
                        [
                                32.8634,
                                28.9055
                        ],
                        [
                                32.3161,
                                30.4084
                        ],
                        [
                                31.7,
                                32.1
                        ],
                        [
                                31.3364,
                                32.3599
                        ],
                        [
                                31.1029,
                                32.3101
                        ],
                        [
                                30.3184,
                                32.3822
                        ],
                        [
                                30.214,
                                32.558
                        ],
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                14.1436,
                                49.5581
                        ],
                        [
                                16.2,
                                54.2
                        ],
                        [
                                17.3839,
                                56.876
                        ],
                        [
                                18.7425,
                                58.1918
                        ],
                        [
                                20,
                                59
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                22.8425,
                                64.447
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_041",
                "from_node": "sup_libya",
                "to_node": "port_mundra",
                "corridor": "Gibraltar Strait + Suez Canal + Bab el-Mandeb",
                "corridor_id": "corr_gibraltar",
                "corridors": [
                        "corr_gibraltar",
                        "corr_suez",
                        "corr_babelmandeb"
                ],
                "capacity_bpd": 26000,
                "current_flow_bpd": 20000,
                "distance_km": 13109,
                "lead_time_days": 22,
                "transport_cost_usd_bbl": 7.24,
                "risk_base": 65.2,
                "status": "active",
                "waypoints": [
                        [
                                31.2284,
                                19.2928
                        ],
                        [
                                32.4089,
                                19.3717
                        ],
                        [
                                32.5,
                                19.9
                        ],
                        [
                                33.3,
                                22
                        ],
                        [
                                32.7647,
                                23.8248
                        ],
                        [
                                32.5771,
                                24.4643
                        ],
                        [
                                32.2,
                                25.75
                        ],
                        [
                                31.8094,
                                29.2654
                        ],
                        [
                                31.7883,
                                29.4551
                        ],
                        [
                                31.75,
                                29.8
                        ],
                        [
                                31.7441,
                                30.0725
                        ],
                        [
                                31.7,
                                32.1
                        ],
                        [
                                31.3364,
                                32.3599
                        ],
                        [
                                31.1029,
                                32.3101
                        ],
                        [
                                30.3184,
                                32.3822
                        ],
                        [
                                30.214,
                                32.558
                        ],
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                14.1436,
                                49.5581
                        ],
                        [
                                16.2,
                                54.2
                        ],
                        [
                                17.3839,
                                56.876
                        ],
                        [
                                18.7425,
                                58.1918
                        ],
                        [
                                20,
                                59
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                22.8425,
                                64.447
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_042",
                "from_node": "sup_ecuador",
                "to_node": "port_mundra",
                "corridor": "Panama Canal + Strait of Malacca",
                "corridor_id": "corr_panama",
                "corridors": [
                        "corr_panama",
                        "corr_malacca"
                ],
                "capacity_bpd": 19500,
                "current_flow_bpd": 15000,
                "distance_km": 33814,
                "lead_time_days": 56,
                "transport_cost_usd_bbl": 15.53,
                "risk_base": 52.1,
                "status": "active",
                "waypoints": [
                        [
                                1.2,
                                -80.3
                        ],
                        [
                                1.8484,
                                -81.1762
                        ],
                        [
                                3.0505,
                                -80.9033
                        ],
                        [
                                5.195,
                                -80.4128
                        ],
                        [
                                7.4224,
                                -79.6729
                        ],
                        [
                                8.6,
                                -79.5
                        ],
                        [
                                8.7966,
                                -79.4941
                        ],
                        [
                                8.9927,
                                -79.5859
                        ],
                        [
                                9.036,
                                -79.6417
                        ],
                        [
                                9.1064,
                                -79.6893
                        ],
                        [
                                9.1182,
                                -79.7414
                        ],
                        [
                                9.1183,
                                -79.8032
                        ],
                        [
                                9.173,
                                -79.8213
                        ],
                        [
                                9.2082,
                                -79.9006
                        ],
                        [
                                9.75,
                                -80
                        ],
                        [
                                13.6682,
                                -74.9707
                        ],
                        [
                                13.6778,
                                -74.9584
                        ],
                        [
                                14.9065,
                                -73.284
                        ],
                        [
                                15.6655,
                                -72.2499
                        ],
                        [
                                15.6838,
                                -72.2249
                        ],
                        [
                                16.1571,
                                -71.58
                        ],
                        [
                                16.455,
                                -71.174
                        ],
                        [
                                17.5,
                                -69.75
                        ],
                        [
                                17.9526,
                                -68.6151
                        ],
                        [
                                18.5,
                                -67.95
                        ],
                        [
                                19.0121,
                                -67.0379
                        ],
                        [
                                19.1444,
                                -66.8024
                        ],
                        [
                                19.2237,
                                -66.6611
                        ],
                        [
                                19.3015,
                                -66.5226
                        ],
                        [
                                19.3048,
                                -66.5167
                        ],
                        [
                                19.3358,
                                -66.4615
                        ],
                        [
                                19.3589,
                                -66.4203
                        ],
                        [
                                19.3949,
                                -66.3562
                        ],
                        [
                                19.4166,
                                -66.3175
                        ],
                        [
                                19.4554,
                                -66.2484
                        ],
                        [
                                19.8882,
                                -65.4776
                        ],
                        [
                                20.3258,
                                -64.6983
                        ],
                        [
                                21.8778,
                                -61.7714
                        ],
                        [
                                22.7717,
                                -60.0008
                        ],
                        [
                                23.4308,
                                -58.6758
                        ],
                        [
                                23.7856,
                                -57.9624
                        ],
                        [
                                25.047,
                                -55.2385
                        ],
                        [
                                25.1967,
                                -54.9153
                        ],
                        [
                                25.3026,
                                -54.6867
                        ],
                        [
                                26.9387,
                                -50.8793
                        ],
                        [
                                27.2826,
                                -50.0008
                        ],
                        [
                                28.079,
                                -47.9664
                        ],
                        [
                                28.3801,
                                -47.1972
                        ],
                        [
                                29.7204,
                                -43.4184
                        ],
                        [
                                30.0448,
                                -42.3967
                        ],
                        [
                                30.6237,
                                -40.5736
                        ],
                        [
                                30.8057,
                                -40.0003
                        ],
                        [
                                31.1085,
                                -38.9804
                        ],
                        [
                                32.0633,
                                -35.5717
                        ],
                        [
                                32.7925,
                                -32.5684
                        ],
                        [
                                32.8003,
                                -32.5364
                        ],
                        [
                                33.0496,
                                -31.5096
                        ],
                        [
                                33.3597,
                                -30.0014
                        ],
                        [
                                33.9022,
                                -27.3629
                        ],
                        [
                                34.0922,
                                -26.2359
                        ],
                        [
                                34.6142,
                                -23.1406
                        ],
                        [
                                34.7255,
                                -22.2964
                        ],
                        [
                                34.9405,
                                -20.6651
                        ],
                        [
                                35.0042,
                                -20.1813
                        ],
                        [
                                35.0278,
                                -20.0021
                        ],
                        [
                                35.1792,
                                -18.8537
                        ],
                        [
                                35.498,
                                -15.5078
                        ],
                        [
                                35.5925,
                                -14.5159
                        ],
                        [
                                35.6445,
                                -13.6341
                        ],
                        [
                                35.6959,
                                -12.7612
                        ],
                        [
                                35.8502,
                                -10.1424
                        ],
                        [
                                35.8738,
                                -9.1045
                        ],
                        [
                                35.8799,
                                -8.8337
                        ],
                        [
                                35.8817,
                                -8.7569
                        ],
                        [
                                35.8945,
                                -8.1909
                        ],
                        [
                                35.9104,
                                -7.4941
                        ],
                        [
                                35.95,
                                -5.75
                        ],
                        [
                                35.9688,
                                -5.3549
                        ],
                        [
                                35.9729,
                                -5.2694
                        ],
                        [
                                36,
                                -4.7
                        ],
                        [
                                36.1565,
                                -3.683
                        ],
                        [
                                36.2209,
                                -3.2642
                        ],
                        [
                                36.3245,
                                -2.5907
                        ],
                        [
                                36.3777,
                                -2.2448
                        ],
                        [
                                36.4732,
                                -1.6244
                        ],
                        [
                                36.6667,
                                -0.3667
                        ],
                        [
                                37.2,
                                3.1
                        ],
                        [
                                37.4,
                                7.5
                        ],
                        [
                                37.4821,
                                10.373
                        ],
                        [
                                37.5,
                                11
                        ],
                        [
                                37.4549,
                                11.1722
                        ],
                        [
                                37.2832,
                                11.8278
                        ],
                        [
                                37.2155,
                                12.0863
                        ],
                        [
                                37.2091,
                                12.1106
                        ],
                        [
                                36.9071,
                                13.2638
                        ],
                        [
                                36.4,
                                15.2
                        ],
                        [
                                36.0869,
                                16.7266
                        ],
                        [
                                35.8457,
                                17.9021
                        ],
                        [
                                35.1267,
                                21.4074
                        ],
                        [
                                34.8,
                                23
                        ],
                        [
                                34.1874,
                                24.9267
                        ],
                        [
                                34.0119,
                                25.4787
                        ],
                        [
                                33.7488,
                                26.3064
                        ],
                        [
                                33.2196,
                                27.9275
                        ],
                        [
                                33.1158,
                                28.2124
                        ],
                        [
                                32.8634,
                                28.9055
                        ],
                        [
                                32.3161,
                                30.4084
                        ],
                        [
                                31.7,
                                32.1
                        ],
                        [
                                31.3364,
                                32.3599
                        ],
                        [
                                31.1029,
                                32.3101
                        ],
                        [
                                30.3184,
                                32.3822
                        ],
                        [
                                30.214,
                                32.558
                        ],
                        [
                                29.7,
                                32.6
                        ],
                        [
                                28.4445,
                                33.2336
                        ],
                        [
                                27,
                                34.5
                        ],
                        [
                                23.6,
                                37
                        ],
                        [
                                22.2107,
                                37.7865
                        ],
                        [
                                20.8075,
                                38.573
                        ],
                        [
                                17.0988,
                                41.001
                        ],
                        [
                                14.5091,
                                42.3413
                        ],
                        [
                                13.6761,
                                42.5411
                        ],
                        [
                                12.7,
                                43.3
                        ],
                        [
                                12.4044,
                                43.7466
                        ],
                        [
                                12,
                                45
                        ],
                        [
                                14.1436,
                                49.5581
                        ],
                        [
                                16.2,
                                54.2
                        ],
                        [
                                17.3839,
                                56.876
                        ],
                        [
                                18.7425,
                                58.1918
                        ],
                        [
                                20,
                                59
                        ],
                        [
                                21.4404,
                                62.376
                        ],
                        [
                                22.8425,
                                64.447
                        ],
                        [
                                24.3,
                                66.6
                        ],
                        [
                                22.543,
                                68.7195
                        ],
                        [
                                22.5734,
                                69.4446
                        ]
                ]
        },
        {
                "_id": "route_043",
                "from_node": "sup_malaysia",
                "to_node": "port_kakinada",
                "corridor": "Strait of Malacca",
                "corridor_id": "corr_malacca",
                "corridors": [
                        "corr_malacca"
                ],
                "capacity_bpd": 19500,
                "current_flow_bpd": 15000,
                "distance_km": 5716,
                "lead_time_days": 10,
                "transport_cost_usd_bbl": 3.49,
                "risk_base": 29.1,
                "status": "active",
                "waypoints": [
                        [
                                1.3756,
                                104.0265
                        ],
                        [
                                1.2493,
                                104.1458
                        ],
                        [
                                1.1714,
                                103.8611
                        ],
                        [
                                1.1,
                                103.6
                        ],
                        [
                                2,
                                102
                        ],
                        [
                                2.5861,
                                101.3164
                        ],
                        [
                                3.2,
                                100.6
                        ],
                        [
                                4.0845,
                                99.7638
                        ],
                        [
                                5.8117,
                                98.1281
                        ],
                        [
                                10.1365,
                                92.3346
                        ],
                        [
                                13.2644,
                                88.9733
                        ],
                        [
                                13,
                                88
                        ],
                        [
                                13.7726,
                                86.4549
                        ],
                        [
                                14.4222,
                                85.1557
                        ],
                        [
                                15.2718,
                                83.4593
                        ],
                        [
                                16.7083,
                                82.8282
                        ],
                        [
                                16.999,
                                82.3714
                        ]
                ]
        },
        {
                "_id": "route_044",
                "from_node": "sup_indonesia",
                "to_node": "port_paradip",
                "corridor": "Strait of Malacca",
                "corridor_id": "corr_malacca",
                "corridors": [
                        "corr_malacca"
                ],
                "capacity_bpd": 13000,
                "current_flow_bpd": 10000,
                "distance_km": 6955,
                "lead_time_days": 12,
                "transport_cost_usd_bbl": 3.98,
                "risk_base": 31.1,
                "status": "active",
                "waypoints": [
                        [
                                -6.0832,
                                106.8798
                        ],
                        [
                                -5.9166,
                                106.8681
                        ],
                        [
                                -5.2,
                                106.8
                        ],
                        [
                                -3,
                                106.1
                        ],
                        [
                                -2.8923,
                                105.9052
                        ],
                        [
                                -2.3456,
                                105.6863
                        ],
                        [
                                -2.169,
                                105.0632
                        ],
                        [
                                -0.5866,
                                104.1371
                        ],
                        [
                                0.5685,
                                103.8428
                        ],
                        [
                                0.7388,
                                103.623
                        ],
                        [
                                1.1,
                                103.6
                        ],
                        [
                                2,
                                102
                        ],
                        [
                                2.5861,
                                101.3164
                        ],
                        [
                                3.2,
                                100.6
                        ],
                        [
                                4.0845,
                                99.7638
                        ],
                        [
                                5.8117,
                                98.1281
                        ],
                        [
                                14.5492,
                                93.6386
                        ],
                        [
                                18.8489,
                                89.7274
                        ],
                        [
                                21,
                                88
                        ]
                ]
        },
        {
                "_id": "route_045",
                "from_node": "sup_canada",
                "to_node": "port_mundra",
                "corridor": "Panama Canal + Strait of Malacca",
                "corridor_id": "corr_panama",
                "corridors": [
                        "corr_panama",
                        "corr_malacca"
                ],
                "capacity_bpd": 6500,
                "current_flow_bpd": 5000,
                "distance_km": 34384,
                "lead_time_days": 57,
                "transport_cost_usd_bbl": 15.75,
                "risk_base": 47.9,
                "status": "active",
                "waypoints": [
                        [
                                49.3153,
                                -123.3147
                        ],
                        [
                                49.0699,
                                -123.3795
                        ],
                        [
                                48.8551,
                                -123.051
                        ],
                        [
                                48.7977,
                                -123.0054
                        ],
                        [
                                48.7325,
                                -123.006
                        ],
                        [
                                48.7351,
                                -123.0327
                        ],
                        [
                                48.7146,
                                -123.2549
                        ],
                        [
                                48.5113,
                                -123.2018
                        ],
                        [
                                48.3854,
                                -123.2117
                        ],
                        [
                                48.3818,
                                -123.3971
                        ],
                        [
                                48.2308,
                                -123.4798
                        ],
                        [
                                48.2659,
                                -123.9732
                        ],
                        [
                                48.4862,
                                -124.7292
                        ],
                        [
                                48.5683,
                                -125.5016
                        ],
                        [
                                50,
                                -130
                        ],
                        [
                                50,
                                -135.0568
                        ],
                        [
                                50,
                                -137.5416
                        ],
                        [
                                50,
                                -140
                        ],
                        [
                                50.7028,
                                -144.0492
                        ],
                        [
                                51.23,
                                -149.8894
                        ],
                        [
                                51.2678,
                                -150.3081
                        ],
                        [
                                51.4967,
                                -152.8431
                        ],
                        [
                                51.6668,
                                -154.7279
                        ],
                        [
                                51.7758,
                                -158.3055
                        ],
                        [
                                51.8301,
                                -160.0892
                        ],
                        [
                                51.7485,
                                -161.8405
                        ],
                        [
                                51.6826,
                                -163.2549
                        ],
                        [
                                51.5931,
                                -165.1749
                        ],
                        [
                                51.4861,
                                -167.4716
                        ],
                        [
                                51.0799,
                                -168.081
                        ],
                        [
                                51.0966,
                                -168.2056
                        ],
                        [
                                51.2951,
                                -171.5552
                        ],
                        [
                                50.5587,
                                -176.9962
                        ],
                        [
                                50.2529,
                                -179.4858
                        ],
                        [
                                50,
                                -180
                        ],
                        [
                                50,
                                -180
                        ],
                        [
                                44.8596,
                                -195.8168
                        ],
                        [
                                40,
                                -210
                        ],
                        [
                                38.0301,
                                -214.4708
                        ],
                        [
                                35.6828,
                                -218.9779
                        ],
                        [
                                35.0862,
                                -219.5233
                        ],
                        [
                                34.8,
                                -220.1
                        ],
                        [
                                34.7125,
                                -220.3688
                        ],
                        [
                                34.683,
                                -220.4494
                        ],
                        [
                                34.605,
                                -220.6989
                        ],
                        [
                                34.3956,
                                -221.0449
                        ],
                        [
                                32.4438,
                                -223.6732
                        ],
                        [
                                30.7103,
                                -225.9601
                        ],
                        [
                                29.4912,
                                -227.6677
                        ],
                        [
                                25.9803,
                                -232.1631
                        ],
                        [
                                25.9851,
                                -232.6243
                        ],
                        [
                                25.0259,
                                -234.8108
                        ],
                        [
                                24.8093,
                                -235.4111
                        ],
                        [
                                24.4697,
                                -236.022
                        ],
                        [
                                24.5722,
                                -236.5818
                        ],
                        [
                                23.0909,
                                -237.881
                        ],
                        [
                                21.8154,
                                -238.5368
                        ],
                        [
                                19,
                                -240
                        ],
                        [
                                17.9093,
                                -240.9612
                        ],
                        [
                                16.9083,
                                -241.8381
                        ],
                        [
                                13.3608,
                                -244.9555
                        ],
                        [
                                9.7977,
                                -248.0866
                        ],
                        [
                                7.5453,
                                -250.0659
                        ],
                        [
                                1.3413,
                                -255.5177
                        ],
                        [
                                1.2493,
                                -255.8542
                        ],
                        [
                                1.1714,
                                -256.1389
                        ],
                        [
                                1.1,
                                -256.4
                        ],
                        [
                                2,
                                -258
                        ],
                        [
                                2.5861,
                                -258.6836
                        ],
                        [
                                3.2,
                                -259.4
                        ],
                        [
                                4.0845,
                                -260.2362
                        ],
                        [
                                5.8117,
                                -261.8719
                        ],
                        [
                                6.1571,
                                -265.6736
                        ],
                        [
                                6.4664,
                                -270
                        ],
                        [
                                6.1983,
                                -274.0521
                        ],
                        [
                                5.9,
                                -278.1
                        ],
                        [
                                5.8,
                                -279.9
                        ],
                        [
                                6.6749,
                                -281.1311
                        ],
                        [
                                8,
                                -283
                        ],
                        [
                                9.7,
                                -284.7
                        ],
                        [
                                12.7734,
                                -285.8665
                        ],
                        [
                                15.3,
                                -287
                        ],
                        [
                                19,
                                -287.6
                        ],
                        [
                                20,
                                -290
                        ],
                        [
                                20.8093,
                                -290.4075
                        ],
                        [
                                22.543,
                                -291.2805
                        ],
                        [
                                22.5734,
                                -290.5554
                        ]
                ]
        }
]
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
    try:
        from scripts.seed_historical_news import TIER_1_HISTORICAL_EVENTS, TIER_2_HISTORICAL_EVENTS
        risk_events = risk_events + TIER_1_HISTORICAL_EVENTS + TIER_2_HISTORICAL_EVENTS
    except Exception:
        pass

    countries = [
        {
                "_id": "IND",
                "name": "India",
                "iso_code": "IND",
                "is_import_dependent": true,
                "daily_consumption_bpd": 5340000,
                "total_daily_import_bpd": 4700000,
                "strategic_reserve_bbl": 42000000,
                "reserve_safety_floor_bbl": 8000000,
                "reserve_days": 9.5
        }
]

    collections = {
        "suppliers": suppliers,
        "ports": ports,
        "refineries": refineries,
        "corridors": corridors,
        "routes": routes,
        "scenario_templates": scenario_templates,
        "risk_events": risk_events,
        "countries": countries,
        "risk_scores": []
    }

    for name, docs in collections.items():
        coll = db[name]
        coll.delete_many({})
        if docs:
            coll.insert_many(docs)
            print(f"Collection '{name}': seeded {len(docs)} documents into '{DATABASE_NAME}'.")
        else:
            print(f"Collection '{name}': cleared.")

    print("\nDatabase seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
