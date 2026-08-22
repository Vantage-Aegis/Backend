from fastapi import APIRouter, Depends
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.schemas.supplier import SupplierResponse

router = APIRouter(prefix="/api/suppliers", tags=["Suppliers"])

@router.get("", response_model=List[SupplierResponse])
async def get_suppliers(db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Returns list of crude suppliers from MongoDB Atlas database.
    """
    cursor = db.suppliers.find({})
    docs = await cursor.to_list(length=100)
    
    routes_cursor = db.routes.find({})
    routes = await routes_cursor.to_list(length=100)
    
    result = []
    for doc in docs:
        supplier_name = doc["name"]
        supplier_id = doc["_id"]
        
        # Check if supplier is blocked
        supplier_routes = [r for r in routes if r.get("from_node") == supplier_id]
        total_routes = len(supplier_routes)
        blocked_routes = sum(1 for r in supplier_routes if r.get("status") == "blocked")
        
        rel_score = doc["reliability_score"]
        if total_routes > 0:
            if blocked_routes == total_routes:
                rel_score = min(rel_score, 0.1)  # Completely blocked
            elif blocked_routes > 0:
                rel_score = min(rel_score, 0.4)  # Partially blocked

        result.append(SupplierResponse(
            _id=doc["_id"],
            name=doc["name"],
            current_export_bpd=doc["current_export_bpd"],
            max_capacity_bpd=doc["max_capacity_bpd"],
            reliability_score=rel_score,
            base_price_usd_bbl=doc["base_price_usd_bbl"],
            lat=doc["lat"],
            lng=doc["lng"]
        ))
    return result
