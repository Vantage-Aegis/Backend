import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.simulation.scenario_simulator import run_scenario, ScenarioParams
import os
from dotenv import load_dotenv

load_dotenv("Backend/.env")
db_uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
db_name = os.environ.get("DATABASE_NAME", "vantage_db")
client = AsyncIOMotorClient(db_uri)
db = client[db_name]

async def test():
    params = ScenarioParams(
        event_type="hormuz_closure",
        affected_corridor_id="corr_hormuz",
        severity=5,
        duration_days=30,
        demand_delta_pct=0.0
    )
    res = await run_scenario(params, db)
    print("Success:", res["scenario_id"])
    print("Risk:", res["risk"])
    print("Deficit:", res["supply_impact"]["deficit_bpd"])
    
if __name__ == "__main__":
    asyncio.run(test())
