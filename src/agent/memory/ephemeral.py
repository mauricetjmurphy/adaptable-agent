"""Ephemeral (no-op) memory implementation."""

from typing import Any, Dict, List
from agent.memory.base import BaseMemory


class EphemeralMemory(BaseMemory):
    """
    Ephemeral memory - stores nothing.
    
    All memory operations are no-ops.
    Suitable for stateless agents that don't need to maintain context.
    """
    
    def __init__(self):
        super().__init__(max_items=0)
    
    async def load(self) -> List[Dict[str, Any]]:
        """Always returns empty list."""
        return []
    
    async def persist(self, data: List[Dict[str, Any]]) -> None:
        """No-op - data is discarded."""
        pass
    
    async def clear(self) -> None:
        """No-op - nothing to clear."""
        pass
