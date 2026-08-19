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
    
    result = []
    for doc in docs:
        result.append(SupplierResponse(
            _id=doc["_id"],
            name=doc["name"],
            current_export_bpd=doc["current_export_bpd"],
            max_capacity_bpd=doc["max_capacity_bpd"],
            reliability_score=doc["reliability_score"],
            base_price_usd_bbl=doc["base_price_usd_bbl"],
            lat=doc["lat"],
            lng=doc["lng"]
        ))
    return result
