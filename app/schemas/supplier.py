from pydantic import BaseModel, Field, ConfigDict

class SupplierResponse(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    current_export_bpd: int
    max_capacity_bpd: int
    reliability_score: float
    base_price_usd_bbl: float
    lat: float
    lng: float

    model_config = ConfigDict(populate_by_name=True)
