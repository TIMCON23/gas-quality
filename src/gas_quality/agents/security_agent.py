import asyncio
from typing import Any
from src.gas_quality.interfaces.base_agent import BaseAgent
from src.gas_quality.events.events import TelemetryEvent, SecurityAlertEvent

class SecurityAgent(BaseAgent):
    async def run(self):
        async def handler(msg: Any):
            try:
                if isinstance(msg, dict):
                    event = TelemetryEvent(**msg)
                else:
                    event = msg
                if event.payload is None or not isinstance(event.payload, dict):
                    alert = SecurityAlertEvent(source=self.name, level="critical", message="invalid telemetry payload")
                    await self.transport.publish('security_alert', alert.dict())
            except Exception:
                return

        await self.transport.subscribe('telemetry', handler)
        while self._running:
            await asyncio.sleep(0.5)
