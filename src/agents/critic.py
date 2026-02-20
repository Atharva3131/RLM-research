# src/agents/critic.py
"""
Critic Agent

Evaluates the current solution and produces a structured critique.
The critic does NOT propose fixes. It only diagnoses problems.
"""

from typing import Dict, Any
from src.core.state import RLMState


class CriticAgent:
    def __init__(self, llm):
        """
        llm: Any callable LLM interface with a `.invoke(prompt)` method
        """
        self.llm = llm

    def build_prompt(self, task: str, solution: str) -> str:
        """
        Construct a prompt that enforces structured critique.
        """
        return (
            "You are a strict and adversarial evaluator.\n\n"
            "Your job is to critique the solution to the task below.\n"
            "Do NOT rewrite the solution.\n"
            "Do NOT suggest fixes.\n\n"
            "Evaluate ONLY correctness, reasoning gaps, and constraint violations.\n\n"
            "Return your critique strictly in the following JSON format:\n\n"
            "{\n"
            '  "critical_errors": [string],\n'
            '  "minor_issues": [string],\n'
            '  "missing_steps": [string],\n'
            '  "confidence": float  // value between 0 and 1\n'
            "}\n\n"
            f"Task:\n{task}\n\n"
            f"Solution:\n{solution}\n\n"
            "Critique JSON:"
        )

    def compute_severity(self, critique: Dict[str, Any]) -> float:
        """
        Compute a normalized error severity score ∈ [0, 1].
        """
        critical = len(critique.get("critical_errors", []))
        missing = len(critique.get("missing_steps", []))
        minor = len(critique.get("minor_issues", []))

        # Weighted severity model
        severity = (1.0 * critical) + (0.5 * missing) + (0.2 * minor)

        # Normalize using soft cap
        return min(1.0, severity / 5.0)

    def __call__(self, state: RLMState) -> RLMState:
        """
        Execute the Critic agent.
        """
        if state.current_solution is None:
            raise ValueError("CriticAgent called with no solution to evaluate.")

        prompt = self.build_prompt(state.task, state.current_solution)
        response = self.llm.invoke(prompt)

        # Parse JSON safely (minimal assumptions)
        try:
            critique: Dict[str, Any] = eval(response.strip())
        except Exception:
            critique = {
                "critical_errors": ["Malformed critique output"],
                "minor_issues": [],
                "missing_steps": [],
                "confidence": 0.0,
            }

        # Compute severity
        severity = self.compute_severity(critique)

        # Log critique and severity
        state.log_critique(critique)
        state.error_severity = severity

        return state