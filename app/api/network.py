from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.schemas.network import NetworkResponse
from app.services.twin_service import build_network

router = APIRouter(prefix="/api/network", tags=["Digital Twin Network"])

@router.get("", response_model=NetworkResponse)
async def get_network(db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Returns full digital twin network graph (nodes and edges) for Leaflet map renderer.
    """
    suppliers_docs = await db.suppliers.find({}).to_list(length=100)
    ports_docs = await db.ports.find({}).to_list(length=100)
    refineries_docs = await db.refineries.find({}).to_list(length=100)
    routes_docs = await db.routes.find({}).to_list(length=100)

    network_data = build_network(suppliers_docs, ports_docs, refineries_docs, routes_docs)
    return NetworkResponse(**network_data)
