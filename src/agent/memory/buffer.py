"""Conversation buffer memory implementation."""

from typing import Any, Dict, List
from agent.memory.base import BaseMemory


class BufferMemory(BaseMemory):
    """
    Conversation buffer memory.
    
    Stores recent conversation history in a sliding window.
    Suitable for chat-based agents.
    """
    
    def __init__(self, max_messages: int = 50, max_tokens: int = 2000):
        super().__init__(max_items=max_messages)
        self.max_tokens = max_tokens
        self._token_count = 0
    
    async def persist(self, data: List[Dict[str, Any]]) -> None:
        """Persist messages with token-based pruning."""
        for item in data:
            # Estimate tokens (rough approximation)
            item_tokens = len(str(item)) // 4
            
            # Add to storage
            self._storage.append(item)
            self._token_count += item_tokens
            
            # Prune oldest messages if over token limit
            while self._token_count > self.max_tokens and self._storage:
                removed = self._storage.pop(0)
                removed_tokens = len(str(removed)) // 4
                self._token_count -= removed_tokens
    
    async def clear(self) -> None:
        """Clear all memory and reset token count."""
        await super().clear()
        self._token_count = 0
    
    def get_token_count(self) -> int:
        """Get the approximate token count."""
        return self._token_count
