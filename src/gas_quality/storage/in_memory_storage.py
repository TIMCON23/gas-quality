from typing import Any, Dict

class InMemoryStorage:
    def __init__(self):
        self.records: Dict[str, Any] = {}

    async def save(self, key: str, value: Any):
        self.records[key] = value
        return value

    async def query(self, query: str):
        if query == "all":
            return list(self.records.values())
        return [v for v in self.records.values() if query in str(v)]
