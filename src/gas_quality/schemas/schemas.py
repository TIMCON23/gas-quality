from pydantic import BaseModel
from typing import Dict, Any, Optional

class TelemetryPacket(BaseModel):
    sensor_id: str
    timestamp: float
    measurements: Dict[str, float]

class AgentDecision(BaseModel):
    agent: str
    label: str
    confidence: float

class PhysicalState(BaseModel):
    q_in: float
    q_out: float
    pressure: float

class ConfidenceScore(BaseModel):
    score: float
    source: str
