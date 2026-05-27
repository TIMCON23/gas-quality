import asyncio
from typing import Any
import numpy as np
from src.gas_quality.interfaces.base_agent import BaseAgent
from src.gas_quality.events.events import ReconstructedSignalEvent, ScoreEvent
from src.gas_quality.double_control.statistical import statistical_control

class StatisticalAgent(BaseAgent):
    @staticmethod
    def _extract_primary_signal(signal_data: dict) -> np.ndarray:
        preferred = ['reconstructed_signal', 'signal', 'flow_m3h', 'pressure_kpa']
        for key in preferred:
            value = signal_data.get(key)
            if isinstance(value, (list, tuple, np.ndarray)) and len(value) > 0:
                return np.asarray(value, dtype=float)
        for value in signal_data.values():
            if isinstance(value, (list, tuple, np.ndarray)) and len(value) > 0:
                return np.asarray(value, dtype=float)
            if isinstance(value, (int, float)):
                return np.asarray([float(value)])
        return np.asarray([])

    async def run(self):
        async def handler(msg: Any):
            try:
                if isinstance(msg, dict):
                    event = ReconstructedSignalEvent(**msg)
                else:
                    event = msg
                raw = self._extract_primary_signal(event.signal)
                if raw.size == 0:
                    return
                score, flags, details = statistical_control(raw, raw)
                await self.transport.publish('statistical_score', ScoreEvent(agent=self.name, score=float(score.mean()), metrics=details).dict())
            except Exception:
                return

        await self.transport.subscribe('reconstructed_signal', handler)
        while self._running:
            await asyncio.sleep(0.5)
