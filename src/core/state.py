# src/core/state.py
"""
State definition for Recursive Self-Refinement Agent (RLM-Agent).

This state object is passed between nodes in the LangGraph
and tracks the evolution of the solution across recursion steps.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class RLMState:
    """
    Global state for recursive agent execution.
    """

    # ---- Task ----
    task: str

    # ---- Solution Tracking ----
    current_solution: Optional[str] = None
    solution_history: List[str] = field(default_factory=list)

    # ---- Critique Tracking ----
    critique: Optional[Dict[str, Any]] = None
    critique_history: List[Dict[str, Any]] = field(default_factory=list)

    # ---- Recursion Control ----
    recursion_step: int = 0
    max_recursion_steps: int = 5
    halt: bool = False

    # ---- Metrics ----
    error_severity: Optional[float] = None
    improvement_delta: Optional[float] = None

    # ---- Metadata ----
    metadata: Dict[str, Any] = field(default_factory=dict)

    def log_solution(self, solution: str):
        """Store solution version and update current solution."""
        self.current_solution = solution
        self.solution_history.append(solution)

    def log_critique(self, critique: Dict[str, Any]):
        """Store critique output."""
        self.critique = critique
        self.critique_history.append(critique)

    def increment_step(self):
        """Advance recursion counter."""
        self.recursion_step += 1

    def should_halt(self) -> bool:
        """
        Centralized halt check.
        Controller node should set `halt = True` when stopping conditions are met.
        """
        return self.halt or self.recursion_step >= self.max_recursion_steps