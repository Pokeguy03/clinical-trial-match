"""
Clinical Trial Patient Matching Environment Client.

Provides the client for connecting to the Clinical Trial Matching server.

Example:
    >>> with ClinicalTrialEnv(base_url="http://localhost:8000") as env:
    ...     env.reset()
    ...     tools = env.list_tools()
    ...     patients = env.call_tool("list_patients")
    ...     record = env.call_tool("get_patient_record", patient_id="P001")
    ...     trials = env.call_tool("list_trials")
    ...     details = env.call_tool("get_trial_details", trial_id="T001")
    ...     result = env.call_tool("submit_match",
    ...         patient_id="P001", trial_id="T001",
    ...         eligible=True, reasoning="Patient meets all criteria")
"""

from openenv.core.mcp_client import MCPToolClient


class ClinicalTrialEnv(MCPToolClient):
    """
    Client for the Clinical Trial Patient Matching Environment.

    Inherits all functionality from MCPToolClient:
    - `list_tools()`: Discover available tools
    - `call_tool(name, **kwargs)`: Call a tool by name
    - `reset(**kwargs)`: Reset the environment
    - `step(action)`: Execute an action
    """

    pass
