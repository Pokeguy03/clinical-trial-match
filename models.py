"""
Models for the Clinical Trial Patient Matching Environment.

Defines the action and observation types used by the OpenEnv framework
for MCP tool-calling interactions.
"""

try:
    from openenv.core.env_server.mcp_types import (
        CallToolAction,
        CallToolObservation,
        ListToolsAction,
        ListToolsObservation,
    )
except ImportError:
    from openenv.core.env_server.mcp_types import (
        CallToolAction,
        CallToolObservation,
        ListToolsAction,
        ListToolsObservation,
    )

# Re-export for openenv framework discovery
__all__ = [
    "CallToolAction",
    "CallToolObservation",
    "ListToolsAction",
    "ListToolsObservation",
]
