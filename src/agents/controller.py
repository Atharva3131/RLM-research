# src/agents/controller.py
"""
Controller Agent

Decides whether the recursive loop should continue or halt.
This agent does NOT modify the solution.
It enforces recursion limits, convergence, and degeneration checks.
"""

from src.core.state import RLMState


class ControllerAgent:
    def __init__(
        self,
        severity_threshold: float = 0.15,
        improvement_threshold: float = 0.05,
    ):
        """
        severity_threshold:
            Below this value, the solution is considered acceptable.

        improvement_threshold:
            Minimum required improvement to justify another recursion step.
        """
        self.severity_threshold = severity_threshold
        self.improvement_threshold = improvement_threshold

    def compute_improvement_delta(self, state: RLMState) -> float:
        """
        Estimate improvement between the last two iterations
        using error severity reduction.
        """
        if len(state.critique_history) < 2:
            return 1.0  # Assume improvement at first iteration

        prev = state.critique_history[-2]
        curr = state.critique_history[-1]

        prev_sev = state.error_severity
        curr_sev = state.error_severity

        # Conservative delta estimate
        delta = prev_sev - curr_sev if prev_sev is not None else 0.0
        return max(0.0, delta)

    def detect_degeneration(self, state: RLMState) -> bool:
        """
        Detect degeneration patterns in recursion.
        """
        if len(state.solution_history) < 3:
            return False

        last = state.solution_history[-1]
        prev = state.solution_history[-2]

        # Simple degeneration heuristic:
        # identical or near-identical outputs
        return last.strip() == prev.strip()

    def __call__(self, state: RLMState) -> RLMState:
        """
        Execute controller decision.
        """
        state.increment_step()

        # Safety: hard stop
        if state.recursion_step >= state.max_recursion_steps:
            state.halt = True
            return state

        # Severity-based stop
        if state.error_severity is not None:
            if state.error_severity < self.severity_threshold:
                state.halt = True
                return state

        # Degeneration check
        if self.detect_degeneration(state):
            state.halt = True
            return state

        # Continue recursion
        state.halt = False
        return state