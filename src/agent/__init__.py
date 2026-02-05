"""Adaptable Agent Architecture - A flexible, LLM-agnostic agent framework."""

__version__ = "0.1.0"

from agent.core.engine import AgentEngine
from agent.core.config import AgentConfig
from agent.models.input import BaseInput
from agent.models.output import BaseOutput

__all__ = ["AgentEngine", "AgentConfig", "BaseInput", "BaseOutput"]
