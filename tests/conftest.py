"""Test configuration and fixtures."""

import pytest
from agent.adapters.factory import AdapterFactory
from agent.memory.buffer import BufferMemory
from agent.memory.ephemeral import EphemeralMemory


@pytest.fixture
def mock_chat_adapter():
    """Create a mock chat adapter for testing."""
    # TODO: Implement mock adapter
    return None


@pytest.fixture
def buffer_memory():
    """Create a buffer memory instance."""
    return BufferMemory(max_messages=10)


@pytest.fixture
def ephemeral_memory():
    """Create an ephemeral memory instance."""
    return EphemeralMemory()
