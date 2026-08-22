from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class EventCreateRequest(BaseModel):
    title: str
    corridor: Optional[str] = Field(None, alias="region")
    severity: Optional[int] = None
    source: str = "manual"
    category: Optional[str] = "sanctions"
    description: Optional[str] = ""

    model_config = ConfigDict(populate_by_name=True)

class EventResponse(BaseModel):
    id: str = Field(..., alias="_id")
    title: str
    corridor: str
    severity: int
    source: str
    category: str
    description: Optional[str] = ""
    confidence: Optional[float] = None
    needs_review: Optional[bool] = False
    date: Optional[str] = None
    published_at: Optional[str] = None
    ingested_at: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)
