from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List

class PriceChanges24h(BaseModel):
    amount: Optional[float] = None
    percent: Optional[float] = None
    previous_price: Optional[float] = None
    previous_timestamp: Optional[str] = None
    measured_at: Optional[str] = None

class BrentPriceRecord(BaseModel):
    id: str = Field(..., alias="_id")
    date: str
    timestamp: str
    price: float
    currency: str = "USD"
    unit: str = "barrel"
    code: str = "BRENT_CRUDE_USD"
    formatted: Optional[str] = None
    price_change_pct: Optional[float] = 0.0
    change_24h_amount: Optional[float] = 0.0
    previous_price: Optional[float] = None
    source: str = "oilpriceapi"
    data_status: Optional[str] = "current"
    anomaly_flag: bool = False
    anomaly_score: float = 0.0
    is_anomaly: Optional[bool] = False
    updated_at: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)

class LatestPriceResponse(BaseModel):
    status: str = "success"
    data: BrentPriceRecord
    cached: bool = False
    last_synced_at: str

class PriceHistoryPoint(BaseModel):
    date: str
    price: float
    price_change_pct: Optional[float] = None
    anomaly_flag: bool = False
    anomaly_score: float = 0.0
    is_anomaly: Optional[bool] = False
    source: Optional[str] = "historical"

class PriceHistoryResponse(BaseModel):
    status: str = "success"
    count: int
    data: List[PriceHistoryPoint]

class PriceSyncResponse(BaseModel):
    status: str
    message: str
    data: Optional[BrentPriceRecord] = None
