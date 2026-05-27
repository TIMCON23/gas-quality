import asyncio
import time
from typing import List
from src.gas_quality.transport import InProcTransport
from src.gas_quality.agents.sensor_agent import SensorAgent
from src.gas_quality.agents.balance_agent import BalanceAgent
from src.gas_quality.agents.statistical_agent import StatisticalAgent
from src.gas_quality.agents.decision_agent import DecisionAgent
from src.gas_quality.agents.knowledge_agent import KnowledgeAgent
from src.gas_quality.agents.security_agent import SecurityAgent
from src.gas_quality.storage.in_memory_storage import InMemoryStorage
from src.gas_quality.events.events import TelemetryEvent

class MASHost:
    def __init__(self):
        self.transport = InProcTransport()
        self.storage = InMemoryStorage()
        self.agents = self._create_agents()

    def _create_agents(self) -> List:
        return [
            SensorAgent(name="SensorAgent", transport=self.transport),
            BalanceAgent(name="BalanceAgent", transport=self.transport),
            StatisticalAgent(name="StatisticalAgent", transport=self.transport),
            DecisionAgent(name="DecisionAgent", transport=self.transport),
            KnowledgeAgent(name="KnowledgeAgent", transport=self.transport, storage=self.storage),
            SecurityAgent(name="SecurityAgent", transport=self.transport),
        ]

    async def start(self):
        for agent in self.agents:
            await agent.start()
        # allow agent tasks to subscribe before publishing events
        await asyncio.sleep(0.5)

    async def stop(self):
        for agent in self.agents:
            await agent.stop()

    async def publish_telemetry(self, packet: dict):
        event = TelemetryEvent(**packet)
        await self.transport.publish('telemetry', event.dict())

    async def run_demo(self):
        await self.start()
        sample = {
            "sensor_id": "node-1",
            "timestamp": time.time(),
            "payload": {
                "time": [0, 10, 20, 30, 40],
                "flow_m3h": [10.0, 10.5, 9.8, 11.2, 10.1],
                "pressure_kpa": [50.0, 49.8, 50.2, 49.5, 50.1],
                "Qin": [10.0, 10.5, 9.8, 11.2, 10.1],
                "Qout": [9.0, 9.2, 8.8, 9.5, 9.1],
                "signal": [100.0, 101.5, 99.8, 102.2, 100.5],
            },
        }
        await self.publish_telemetry(sample)
        await asyncio.sleep(2.0)
        return await self.storage.query("all")

if __name__ == "__main__":
    async def main():
        host = MASHost()
        records = await host.run_demo()
        print("Knowledge storage records:", records)
        await host.stop()

    asyncio.run(main())
