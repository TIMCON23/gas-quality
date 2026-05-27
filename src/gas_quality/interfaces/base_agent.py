from abc import ABC, abstractmethod
import asyncio
from typing import Any

class BaseAgent(ABC):
    """Abstract base class for agents."""
    def __init__(self, name: str, transport: Any = None):
        self.name = name
        self.transport = transport
        self._task = None
        self._running = False

    async def start(self):
        self._running = True
        self._task = asyncio.create_task(self.run())

    async def stop(self):
        self._running = False
        if self._task:
            await self._task

    @abstractmethod
    async def run(self):
        """Main loop of the agent."""
        raise NotImplementedError()
