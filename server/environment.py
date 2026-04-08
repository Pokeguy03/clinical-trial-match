"""
Clinical Trial Patient Matching — MCPEnvironment Implementation.

Registers 6 FastMCP tools and implements the core matching logic with
reward computation and state management across 3 difficulty tiers.
"""

import json
from typing import Any, Optional
from uuid import uuid4

try:
    from openenv.core.env_server.mcp_environment import MCPEnvironment
    from openenv.core.env_server.types import Action, Observation, State
except ImportError:
    from openenv.core.env_server.mcp_environment import MCPEnvironment
    from openenv.core.env_server.types import Action, Observation, State

from fastmcp import FastMCP

from server.data import (
    GROUND_TRUTH,
    PATIENTS,
    TASKS,
    TRIALS,
    get_patient_summary,
    get_trial_summary,
)


class ClinicalTrialMatchEnvironment(MCPEnvironment):
    """
    Clinical Trial Patient Matching environment.

    An AI agent reviews patient medical records and determines eligibility
    for clinical trials. The agent uses MCP tools to browse patients, read
    records, review trial protocols, and submit match decisions.

    Tools:
        - list_patients: View patient summaries
        - get_patient_record: Full patient medical record
        - list_trials: View trial summaries
        - get_trial_details: Full trial protocol with criteria
        - submit_match: Submit eligibility decision with reasoning
        - get_progress: Check matching progress and current score
    """

    def __init__(self) -> None:
        """Initialize environment with MCP tools."""
        mcp = FastMCP("clinical_trial_match")

        # State that tools need access to (set on reset)
        self._task_name: str = "easy"
        self._patient_ids: list[str] = []
        self._trial_ids: list[str] = []
        self._max_steps: int = 30
        self._submitted_matches: dict[tuple[str, str], dict[str, Any]] = {}
        self._expected_pairs: set[tuple[str, str]] = set()
        self._cumulative_reward: float = 0.0
        self._patients_reviewed: set[str] = set()
        self._trials_reviewed: set[str] = set()
        self._done: bool = False

        # Keep a ref to self for closures
        env = self

        @mcp.tool
        def list_patients() -> str:
            """
            List all patients in the current task with brief summaries.
            Returns patient IDs, names, ages, sex, and primary conditions.
            Use this to identify which patients to review.
            """
            summaries = [
                get_patient_summary(pid) for pid in env._patient_ids
            ]
            return json.dumps(summaries, indent=2)

        @mcp.tool
        def get_patient_record(patient_id: str) -> str:
            """
            Get the complete medical record for a specific patient.
            Includes demographics, conditions, medications, lab results,
            allergies, medical history, and vital signs.

            Args:
                patient_id: The patient identifier (e.g., 'P001')
            """
            if patient_id not in env._patient_ids:
                return json.dumps({
                    "error": f"Patient {patient_id} not found in current task. "
                    f"Available: {env._patient_ids}"
                })
            env._patients_reviewed.add(patient_id)
            record = PATIENTS[patient_id].copy()
            record["patient_id"] = patient_id
            return json.dumps(record, indent=2, default=str)

        @mcp.tool
        def list_trials() -> str:
            """
            List all clinical trials in the current task with brief summaries.
            Returns trial IDs, titles, phases, and target conditions.
            Use this to identify which trials to review.
            """
            summaries = [
                get_trial_summary(tid) for tid in env._trial_ids
            ]
            return json.dumps(summaries, indent=2)

        @mcp.tool
        def get_trial_details(trial_id: str) -> str:
            """
            Get the complete protocol for a specific clinical trial.
            Includes summary, inclusion criteria, exclusion criteria,
            primary endpoint, and study duration.

            Args:
                trial_id: The trial identifier (e.g., 'T001')
            """
            if trial_id not in env._trial_ids:
                return json.dumps({
                    "error": f"Trial {trial_id} not found in current task. "
                    f"Available: {env._trial_ids}"
                })
            env._trials_reviewed.add(trial_id)
            details = TRIALS[trial_id].copy()
            details["trial_id"] = trial_id
            return json.dumps(details, indent=2)

        @mcp.tool
        def submit_match(
            patient_id: str,
            trial_id: str,
            eligible: bool,
            reasoning: str,
        ) -> str:
            """
            Submit an eligibility decision for a patient-trial pair.

            You must review the patient record and trial criteria before
            submitting a decision. Provide clear reasoning for your decision.

            Args:
                patient_id: The patient identifier (e.g., 'P001')
                trial_id: The trial identifier (e.g., 'T001')
                eligible: True if the patient meets all criteria, False otherwise
                reasoning: Explanation of why the patient is/isn't eligible.
                    Reference specific criteria and patient data.
            """
            pair = (patient_id, trial_id)

            # Validate inputs
            if patient_id not in env._patient_ids:
                return json.dumps({
                    "error": f"Patient {patient_id} not in current task.",
                    "reward": 0.0,
                })
            if trial_id not in env._trial_ids:
                return json.dumps({
                    "error": f"Trial {trial_id} not in current task.",
                    "reward": 0.0,
                })
            if pair in env._submitted_matches:
                return json.dumps({
                    "error": f"Match ({patient_id}, {trial_id}) already submitted.",
                    "reward": 0.0,
                })

            # Compute reward for this decision
            reward = env._compute_match_reward(
                patient_id, trial_id, eligible, reasoning
            )
            env._cumulative_reward += reward
            env._submitted_matches[pair] = {
                "eligible": eligible,
                "reasoning": reasoning,
                "reward": reward,
            }

            remaining = len(env._expected_pairs) - len(env._submitted_matches)
            if remaining == 0:
                env._done = True

            return json.dumps({
                "status": "accepted",
                "patient_id": patient_id,
                "trial_id": trial_id,
                "decision": "eligible" if eligible else "not eligible",
                "reward": round(reward, 3),
                "matches_remaining": remaining,
                "done": env._done,
            }, indent=2)

        @mcp.tool
        def get_progress() -> str:
            """
            Check current matching progress, score, and remaining work.
            Returns the number of submitted and remaining matches,
            cumulative reward, and normalized score.
            """
            total = len(env._expected_pairs)
            submitted = len(env._submitted_matches)
            max_reward = env._get_max_possible_reward()
            norm_score = (
                env._cumulative_reward / max_reward if max_reward > 0 else 0.0
            )
            return json.dumps({
                "task": env._task_name,
                "matches_submitted": submitted,
                "matches_total": total,
                "matches_remaining": total - submitted,
                "cumulative_reward": round(env._cumulative_reward, 3),
                "max_possible_reward": round(max_reward, 3),
                "normalized_score": round(max(min(norm_score, 1 - 1e-9), 1e-9), 3),
                "patients_reviewed": sorted(list(env._patients_reviewed)),
                "trials_reviewed": sorted(list(env._trials_reviewed)),
                "done": env._done,
            }, indent=2)

        super().__init__(mcp)
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._reset_count = 0

    def _compute_match_reward(
        self,
        patient_id: str,
        trial_id: str,
        eligible: bool,
        reasoning: str,
    ) -> float:
        """
        Compute reward for a single match decision.

        Scoring:
        - Correct decision: +1.0
        - Wrong decision: +0.0
        - Reasoning bonus: +0.25 if reasoning mentions key criteria
        - Review bonus: +0.1 if agent reviewed patient record before deciding
        - Review bonus: +0.05 if agent reviewed trial details before deciding
        """
        pair = (patient_id, trial_id)
        gt = GROUND_TRUTH.get(pair)

        if gt is None:
            return 0.0

        reward = 0.0

        # Decision correctness (main reward)
        if eligible == gt["eligible"]:
            reward += 1.0

        # Reasoning quality bonus
        reasoning_lower = reasoning.lower()
        key_reasons = gt.get("key_reasons", [])
        if key_reasons:
            matches = sum(
                1 for kr in key_reasons
                if any(
                    word in reasoning_lower
                    for word in kr.lower().split()
                    if len(word) > 3  # skip small words
                )
            )
            reason_ratio = matches / len(key_reasons)
            reward += 0.25 * reason_ratio

        # Review bonus — did agent actually look at the data?
        if patient_id in self._patients_reviewed:
            reward += 0.1
        if trial_id in self._trials_reviewed:
            reward += 0.05

        return reward

    def _get_max_possible_reward(self) -> float:
        """Max reward if all decisions are correct with perfect reasoning and reviews."""
        return len(self._expected_pairs) * (1.0 + 0.25 + 0.1 + 0.05)

    def reset(
        self,
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
        task: Optional[str] = None,
        **kwargs: Any,
    ) -> Observation:
        """
        Reset the environment and load a task.

        Args:
            seed: Optional random seed
            episode_id: Optional episode ID
            task: Task difficulty — 'easy', 'medium', or 'hard' (default: 'easy')
        """
        task_name = task or kwargs.get("task_name", "easy")
        if task_name not in TASKS:
            task_name = "easy"

        task_def = TASKS[task_name]
        self._task_name = task_name
        self._patient_ids = task_def["patient_ids"]
        self._trial_ids = task_def["trial_ids"]
        self._max_steps = task_def["max_steps"]
        self._submitted_matches = {}
        self._expected_pairs = {
            (pid, tid)
            for pid in self._patient_ids
            for tid in self._trial_ids
        }
        self._cumulative_reward = 0.0
        self._patients_reviewed = set()
        self._trials_reviewed = set()
        self._done = False

        self._state = State(
            episode_id=episode_id or str(uuid4()),
            step_count=0,
        )
        self._reset_count += 1

        return Observation(
            done=False,
            reward=0.0,
            metadata={
                "status": "ready",
                "task": task_name,
                "task_description": task_def["description"],
                "num_patients": len(self._patient_ids),
                "num_trials": len(self._trial_ids),
                "total_matches_required": len(self._expected_pairs),
                "max_steps": self._max_steps,
                "instructions": (
                    "You are a clinical trial matching specialist. Your job is to "
                    "review patient medical records and determine their eligibility "
                    "for each clinical trial. Use the available tools to: "
                    "(1) list_patients and list_trials to see what's available, "
                    "(2) get_patient_record and get_trial_details to review details, "
                    "(3) submit_match to submit your eligibility decisions with reasoning, "
                    "(4) get_progress to check your current score and remaining work. "
                    "Submit a decision for EVERY patient-trial pair."
                ),
            },
        )

    def _step_impl(
        self,
        action: Action,
        timeout_s: Optional[float] = None,
        **kwargs: Any,
    ) -> Observation:
        """Handle non-MCP actions (returns error)."""
        return Observation(
            done=False,
            reward=0.0,
            metadata={
                "error": f"Unknown action type: {type(action).__name__}. "
                "Use ListToolsAction or CallToolAction for MCP interactions."
            },
        )

    def step(
        self,
        action: Action,
        timeout_s: Optional[float] = None,
        **kwargs: Any,
    ) -> Observation:
        """Execute a step. Increments step count and checks for episode end."""
        self._state.step_count += 1

        # Check step limit
        if self._state.step_count >= self._max_steps:
            self._done = True

        obs = super().step(action, timeout_s=timeout_s, **kwargs)

        # Override done flag and reward on observation
        if self._done or self._state.step_count >= self._max_steps:
            max_reward = self._get_max_possible_reward()
            norm_score = (
                self._cumulative_reward / max_reward if max_reward > 0 else 0.0
            )
            obs.done = True
            obs.reward = round(max(min(norm_score, 1 - 1e-9), 1e-9), 4)
            if obs.metadata is None:
                obs.metadata = {}
            obs.metadata["final_score"] = round(norm_score, 4)
            obs.metadata["cumulative_reward"] = round(self._cumulative_reward, 3)
            obs.metadata["matches_submitted"] = len(self._submitted_matches)
            obs.metadata["matches_total"] = len(self._expected_pairs)
        else:
            # Emit per-step reward hint
            max_reward = self._get_max_possible_reward()
            obs.reward = round(
                self._cumulative_reward / max_reward if max_reward > 0 else 0.0,
                4,
            )

        return obs

    async def step_async(
        self,
        action: Action,
        timeout_s: Optional[float] = None,
        **kwargs: Any,
    ) -> Observation:
        """Async step for WebSocket handler."""
        self._state.step_count += 1

        if self._state.step_count >= self._max_steps:
            self._done = True

        obs = await super().step_async(action, timeout_s=timeout_s, **kwargs)

        if self._done or self._state.step_count >= self._max_steps:
            max_reward = self._get_max_possible_reward()
            norm_score = (
                self._cumulative_reward / max_reward if max_reward > 0 else 0.0
            )
            obs.done = True
            obs.reward = round(max(min(norm_score, 1 - 1e-9), 1e-9), 4)
            if obs.metadata is None:
                obs.metadata = {}
            obs.metadata["final_score"] = round(norm_score, 4)
            obs.metadata["cumulative_reward"] = round(self._cumulative_reward, 3)
            obs.metadata["matches_submitted"] = len(self._submitted_matches)
            obs.metadata["matches_total"] = len(self._expected_pairs)
        else:
            max_reward = self._get_max_possible_reward()
            obs.reward = round(
                self._cumulative_reward / max_reward if max_reward > 0 else 0.0,
                4,
            )

        return obs

    @property
    def state(self) -> State:
        """Get current environment state."""
        return self._state
