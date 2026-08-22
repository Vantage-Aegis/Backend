from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.services.oil_price_service import OilPriceService
from app.schemas.price import (
    LatestPriceResponse,
    BrentPriceRecord,
    PriceHistoryResponse,
    PriceHistoryPoint,
    PriceSyncResponse
)
from datetime import datetime, timezone

router = APIRouter(prefix="/api/prices", tags=["Crude Oil Prices"])

@router.get("/latest", response_model=LatestPriceResponse)
async def get_latest_price(db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Returns the latest real-time Brent Crude benchmark price, 24h change %, and anomaly status.
    Data is refreshed daily from OilPriceAPI and stored in MongoDB Atlas.
    """
    doc = await OilPriceService.get_latest_price(db)
    if not doc:
        raise HTTPException(status_code=404, detail="No price data available")

    # Map to schema
    record = BrentPriceRecord(
        _id=doc.get("_id", "latest_brent_price"),
        date=doc.get("date", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
        timestamp=doc.get("timestamp", datetime.now(timezone.utc).isoformat()),
        price=float(doc.get("price", 0.0)),
        currency=doc.get("currency", "USD"),
        unit=doc.get("unit", "barrel"),
        code=doc.get("code", "BRENT_CRUDE_USD"),
        formatted=doc.get("formatted", f"${float(doc.get('price', 0.0)):.2f}"),
        price_change_pct=doc.get("price_change_pct", 0.0),
        change_24h_amount=doc.get("change_24h_amount", 0.0),
        previous_price=doc.get("previous_price"),
        source=doc.get("source", "oilpriceapi"),
        data_status=doc.get("data_status", "current"),
        anomaly_flag=bool(doc.get("anomaly_flag", False)),
        anomaly_score=float(doc.get("anomaly_score", 0.0) or 0.0),
        is_anomaly=bool(doc.get("is_anomaly", False)),
        updated_at=doc.get("updated_at")
    )

    return LatestPriceResponse(
        status="success",
        data=record,
        cached=doc.get("source") != "oilpriceapi_live_direct",
        last_synced_at=doc.get("updated_at") or datetime.now(timezone.utc).isoformat()
    )

@router.get("/history", response_model=PriceHistoryResponse)
async def get_price_history(
    timeframe: str = Query("1M", description="Timeframe: 1W, 1M, 6M, 1Y, 5Y, MAX"),
    limit: Optional[int] = Query(None, ge=1, le=1000, description="Optional custom limit on data points"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Returns historical Brent crude price data points and anomaly detection indicators filtered by timeframe (1W, 1M, 6M, 1Y, 5Y, MAX).
    """
    history_docs = await OilPriceService.get_price_history(db, timeframe=timeframe, limit=limit)
    points = [PriceHistoryPoint(**item) for item in history_docs]
    return PriceHistoryResponse(
        status="success",
        count=len(points),
        data=points
    )

@router.post("/sync", response_model=PriceSyncResponse)
async def sync_price_now(db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Triggers an on-demand real-time refresh from OilPriceAPI and records the price in MongoDB Atlas.
    """
    synced_doc = await OilPriceService.sync_and_store_daily_price(db)
    if not synced_doc:
        raise HTTPException(status_code=502, detail="Failed to fetch real-time price from OilPriceAPI")

    record = BrentPriceRecord(
        _id=synced_doc.get("_id", "brent_now"),
        date=synced_doc.get("date"),
        timestamp=synced_doc.get("timestamp"),
        price=float(synced_doc.get("price", 0.0)),
        currency=synced_doc.get("currency", "USD"),
        unit=synced_doc.get("unit", "barrel"),
        code=synced_doc.get("code", "BRENT_CRUDE_USD"),
        formatted=synced_doc.get("formatted"),
        price_change_pct=synced_doc.get("price_change_pct", 0.0),
        change_24h_amount=synced_doc.get("change_24h_amount", 0.0),
        previous_price=synced_doc.get("previous_price"),
        source=synced_doc.get("source", "oilpriceapi"),
        data_status=synced_doc.get("data_status", "current"),
        anomaly_flag=bool(synced_doc.get("anomaly_flag", False)),
        anomaly_score=float(synced_doc.get("anomaly_score", 0.0) or 0.0),
        is_anomaly=bool(synced_doc.get("is_anomaly", False)),
        updated_at=synced_doc.get("updated_at")
    )

    return PriceSyncResponse(
        status="success",
        message="Live Brent crude oil price refreshed and persisted successfully",
        data=record
    )
