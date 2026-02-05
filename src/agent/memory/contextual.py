"""Read-only contextual memory implementation."""

from typing import Any, Dict, List
from agent.memory.base import BaseMemory


class ContextualMemory(BaseMemory):
    """
    Read-only contextual memory.
    
    Provides static context that cannot be modified during execution.
    Suitable for agents that need access to reference information,
    documentation, or system prompts.
    """
    
    def __init__(self, context_data: List[Dict[str, Any]]):
        super().__init__()
        self._context = context_data
        self._storage = context_data.copy()
    
    async def persist(self, data: List[Dict[str, Any]]) -> None:
        """
        Persist is a no-op for read-only memory.
        
        New data is not added to contextual memory.
        """
        pass  # Read-only memory does not persist new data
    
    async def clear(self) -> None:
        """Reset to original context."""
        self._storage = self._context.copy()
    
    async def reload_context(self, new_context: List[Dict[str, Any]]) -> None:
        """Replace the contextual data."""
        self._context = new_context
        self._storage = new_context.copy()
