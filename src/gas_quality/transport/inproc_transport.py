import asyncio
from typing import Callable, Any, Dict, List
from src.gas_quality.interfaces.base_transport import BaseTransport

class InProcTransport(BaseTransport):
    """Lightweight in-process async transport for prototyping."""
    def __init__(self):
        self._topics: Dict[str, List[Callable[[Any], Any]]] = {}

    async def publish(self, topic: str, message: Any):
        handlers = list(self._topics.get(topic, []))
        for h in handlers:
            asyncio.create_task(h(message))

    async def subscribe(self, topic: str, handler: Callable[[Any], Any]):
        self._topics.setdefault(topic, []).append(handler)

