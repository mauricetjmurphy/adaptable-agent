"""Tool-level permission management."""

from typing import Dict, List, Set
from enum import Enum


class Permission(Enum):
    """Permission types."""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DELETE = "delete"
    ADMIN = "admin"


class PermissionManager:
    """
    Manages permissions for tool execution.
    
    Controls which tools can be executed based on:
    - Agent identity
    - Tool sensitivity
    - User approval
    """
    
    def __init__(self):
        self._tool_permissions: Dict[str, Set[Permission]] = {}
        self._sensitive_tools: Set[str] = set()
    
    def register_tool_permissions(
        self,
        tool_name: str,
        permissions: List[Permission]
    ) -> None:
        """Register required permissions for a tool."""
        self._tool_permissions[tool_name] = set(permissions)
    
    def mark_sensitive(self, tool_name: str) -> None:
        """Mark a tool as sensitive (requires extra approval)."""
        self._sensitive_tools.add(tool_name)
    
    def is_sensitive(self, tool_name: str) -> bool:
        """Check if a tool is marked as sensitive."""
        return tool_name in self._sensitive_tools
    
    def check_permission(
        self,
        tool_name: str,
        required_permission: Permission
    ) -> bool:
        """Check if a permission is granted for a tool."""
        tool_perms = self._tool_permissions.get(tool_name, set())
        return required_permission in tool_perms or Permission.ADMIN in tool_perms
    
    def get_tool_permissions(self, tool_name: str) -> Set[Permission]:
        """Get all permissions for a tool."""
        return self._tool_permissions.get(tool_name, set()).copy()


# Global permission manager
_global_permissions = PermissionManager()

# Mark sensitive tools
_global_permissions.mark_sensitive("send_email")
_global_permissions.mark_sensitive("delete_file")


def get_global_permissions() -> PermissionManager:
    """Get the global permission manager."""
    return _global_permissions
