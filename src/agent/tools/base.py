"""Base tool implementation."""

from typing import Any, Dict
from pydantic import BaseModel, Field
from agent.core.contracts import Tool


class ToolInput(BaseModel):
    """Base input schema for tools."""
    pass


class BaseTool(Tool):
    """
    Base implementation for agent tools.
    
    Tools represent capabilities, not raw API calls.
    Characteristics:
    - Narrow and well-defined
    - Schema-validated with Pydantic
    - Explicitly declared per agent
    """
    
    def __init__(self, name: str, description: str, input_schema: type[BaseModel]):
        self.name = name
        self.description = description
        self.input_schema = input_schema
    
    async def execute(self, arguments: Dict[str, Any]) -> Any:
        """
        Execute the tool with validated arguments.
        
        Args:
            arguments: Tool input arguments
            
        Returns:
            Tool execution result
        """
        # Validate input
        validated_input = self.input_schema(**arguments)
        
        # Execute tool logic
        return await self._execute(validated_input)
    
    async def _execute(self, input_data: BaseModel) -> Any:
        """
        Override this method in subclasses to implement tool logic.
        
        Args:
            input_data: Validated Pydantic input model
            
        Returns:
            Tool execution result
        """
        raise NotImplementedError("Subclasses must implement _execute()")
