from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class NetworkNode(BaseModel):
    id: str = Field(..., alias="_id")
    type: str  # "supplier", "origin", "indian_port", "refinery"
    name: str
    lat: float
    lng: float
    risk: Optional[float] = 0.0

    model_config = ConfigDict(populate_by_name=True)

class NetworkEdge(BaseModel):
    id: str = Field(..., alias="_id")
    from_node: str = Field(..., alias="from")
    to_node: str = Field(..., alias="to")
    corridor: Optional[str] = None
    corridor_id: Optional[str] = None
    risk: float
    status: str  # "active", "blocked", "degraded"
    flow_bpd: int
    current_flow_bpd: int
    capacity_bpd: int

    model_config = ConfigDict(populate_by_name=True)

class NetworkResponse(BaseModel):
    nodes: List[NetworkNode]
    edges: List[NetworkEdge]
