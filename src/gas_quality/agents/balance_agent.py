import asyncio
from typing import Any, Dict
import pandas as pd
from src.gas_quality.interfaces.base_agent import BaseAgent
from src.gas_quality.events.events import ReconstructedSignalEvent, ScoreEvent
from src.gas_quality.double_control.physical import physical_control

class BalanceAgent(BaseAgent):
    @staticmethod
    def _normalize_signal(signal: Dict[str, Any]) -> pd.DataFrame:
        lengths = {}
        for key, value in signal.items():
            if isinstance(value, (list, tuple)):
                lengths.setdefault(len(value), []).append(key)
        if not lengths:
            return pd.DataFrame(signal)
        largest_group = max(lengths.items(), key=lambda item: len(item[1]))[1]
        normalized = {key: signal[key] for key in largest_group}
        return pd.DataFrame(normalized)

    async def run(self):
        async def handler(msg: Any):
            try:
                if isinstance(msg, dict):
                    event = ReconstructedSignalEvent(**msg)
                else:
                    event = msg
                df = self._normalize_signal(event.signal)
                score, flags, details = physical_control(df)
                await self.transport.publish('physical_score', ScoreEvent(agent=self.name, score=float(score.mean()), metrics=details).dict())
            except Exception:
                return

        await self.transport.subscribe('reconstructed_signal', handler)
        while self._running:
            await asyncio.sleep(0.5)
