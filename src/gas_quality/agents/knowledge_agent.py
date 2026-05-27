import asyncio
from typing import Any
from src.gas_quality.interfaces.base_agent import BaseAgent
from src.gas_quality.events.events import DecisionEvent
from src.gas_quality.storage.in_memory_storage import InMemoryStorage

class KnowledgeAgent(BaseAgent):
    def __init__(self, name: str, transport: Any = None, storage: Any = None):
        super().__init__(name, transport)
        self.storage = storage or InMemoryStorage()

    async def run(self):
        async def handler(msg: Any):
            try:
                if isinstance(msg, dict):
                    event = DecisionEvent(**msg)
                else:
                    event = msg
                record = {
                    "event": event.decision,
                    "confidence": event.confidence,
                    "details": event.details,
                    "timestamp": event.details.get("timestamp") if event.details else None,
                }
                await self.storage.save(f"decision-{len(self.storage.records)}", record)
            except Exception:
                return

        await self.transport.subscribe('decision', handler)
        while self._running:
            await asyncio.sleep(0.5)
