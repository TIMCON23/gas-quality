from pydantic import BaseModel
from typing import Dict, Any, Optional

class TelemetryEvent(BaseModel):
    sensor_id: str
    timestamp: float
    payload: Dict[str, Any]

class ReconstructedSignalEvent(BaseModel):
    sensor_id: str
    timestamp: float
    signal: Dict[str, Any]

class ScoreEvent(BaseModel):
    agent: str
    score: float
    metrics: Optional[Dict[str, Any]] = None

class SecurityAlertEvent(BaseModel):
    source: str
    level: str
    message: str
    metadata: Optional[Dict[str, Any]] = None

class DecisionEvent(BaseModel):
    decision: str
    confidence: float
    details: Optional[Dict[str, Any]] = None
