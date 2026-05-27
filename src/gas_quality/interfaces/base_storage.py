from abc import ABC, abstractmethod
from typing import Any

class BaseStorage(ABC):
    @abstractmethod
    async def save(self, key: str, value: Any):
        raise NotImplementedError()

    @abstractmethod
    async def query(self, query: str):
        raise NotImplementedError()
