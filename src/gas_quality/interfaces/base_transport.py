from abc import ABC, abstractmethod
from typing import Callable, Any

class BaseTransport(ABC):
    @abstractmethod
    async def publish(self, topic: str, message: Any):
        raise NotImplementedError()

    @abstractmethod
    async def subscribe(self, topic: str, handler: Callable[[Any], Any]):
        raise NotImplementedError()
