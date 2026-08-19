# Vantage Backend — Energy Supply Chain Resilience System

This is the backend service for the Vantage AI-Driven Energy Supply Chain Resilience system. It provides real-time supply chain digital twin simulation, geopolitical risk intelligence, and AI-powered procurement rerouting recommendations for import-dependent economies like India.

## 🚀 Installation & Setup

Follow these steps to deploy and run the backend on any device:

### Prerequisites
- **Python 3.10+**
- A **MongoDB Atlas** cluster URL.
- A **Google Gemini API Key**.

### 1. Clone & Environment Setup
Navigate to the backend directory and set up a virtual environment:
```bash
cd Backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root of the `Backend/` directory (you can copy `.env.example` if it exists). Add the following variables:
```env
MONGODB_URI="mongodb+srv://<user>:<password>@cluster0.xxx.mongodb.net/"
DATABASE_NAME="energy_resilience_db"
GEMINI_API_KEY="your_google_gemini_api_key_here"
LLM_MODEL="gemini-2.5-flash"
```

### 4. Seed the Database
Initialize your MongoDB database with the required mock data (suppliers, ports, refineries, corridors, routes, and India's baseline country metrics):
```bash
python scripts/seed.py
```
*Note: This will clear existing data in the database and write fresh documents.*

### 5. Run the Server
Start the FastAPI server:
```bash
uvicorn app.main:app --reload --port 8000
```
The API will be available at `http://localhost:8000`. You can view the interactive Swagger documentation at `http://localhost:8000/docs`.

### 6. Run Tests
Verify the installation by running the test suite:
```bash
pytest tests/ -v
```

---

## 🏗️ Architecture & File Explanations

During the recent comprehensive audit, we thoroughly updated the backend to ensure it aligns perfectly with the system specifications, is completely secure, and runs flawlessly. Below is an explanation of every core component and the specific work completed on them.

### Application Core
- **`app/main.py`**: The FastAPI entry point. It registers all API routers and configures strictly scoped CORS middleware. *(Recent fix: Removed permissive wildcard `*` domains to harden security).*
- **`app/config.py`**: Uses Pydantic to strictly validate environment variables. *(Recent fix: Stripped hardcoded passwords and Gemini keys, forcing the app to read from `.env`).*
- **`app/database.py`**: Manages the `AsyncIOMotorClient` connection to MongoDB. *(Recent fix: Refactored to only use FastAPI's `lifespan` context manager, preventing background connection leaks).*

### Core AI & Algorithms (`app/services/` & `app/simulation/`)
- **`twin_service.py`**: Calculates the geopolitical "Digital Twin" graph of routes, ports, and refineries. *(Recent fix: Refactored disruption propagation to accurately reduce `effective_capacity_bpd`, set edges to `blocked`/`degraded`, and intelligently flag refineries as disrupted only when all supply routes fall).*
- **`risk_engine.py`**: Computes weighted risk scores dynamically based on 8 geopolitical factors. *(Recent fix: Rewritten to use `scoring_utils.py` for accurate min-max normalization and weighted distribution according to the system blueprint).*
- **`recommendation_engine.py`**: The Adaptive Procurement Orchestrator. Ranks alternative crude sources based on lead time, landed cost, and route risk. *(Recent fix: Corrected algorithms that incorrectly hallucinated 400k bpd of spare capacity on blocked routes).*
- **`reserve_optimizer.py`**: The Strategic Reserve Agent. Calculates how many days India's strategic petroleum reserves can offset a supply deficit.
- **`decision_engine.py`**: Combines recommendations from the reserve optimizer and the procurement orchestrator into a top-3 ranked action plan for the dashboard.
- **`scenario_simulator.py`**: Runs "what-if" simulations (like a Strait of Hormuz closure). *(Recent fix: Added robust fallback logic and logging if graph propagation fails to find affected routes).*

### AI Integration (`app/agents/` & `app/utils/`)
- **`utils/llm_client.py`**: The main async HTTP wrapper for connecting to the Gemini API. *(Recent fix: Implemented strict `systemInstruction` support, bumped timeout limits, and added an intelligent retry loop that auto-prompts the AI if it fails to return valid JSON).*
- **`utils/scoring_utils.py`**: *(New)* Contains standard math utilities like `normalize` and `weighted_score` used by all engines.
- **`agents/event_classifier_agent.py`**: An LLM agent that reads live news/events and classifies their threat severity and impacted corridor. *(Recent fix: Prompt-engineered to return a `confidence` metric, which gates low-confidence classifications into a manual `needs_review` state).*
- **`agents/explanation_agent.py`**: An LLM agent that translates complex scenario mathematics into simple, executive-level summaries.

### API Endpoints (`app/api/`)
- **`dashboard.py`**: Aggregates top-level metrics. *(Recent fix: Modified to read real baseline stats from the DB's `countries` collection and generates dynamic risk trend dates rather than hardcoding).*
- **`events.py`**: Ingests new intelligence events. *(Recent fix: Now triggers automatic risk re-computation across the Digital Twin when high-confidence events are detected).*
- **`risk.py`**: Returns and persists risk intelligence scores.
- **`scenarios.py`, `recommendations.py`, `network.py`, etc.**: Thin wrappers that pass incoming REST payload requests down into the business logic services.

### Scripts & Schemas
- **`scripts/seed.py`**: The database hydration script. *(Recent fix: Cleaned out hardcoded URIs. Added the required `countries` and `risk_scores` collections. Rebalanced maritime shipping route distributions to exactly match the 4 Hormuz, 2 Red Sea, 2 Cape, and 2 Direct/Malacca specification).*
- **`app/schemas/`**: Pydantic models mapping incoming requests and responses. *(Recent fix: Updated `EventResponse` to include AI `confidence` and `needs_review` flags).*
- **`tests/`**: The Pytest suite. *(Recent fix: Fully modernized to use FastAPI `TestClient` as a context manager so database lifecycle connections spin up and tear down cleanly during tests).*
