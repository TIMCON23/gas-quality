from typing import Dict, Any

class ExplanationEngine:
    @staticmethod
    def explain(decision: str, confidence: float, details: Dict[str, Any]) -> str:
        lines = [f"ANOMALY DETECTION: {decision.upper()}", f"confidence={confidence:.2f}"]
        if details:
            lines.append("details:")
            for key, value in details.items():
                lines.append(f"- {key}: {value}")
        return "\n".join(lines)
