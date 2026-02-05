"""Unit tests for memory providers."""

import pytest
from agent.memory.buffer import BufferMemory
from agent.memory.ephemeral import EphemeralMemory
from agent.memory.contextual import ContextualMemory


@pytest.mark.asyncio
async def test_buffer_memory_persistence():
    """Test that buffer memory persists data correctly."""
    memory = BufferMemory(max_messages=5)
    
    # Add some data
    test_data = [{"message": "test1"}, {"message": "test2"}]
    await memory.persist(test_data)
    
    # Load and verify
    loaded = await memory.load()
    assert len(loaded) == 2
    assert loaded[0]["message"] == "test1"


@pytest.mark.asyncio
async def test_ephemeral_memory():
    """Test that ephemeral memory doesn't persist."""
    memory = EphemeralMemory()
    
    # Try to persist data
    await memory.persist([{"message": "test"}])
    
    # Should return empty
    loaded = await memory.load()
    assert len(loaded) == 0


@pytest.mark.asyncio
async def test_contextual_memory():
    """Test read-only contextual memory."""
    context_data = [{"context": "test"}]
    memory = ContextualMemory(context_data)
    
    # Should load context
    loaded = await memory.load()
    assert len(loaded) == 1
    
    # Persist should be no-op
    await memory.persist([{"new": "data"}])
    loaded = await memory.load()
    assert len(loaded) == 1  # Still only original context
