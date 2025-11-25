from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ExtractInput(BaseModel):
    tender_id: str
    text: Optional[str] = ""


class MatchInput(BaseModel):
    tender_id: str
    title: Optional[str] = None
    subject: Optional[str] = None
    top_k: int = 5


class RiskInput(BaseModel):
    tender_id: str
    features: Dict[str, Any]


class RiskOutput(BaseModel):
    tender_id: str
    risk_score: float
    risk_label: int
    risk_reasons: List[str]
