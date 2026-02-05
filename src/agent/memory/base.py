"""Base memory provider implementation."""

from typing import Any, Dict, List
from agent.core.contracts import MemoryProvider


class BaseMemory(MemoryProvider):
    """
    Base implementation of MemoryProvider.
    
    Provides common functionality for all memory implementations.
    """
    
    def __init__(self, max_items: int = 100):
        self.max_items = max_items
        self._storage: List[Dict[str, Any]] = []
    
    async def load(self) -> List[Dict[str, Any]]:
        """Load memory context."""
        return self._storage.copy()
    
    async def persist(self, data: List[Dict[str, Any]]) -> None:
        """Persist data to memory."""
        self._storage.extend(data)
        # Trim if exceeds max_items
        if len(self._storage) > self.max_items:
            self._storage = self._storage[-self.max_items:]
    
    async def clear(self) -> None:
        """Clear all memory."""
        self._storage.clear()
    
    def get_size(self) -> int:
        """Get the current size of memory."""
        return len(self._storage)
