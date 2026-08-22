<p align="center">
  <img src="https://raw.githubusercontent.com/Vantage-Aegis/Frontend/main/public/logo.png" alt="Vantage Logo" width="80" />
</p>

<h1 align="center">Vantage — Backend</h1>

<p align="center">
  <strong>India's Crude Oil Supply Chain Intelligence Platform</strong>
</p>

<p align="center">
  The AI-driven data processing, geopolitical risk intelligence, and supply chain simulation engine powering the Vantage platform.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/MongoDB-Motor-47A248?logo=mongodb&logoColor=white" alt="MongoDB" />
  <img src="https://img.shields.io/badge/AI-Gemini_2.0_Flash-4285F4?logo=google&logoColor=white" alt="Google Gemini" />
  <img src="https://img.shields.io/badge/ML-XGBoost-blue" alt="XGBoost" />
  <img src="https://img.shields.io/badge/ML-Prophet-blue" alt="Prophet" />
</p>



## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Backend Architecture](#backend-architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Data Sources & Methodology](#data-sources--methodology)
- [API Documentation](#api-documentation)
- [Static vs Real-Time Data](#static-vs-real-time-data)
- [Data Flow](#data-flow)
- [Environment Variables](#environment-variables)
- [Installation & Setup](#installation--setup)
- [Running Locally](#running-locally)
- [Error Handling](#error-handling)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Related Repositories](#related-repositories)
- [Team](#team)

---

## Overview

The **Vantage Backend** is a high-performance Python application built on FastAPI. It acts as the central brain of the Vantage platform, responsible for real-time intelligence gathering, complex geopolitical risk scoring, supply chain disruption simulation, and procurement optimization.

By combining deterministic operations research (like Linear Programming for strategic reserves) with advanced machine learning (XGBoost, Prophet) and Large Language Models (Google Gemini), the backend transforms raw global data into actionable executive intelligence.

---

## Features

### 1. Real-Time Geopolitical Intelligence Poller
**What it does:** Continuously monitors the GDELT v2 Document API (with fallback to Google News RSS) for energy-related geopolitical events.
**How it works:** A background async task (`news_poller.py`) fetches articles every 15 minutes. It uses the Google Gemini LLM via `event_classifier_agent.py` to classify the article's severity, affected corridor, and confidence level.
**Data:** Real-time external API data saved to MongoDB (`risk_events` collection).

### 2. Live Crude Oil Price Tracking
**What it does:** Fetches the daily Brent Crude benchmark price and monitors for volatility.
**How it works:** An async task (`oil_price_poller.py`) fetches daily prices from OilPriceAPI. It also queries pre-computed historical anomaly data from an XGBoost model.
**Data:** Real-time external API data saved to MongoDB (`brent_prices`).

### 3. Supply Chain Digital Twin
**What it does:** Maintains a mathematical graph representation of the global crude oil supply chain relevant to India.
**How it works:** `twin_service.py` constructs a network graph of suppliers (nodes), ports (nodes), refineries (nodes), and maritime corridors (edges). It handles the complex logic of propagating disruptions (e.g., if the Strait of Hormuz is blocked, all connected routes are degraded, and dependent refineries experience capacity drops).
**Data:** Database-backed (seeded configuration of real-world infrastructure).

### 4. Dynamic Risk Engine
**What it does:** Computes weighted vulnerability scores for maritime corridors and supplier nations.
**How it works:** `risk_engine.py` evaluates 8 factors (e.g., geopolitical tension, shipping disruption, dependency percentage). It integrates both deterministic scoring and ML-driven predictions (`xgboost_risk_model.json`), including SHAP value attributions for explainability.
**Data:** Computed on-demand using a combination of database metrics and active news events.

### 5. Disruption Simulator
**What it does:** Calculates the compounding effects of a theoretical supply chain disruption.
**How it works:** `scenario_simulator.py` receives parameters (severity, duration, affected node). It invokes the Digital Twin to propagate the disruption, calculates the crude deficit (bpd), and triggers downstream recommendations.
**Data:** Computed dynamically per user request.

### 6. Strategic Reserve Optimizer
**What it does:** Calculates optimal drawdown schedules for India's Strategic Petroleum Reserves (SPR) to cover supply deficits.
**How it works:** `reserve_optimizer` supports two algorithms: a fast Greedy Proportional heuristic and a strict Linear Programming (LP) model. It calculates daily discharge limits across facilities (Visakhapatnam, Mangalore, Padur).
**Data:** Computed dynamically based on database SPR capacities and simulated deficits.

### 7. Adaptive Procurement Orchestrator
**What it does:** Ranks alternative crude sourcing routes when primary corridors are disrupted.
**How it works:** `recommendation_engine.py` evaluates unblocked routes based on available supplier spare capacity, transit time, landed cost, and route risk, returning a prioritized list.
**Data:** Computed dynamically using Digital Twin state.

### 8. AI Narrative Generation
**What it does:** Translates complex numerical simulation results into a readable executive brief.
**How it works:** `explanation_agent.py` sends the JSON simulation output to Google Gemini with strict system instructions to generate a structured narrative (why it's risky, why routes are recommended, uncertainties). Includes a deterministic fallback if the API fails.
**Data:** LLM-generated text, cached in MongoDB.

---

## Backend Architecture

The backend follows a modular, service-oriented architecture:

* **`app/api/` (Routers):** FastAPI endpoints that validate incoming HTTP requests via Pydantic schemas and route them to business logic.
* **`app/services/` (Core Logic):** The heavy lifting—graph propagation, risk calculation, optimization algorithms, and background data polling.
* **`app/agents/` (AI Integration):** LLM wrappers for specific tasks (event classification, narrative generation).
* **`app/simulation/` (Orchestration):** Connects the various services to execute end-to-end "what-if" scenarios.
* **`app/schemas/` (Models):** Pydantic definitions ensuring strict data validation.
* **`ml/` (Machine Learning):** Training scripts and serialized models (XGBoost, Prophet) for demand forecasting, anomaly detection, and risk scoring.

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Web Framework | FastAPI | High-performance async REST API |
| Python Server | Uvicorn | ASGI server implementation |
| Database | MongoDB (Motor) | Async NoSQL data persistence |
| Data Validation | Pydantic | Schema definition and type checking |
| AI / LLM | Google Gemini 2.0 Flash | Event classification and narrative generation |
| Machine Learning | XGBoost, Prophet, Scikit-learn | Risk modeling, anomaly detection, forecasting |
| External APIs | GDELT, Google News RSS, OilPriceAPI | Live intelligence gathering |
| HTTP Client | HTTPX | Async HTTP requests for polling |
| Testing | Pytest | Unit and integration testing |

---

## Project Structure

```text
Backend/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Environment variable configuration
│   ├── database.py             # MongoDB connection manager
│   ├── api/                    # FastAPI route definitions
│   │   ├── admin.py            # Admin controls and overrides
│   │   ├── dashboard.py        # Aggregated KPI endpoints
│   │   ├── events.py           # News/intelligence feed endpoints
│   │   ├── explain.py          # AI narrative endpoint
│   │   ├── network.py          # Digital Twin graph endpoints
│   │   ├── prices.py           # Crude oil price endpoints
│   │   ├── recommendations.py  # Procurement ranking endpoints
│   │   ├── reserves.py         # Strategic reserve optimization
│   │   ├── risk.py             # Risk scoring endpoints
│   │   ├── routes.py           # Alternative routes endpoints
│   │   ├── scenarios.py        # Disruption simulation endpoints
│   │   └── suppliers.py        # Supplier management endpoints
│   ├── agents/                 # LLM Integrations
│   │   ├── event_classifier_agent.py
│   │   └── explanation_agent.py
│   ├── schemas/                # Pydantic data validation models
│   ├── services/               # Core business logic
│   │   ├── decision_engine.py
│   │   ├── news_poller.py      # Background GDELT/RSS task
│   │   ├── oil_price_poller.py # Background price task
│   │   ├── oil_price_service.py
│   │   ├── recommendation_engine.py
│   │   ├── reserve_optimizer/  # LP and Greedy algorithms
│   │   ├── risk_engine.py      # Weighted risk scoring
│   │   └── twin_service.py     # Supply chain graph logic
│   ├── simulation/
│   │   └── scenario_simulator.py # Orchestrates disruption logic
│   └── utils/
│       ├── llm_client.py       # Wrapper for Gemini API calls
│       └── scoring_utils.py    # Math/normalization helpers
├── data/                       # Processed datasets and ML outputs
├── ml/                         # Machine Learning pipelines
│   ├── models/                 # Serialized XGBoost models (.json/.joblib)
│   ├── train_model1_risk.py    
│   ├── train_model3_forecast.py
│   ├── train_model4_anomaly.py 
│   └── train_model5_ranking.py 
├── scripts/
│   ├── seed.py                 # Database initialization script
│   └── seed_historical_news.py # Populates past events
├── tests/                      # Pytest suite
├── requirements.txt            # Python dependencies
└── .env                        # Environment variables (not in version control)
```

---

## Data Sources & Methodology

> Vantage uses multiple heterogeneous data sources to power its analysis, machine learning models, and real-time features. Detailed information about these sources, including source URLs, datasets, fields, preprocessing methodologies, update frequency, licensing, and limitations, is maintained in a dedicated external document.

**Detailed Data Sources Documentation:**
[View Data Sources & Methodology](https://docs.google.com/document/d/1HVely15othP6V93me_gB-JdQ5FoNl45GNyOwcdvb598/edit?usp=sharing)

*This document is critical for understanding the origin and validity of the data driving the Vantage platform.*

---

## API Documentation

The backend provides a comprehensive REST API. When running locally, interactive documentation is available at `http://localhost:8000/docs` (Swagger UI) and `http://localhost:8000/redoc` (ReDoc).

### Core Endpoints

| Method | Endpoint | Purpose | Authentication |
|--------|----------|---------|----------------|
| GET | `/api/dashboard` | Returns aggregated metrics, KPIs, and overall risk | None |
| GET | `/api/events` | Returns classified risk events (news feed) | None |
| POST | `/api/events/poll` | Triggers an immediate GDELT news fetch | None |
| GET | `/api/prices/latest` | Returns real-time Brent crude price | None |
| GET | `/api/network` | Returns Digital Twin graph (nodes/edges) | None |
| GET | `/api/risk` | Returns risk score for a corridor or supplier | None |
| POST | `/api/scenarios/simulate` | Executes a disruption scenario | None |
| GET | `/api/routes` | Returns ranked alternative routes | None |
| POST | `/api/reserves/optimize` | Computes reserve drawdown schedule | None |
| POST | `/api/explain` | Generates AI executive summary | None |
| POST | `/api/admin/login` | Authenticates administrator | None |
| POST | `/api/admin/entities/{type}/{id}/toggle` | Manually blocks/unblocks supply chain nodes | Bearer Token |

### API Example

**Execute Simulation (`POST /api/scenarios/simulate`)**

Request:
```json
{
  "event_type": "corridor_closure",
  "severity": 100,
  "duration_days": 30,
  "demand_delta_pct": 0,
  "affected_corridor_id": "corr_hormuz"
}
```

Response (Truncated):
```json
{
  "scenario_id": "sim_8f7a2b",
  "risk": {
    "score": 92.5,
    "category": "Critical"
  },
  "supply_impact": {
    "baseline_supply_bpd": 4700000,
    "lost_supply_bpd": 1974000,
    "deficit_bpd": 1974000,
    "price_impact_pct": 22.4
  },
  "alternatives": [ ... ],
  "reserve_plan": {
    "days_of_coverage": 8.5,
    "drawdown_bpd_avg": 232000
  },
  "recommendations": [ ... ]
}
```

---

## Static vs Real-Time Data

Vantage blends pre-configured infrastructure data with real-time intelligence:

| Data Element | Type | Source | Update Mechanism |
|--------------|------|--------|------------------|
| Infrastructure (Ports/Refineries) | Static/Database | Seed Script | Manual DB updates / Admin panel |
| Base Routes & Capacities | Static/Database | Seed Script | Manual DB updates / Admin panel |
| Live News Events | Real-Time | GDELT API / RSS | Async Poller (every 15 mins) |
| Brent Crude Price | Real-Time | OilPriceAPI | Async Poller (every 24 hours) |
| Risk Scores | Computed | Risk Engine | Recomputed on request / event trigger |
| ML Demand Forecast | Static ML Output | Prophet JSON | Updated when model is retrained |
| Price Anomalies | Mixed | XGBoost JSON + Live Price | Historical static + Live eval |
| AI Explanations | Computed LLM | Google Gemini | Generated on-demand, cached in DB |

---

## Data Flow

Example: **Real-Time News Processing Lifecycle**

```text
External Source (GDELT API / Google News RSS)
        ↓
Background Task (`news_poller.py` - fetches every 15m)
        ↓
AI Classification (Gemini LLM extracts severity, location, confidence)
        ↓
Database Insertion (Saved to `risk_events` MongoDB collection)
        ↓
Risk Recomputation (If confidence is high, `risk_engine.py` updates scores)
        ↓
Digital Twin Update (Admin approval engine flags routes as 'degraded'/'blocked')
        ↓
API Response (Frontend fetches updated state via `/api/dashboard`)
```

---

## Environment Variables

Create a `.env` file in the root of the `Backend/` directory.

```env
# Required: MongoDB Connection String
MONGODB_URI="mongodb+srv://<username>:<password>@cluster.mongodb.net/"

# Optional: Database Name (Defaults to energy_resilience_db)
DATABASE_NAME="energy_resilience_db"

# Required: Google Gemini API Key for LLM classification and explanation
GEMINI_API_KEY="your_gemini_api_key"

# Optional: LLM Model (Defaults to gemini-2.0-flash)
LLM_MODEL="gemini-2.0-flash"

# Optional: OilPriceAPI Key for live crude pricing
OIL_PRICE_API_KEY="your_oilprice_api_key"

# Optional: Poller Controls (Default: True)
ENABLE_GDELT_POLLING=True
ENABLE_OIL_PRICE_POLLING=True

# Optional: Admin Password (Defaults to vantage_admin)
ADMIN_PASSWORD="secure_password_here"
```

*If `GEMINI_API_KEY` is missing, the system will fall back to deterministic text templates for explanations.*
*If `OIL_PRICE_API_KEY` is missing, the system will fall back to cached database prices.*

---

## Installation & Setup

### Prerequisites
- **Python 3.10+**
- A **MongoDB Atlas** cluster URL (or local MongoDB instance)
- A **Google Gemini API Key** (from Google AI Studio)

### 1. Clone & Environment Setup
```bash
git clone https://github.com/Vantage-Aegis/Backend.git
cd Backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file as described in the Environment Variables section.

### 4. Seed the Database
Initialize the database with the required mock infrastructure data (suppliers, ports, refineries, routes).
```bash
# Warning: This will drop existing collections in the configured database
python scripts/seed.py
```
*(Optional) Seed historical news events for a richer initial dashboard:*
```bash
python scripts/seed_historical_news.py
```

---

## Running Locally

### Start the Server
Run the FastAPI application using Uvicorn:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.
Background pollers will start automatically upon server launch.

### Run Tests
The backend includes a Pytest suite for core services.
```bash
pytest tests/ -v
```

---

## Error Handling

The backend implements robust error handling:
- **HTTP Exceptions:** Returns standard JSON error responses with proper HTTP status codes (e.g., 404 for not found, 401 for unauthorized).
- **LLM Fallbacks:** If the Gemini API times out, hits rate limits, or returns invalid JSON, `llm_client.py` includes a retry loop. If that fails, deterministic fallback templates are used to prevent system crashes.
- **Poller Resilience:** `news_poller.py` attempts to fetch from GDELT. If GDELT is rate-limiting (429) or times out, it seamlessly falls back to parsing the live Google News RSS feed.
- **Pydantic Validation:** All API requests and LLM JSON outputs are strictly validated against schema definitions.

---

## Security

- **CORS:** Middleware is strictly scoped to specific localhost origins for development. (Must be updated for production).
- **Environment Variables:** No hardcoded secrets. All API keys and database credentials are read from the `.env` file via `pydantic-settings`.
- **Authentication:** The Admin panel endpoints are secured using a Bearer token session mechanism.
- **Input Validation:** Pydantic prevents injection of unexpected data payloads.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `pymongo.errors.ServerSelectionTimeoutError` | Check your `MONGODB_URI`. Ensure your IP address is whitelisted in MongoDB Atlas Network Access. |
| News events aren't updating | Ensure `ENABLE_GDELT_POLLING=True` in `.env`. Check console logs for API timeouts. |
| AI Explanations return basic text | Verify your `GEMINI_API_KEY` is correct and has quota remaining. |
| CORS errors in Frontend | Ensure the frontend is running on an allowed origin (e.g., `http://localhost:5173`) or update `app/main.py`. |
| Port 8000 already in use | Kill the existing process (`lsof -ti:8000 \| xargs kill -9`) or start Uvicorn on a different port (`--port 8001`). |

---

## Related Repositories

- **Frontend:** [github.com/Vantage-Aegis/Frontend](https://github.com/Vantage-Aegis/Frontend)

## Documentation

- **Data Sources & Methodology:** [View Document](https://docs.google.com/document/d/1HVely15othP6V93me_gB-JdQ5FoNl45GNyOwcdvb598/edit?usp=sharing)

---

## Team

### [Kumar Suryanshu](https://github.com/Suryanshu-01)
### [Sridhar Manokaran](https://github.com/sridhar1923)
### [Shiv Thanmay](https://github.com/Shiv-th)
