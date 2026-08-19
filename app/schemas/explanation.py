from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class ExplainRequest(BaseModel):
    scenario_id: str

class ExplanationResponse(BaseModel):
    executive_summary: str
    why_risky: str
    why_recommended: str
    reserve_rationale: str
    key_assumptions: List[str]
    uncertainties: List[str]
    model_used: Optional[str] = "gemini-2.5-flash"

    model_config = ConfigDict(protected_namespaces=())
