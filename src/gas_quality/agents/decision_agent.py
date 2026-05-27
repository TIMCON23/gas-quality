import asyncio
from typing import Any, Dict
from src.gas_quality.interfaces.base_agent import BaseAgent
from src.gas_quality.events.events import ScoreEvent, DecisionEvent

class DecisionAgent(BaseAgent):
    def __init__(self, name: str, transport: Any = None):
        super().__init__(name, transport)
        self._scores: Dict[str, float] = {}

    async def run(self):
        async def handler(msg: Any):
            try:
                if isinstance(msg, dict):
                    event = ScoreEvent(**msg)
                else:
                    event = msg
                self._scores[event.agent] = event.score
                if len(self._scores) >= 2:
                    decision, confidence = self.fuse_scores(self._scores)
                    await self.transport.publish('decision', DecisionEvent(decision=decision, confidence=confidence, details={"scores": self._scores}).dict())
            except Exception:
                return

        await self.transport.subscribe('physical_score', handler)
        await self.transport.subscribe('statistical_score', handler)
        while self._running:
            await asyncio.sleep(0.5)

    @staticmethod
    def fuse_scores(scores: Dict[str, float]) -> tuple[str, float]:
        weights = {"BalanceAgent": 0.5, "StatisticalAgent": 0.5}
        total_weight = sum(weights.get(name, 0.5) for name in scores)
        fused = sum(scores[name] * weights.get(name, 0.5) for name in scores) / max(total_weight, 1e-6)
        label = "anomaly" if fused > 0.6 else "normal"
        return label, float(fused)
