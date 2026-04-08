"""
Clinical Trial Patient Matching — OpenEnv Environment.

An AI agent reviews patient medical records and determines eligibility
for clinical trials by evaluating inclusion/exclusion criteria.

MCP Tools:
- `list_patients`: View all patients in the current batch
- `get_patient_record`: Read detailed patient medical record
- `list_trials`: View available clinical trials
- `get_trial_details`: Read trial protocol with criteria
- `submit_match`: Submit eligibility decision with reasoning
- `get_progress`: Check current matching progress and score

Example:
    >>> from clinical_trial_match import ClinicalTrialEnv
    >>>
    >>> with ClinicalTrialEnv(base_url="http://localhost:8000") as env:
    ...     env.reset()
    ...     tools = env.list_tools()
    ...     result = env.call_tool("list_patients")
"""

from openenv.core.env_server.mcp_types import CallToolAction, ListToolsAction

from .client import ClinicalTrialEnv

__all__ = ["ClinicalTrialEnv", "CallToolAction", "ListToolsAction"]
