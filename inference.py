#!/usr/bin/env python3
"""
Baseline inference script for Clinical Trial Patient Matching.

Uses the OpenAI API client to run a model against the environment.
Reads API credentials from environment variables.

Usage:
    API_BASE_URL=<url> MODEL_NAME=<model> HF_TOKEN=<token> python inference.py

Environment Variables:
    API_BASE_URL  — The API endpoint for the LLM
    MODEL_NAME    — The model identifier to use
    HF_TOKEN      — Your Hugging Face / API key
"""

import asyncio
import json
import os
import sys
from typing import List, Optional

from openai import OpenAI

# ---------------------------------------------------------------------------
# Configuration from environment variables
# ---------------------------------------------------------------------------
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3.3-70B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")

# Optional: set to a local Docker image name when using from_docker_image()
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

# Environment server URL — set to your running server or HF Space URL
ENV_BASE_URL = os.environ.get("ENV_BASE_URL", "http://localhost:8000")
IMAGE_NAME = LOCAL_IMAGE_NAME or "clinical-trial-match:latest"
BENCHMARK = "clinical_trial_match"

TASKS = ["easy", "medium", "hard"]
MAX_STEPS_PER_TASK = {"easy": 25, "medium": 50, "hard": 80}
SUCCESS_SCORE_THRESHOLD = 0.6


# ---------------------------------------------------------------------------
# Structured logging helpers — [START], [STEP], [END]
# ---------------------------------------------------------------------------

def log_start(task: str, env: str, model: str) -> None:
    print(
        f"[START] task={task} env={env} model={model}",
        flush=True,
    )


def log_step(
    step: int,
    action: str,
    reward: float,
    done: bool,
    error: Optional[str] = None,
) -> None:
    error_str = f' error="{error}"' if error else ""
    print(
        f"[STEP] step={step} action={json.dumps(action)} "
        f"reward={reward:.4f} done={done}{error_str}",
        flush=True,
    )


def log_end(
    success: bool,
    steps: int,
    score: float,
    rewards: List[float],
) -> None:
    print(
        f"[END] success={success} steps={steps} "
        f"score={score:.4f} rewards={json.dumps([round(r, 4) for r in rewards])}",
        flush=True,
    )


# ---------------------------------------------------------------------------
# System prompt for the agent
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a clinical trial matching specialist. Your job is to review patient \
medical records and determine their eligibility for clinical trials.

You have these tools available:
- list_patients(): Get summaries of all patients
- get_patient_record(patient_id): Get a patient's full medical record
- list_trials(): Get summaries of all trials
- get_trial_details(trial_id): Get a trial's full protocol with criteria
- submit_match(patient_id, trial_id, eligible, reasoning): Submit your decision
- get_progress(): Check your current score and remaining work

STRATEGY:
1. First, call list_patients() and list_trials() to understand the scope.
2. For each patient, call get_patient_record(patient_id) to review their data.
3. For each trial, call get_trial_details(trial_id) to review criteria.
4. For each patient-trial pair, evaluate inclusion/exclusion criteria carefully.
5. Use submit_match() to submit each decision with clear reasoning.
6. Call get_progress() periodically to check your score.

Be thorough and reference specific criteria in your reasoning. \
Every patient must be evaluated against every trial.\
"""


def build_tool_definitions() -> list:
    """Build OpenAI-compatible tool definitions."""
    return [
        {
            "type": "function",
            "function": {
                "name": "list_patients",
                "description": "List all patients with brief summaries (ID, name, age, sex, conditions)",
                "parameters": {"type": "object", "properties": {}, "required": []},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_patient_record",
                "description": "Get complete medical record for a patient",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "patient_id": {
                            "type": "string",
                            "description": "Patient ID (e.g., 'P001')",
                        }
                    },
                    "required": ["patient_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_trials",
                "description": "List all clinical trials with brief summaries",
                "parameters": {"type": "object", "properties": {}, "required": []},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_trial_details",
                "description": "Get complete protocol for a clinical trial including inclusion/exclusion criteria",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "trial_id": {
                            "type": "string",
                            "description": "Trial ID (e.g., 'T001')",
                        }
                    },
                    "required": ["trial_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "submit_match",
                "description": "Submit eligibility decision for a patient-trial pair",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "patient_id": {
                            "type": "string",
                            "description": "Patient ID",
                        },
                        "trial_id": {
                            "type": "string",
                            "description": "Trial ID",
                        },
                        "eligible": {
                            "type": "boolean",
                            "description": "True if patient meets all inclusion criteria and no exclusion criteria",
                        },
                        "reasoning": {
                            "type": "string",
                            "description": "Detailed reasoning referencing specific criteria and patient data",
                        },
                    },
                    "required": ["patient_id", "trial_id", "eligible", "reasoning"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_progress",
                "description": "Check current matching progress, score, and remaining work",
                "parameters": {"type": "object", "properties": {}, "required": []},
            },
        },
    ]


def get_model_response(
    client: OpenAI,
    messages: list,
    tools: list,
) -> object:
    """Get model response with tool calling."""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.1,
            max_tokens=4096,
        )
        return response
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", flush=True)
        return None


async def run_task(task_name: str) -> dict:
    """Run a single task and return results."""
    from clinical_trial_match import ClinicalTrialEnv

    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
    tools = build_tool_definitions()
    max_steps = MAX_STEPS_PER_TASK[task_name]

    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=task_name, env=BENCHMARK, model=MODEL_NAME)

    try:
        # Connect to running server (local or Docker or HF Space)
        # If you have Docker, you can also use:
        #   env = await ClinicalTrialEnv.from_docker_image(IMAGE_NAME)
        async with ClinicalTrialEnv(base_url=ENV_BASE_URL) as env:
            # Reset environment with task
            result = await env.reset(task=task_name)

            # Task descriptions for the prompt
            task_descriptions = {
                "easy": "Screen 3 patients against 2 clinical trials with clear-cut criteria.",
                "medium": "Screen 5 patients against 3 clinical trials with nuanced criteria including lab values and medication conflicts.",
                "hard": "Screen 8 patients against 4 trials with subtle criteria including temporal conditions and drug washout periods.",
            }
            task_matches = {"easy": 6, "medium": 15, "hard": 32}
            task_patients = {"easy": 3, "medium": 5, "hard": 8}
            task_trials = {"easy": 2, "medium": 3, "hard": 4}

            # Build initial messages
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"Task: {task_name.upper()} — {task_descriptions[task_name]}\n"
                        f"Patients: {task_patients[task_name]}, "
                        f"Trials: {task_trials[task_name]}, "
                        f"Matches required: {task_matches[task_name]}\n\n"
                        "Start by calling list_patients() and list_trials() to see what's available, "
                        "then review each patient and trial, and submit your eligibility decisions."
                    ),
                },
            ]

            done = False

            for step in range(1, max_steps + 1):
                if done:
                    break

                response = get_model_response(client, messages, tools)
                if response is None:
                    break

                choice = response.choices[0]
                message = choice.message

                # Append assistant message (strip None/unsupported fields for provider compat)
                msg_dict = message.model_dump(exclude_none=True)
                # Also remove any extra fields some providers don't accept
                for key in ["annotations", "audio"]:
                    msg_dict.pop(key, None)
                messages.append(msg_dict)

                # Check if model wants to call tools
                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        fn_name = tool_call.function.name
                        try:
                            fn_args = json.loads(tool_call.function.arguments) or {}
                        except (json.JSONDecodeError, TypeError):
                            fn_args = {}

                        # Execute tool via environment
                        action_str = f"{fn_name}({json.dumps(fn_args)})"
                        tool_result = await env.call_tool(fn_name, **fn_args)

                        # Parse result
                        tool_result_str = str(tool_result)
                        reward = 0.0

                        # Get updated env state
                        try:
                            progress_result = await env.call_tool("get_progress")
                            progress = json.loads(str(progress_result))
                            reward = float(progress.get("normalized_score", 0.0))
                            done = progress.get("done", False)
                        except Exception:
                            pass

                        rewards.append(reward)
                        steps_taken = step

                        log_step(
                            step=step,
                            action=action_str,
                            reward=reward,
                            done=done,
                            error=None,
                        )

                        # Add tool result to messages
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": tool_result_str,
                        })

                        if done:
                            break
                else:
                    # Model replied without tools — note it and continue
                    if message.content:
                        log_step(
                            step=step,
                            action=f"text: {message.content[:100]}",
                            reward=rewards[-1] if rewards else 0.0,
                            done=False,
                        )

                if choice.finish_reason == "stop" and not message.tool_calls:
                    # Model finished talking, prompt it to continue if not done
                    if not done:
                        messages.append({
                            "role": "user",
                            "content": "Continue evaluating and submitting match decisions. Call get_progress() to see remaining work.",
                        })

            # Final score
            score = rewards[-1] if rewards else 0.0
            score = max(min(score, 1 - 1e-9), 1e-9)
            success = score >= SUCCESS_SCORE_THRESHOLD

    except Exception as e:
        print(f"[DEBUG] Task {task_name} error: {e}", flush=True)
        import traceback
        traceback.print_exc()

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

    return {
        "task": task_name,
        "score": score,
        "success": success,
        "steps": steps_taken,
    }


async def main() -> None:
    """Run all tasks sequentially."""
    print("=" * 60, flush=True)
    print("Clinical Trial Patient Matching — Baseline Inference", flush=True)
    print(f"Model: {MODEL_NAME}", flush=True)
    print(f"API: {API_BASE_URL}", flush=True)
    print("=" * 60, flush=True)

    all_results = []

    for task_name in TASKS:
        print(f"\n{'─' * 40}", flush=True)
        print(f"Running task: {task_name}", flush=True)
        print(f"{'─' * 40}", flush=True)

        result = await run_task(task_name)
        all_results.append(result)

    # Summary
    print(f"\n{'=' * 60}", flush=True)
    print("RESULTS SUMMARY", flush=True)
    print(f"{'=' * 60}", flush=True)
    for r in all_results:
        status = "✅ PASS" if r["success"] else "❌ FAIL"
        print(
            f"  {r['task']:8s}  score={r['score']:.4f}  "
            f"steps={r['steps']:3d}  {status}",
            flush=True,
        )

    avg_score = sum(r["score"] for r in all_results) / len(all_results)
    print(f"\n  Average score: {avg_score:.4f}", flush=True)
    print(f"{'=' * 60}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
