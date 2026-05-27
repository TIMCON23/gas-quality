import asyncio
from typing import Any
from src.gas_quality.interfaces.base_agent import BaseAgent
from src.gas_quality.events.events import TelemetryEvent, ReconstructedSignalEvent
from src.gas_quality.reconstruction import reconstruct_signal

class SensorAgent(BaseAgent):
    async def run(self):
        async def handler(msg: Any):
            try:
                if isinstance(msg, dict):
                    event = TelemetryEvent(**msg)
                else:
                    event = msg

                payload = event.payload or {}
                signal = payload.get('signal')
                time_values = payload.get('time')
                reconstructed = payload

                if signal is not None and time_values is not None:
                    _, recon = reconstruct_signal(time_values, signal)
                    reconstructed = {
                        **payload,
                        'reconstructed_signal': recon.tolist() if hasattr(recon, 'tolist') else list(recon),
                    }

                out_event = ReconstructedSignalEvent(sensor_id=event.sensor_id, timestamp=event.timestamp, signal=reconstructed)
                await self.transport.publish('reconstructed_signal', out_event.dict())
            except Exception:
                return

        await self.transport.subscribe('telemetry', handler)
        while self._running:
            await asyncio.sleep(0.5)
