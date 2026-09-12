from abc import ABC, abstractmethod
from typing import Any

class BaseIngestionProvider(ABC):

    @abstractmethod
    def fetch_mentions(self, target_entity: str) -> list[dict[str, Any]]:
        """Fetch raw mentions for a given target entity."""
        pass