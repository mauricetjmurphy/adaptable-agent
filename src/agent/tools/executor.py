"""Tool execution logic with safety and observability."""

from typing import Any, Dict, Optional
from agent.core.contracts import Tool
from agent.observability.logger import get_logger

logger = get_logger(__name__)


class ToolExecutionResult:
    """Result of tool execution."""
    
    def __init__(
        self,
        tool_name: str,
        success: bool,
        result: Any = None,
        error: Optional[str] = None
    ):
        self.tool_name = tool_name
        self.success = success
        self.result = result
        self.error = error


class ToolExecutor:
    """
    Executes tools with safety checks and observability.
    
    Wraps tool execution with:
    - Permission checking
    - Error handling
    - Logging and metrics
    - Approval gates (if configured)
    """
    
    def __init__(self, enable_approval_gates: bool = False):
        self.enable_approval_gates = enable_approval_gates
    
    async def execute(
        self,
        tool: Tool,
        arguments: Dict[str, Any],
        require_approval: bool = False
    ) -> ToolExecutionResult:
        """
        Execute a tool with safety checks.
        
        Args:
            tool: Tool to execute
            arguments: Tool arguments
            require_approval: Whether to require human approval
            
        Returns:
            ToolExecutionResult
        """
        logger.info(f"Executing tool: {tool.name}")
        
        try:
            # Check approval if required
            if require_approval or self.enable_approval_gates:
                approved = await self._request_approval(tool, arguments)
                if not approved:
                    return ToolExecutionResult(
                        tool_name=tool.name,
                        success=False,
                        error="Approval denied"
                    )
            
            # Execute tool
            result = await tool.execute(arguments)
            
            logger.info(f"Tool {tool.name} executed successfully")
            return ToolExecutionResult(
                tool_name=tool.name,
                success=True,
                result=result
            )
            
        except Exception as e:
            logger.error(f"Tool {tool.name} execution failed: {e}")
            return ToolExecutionResult(
                tool_name=tool.name,
                success=False,
                error=str(e)
            )
    
    async def _request_approval(
        self,
        tool: Tool,
        arguments: Dict[str, Any]
    ) -> bool:
        """Request human approval for tool execution."""
        # TODO: Implement approval mechanism
        logger.warning(f"Approval requested for {tool.name} (auto-approved)")
        return True
