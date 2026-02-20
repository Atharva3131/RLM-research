# src/agents/refiner.py
"""
Refiner Agent

Improves the current solution strictly based on the structured critique.
The refiner does NOT re-solve the task from scratch.
It applies minimal, targeted corrections.
"""

from typing import Dict, Any
from src.core.state import RLMState


class RefinerAgent:
    def __init__(self, llm):
        """
        llm: Any callable LLM interface with a `.invoke(prompt)` method
        """
        self.llm = llm

    def build_prompt(
        self,
        task: str,
        solution: str,
        critique: Dict[str, Any],
    ) -> str:
        """
        Construct a prompt that enforces constrained refinement.
        """
        return (
            "You are a solution refinement agent.\n\n"
            "You will be given:\n"
            "1. The original task\n"
            "2. The current solution\n"
            "3. A structured critique of the solution\n\n"
            "Your job is to improve the solution by addressing ONLY the issues "
            "explicitly mentioned in the critique.\n\n"
            "Rules:\n"
            "- Do NOT rewrite the solution from scratch\n"
            "- Do NOT introduce new ideas not required by the critique\n"
            "- Preserve all correct parts of the solution\n"
            "- Make the smallest changes necessary\n\n"
            "Return ONLY the revised solution text. No explanations.\n\n"
            f"Task:\n{task}\n\n"
            f"Current Solution:\n{solution}\n\n"
            f"Critique:\n{critique}\n\n"
            "Revised Solution:"
        )

    def __call__(self, state: RLMState) -> RLMState:
        """
        Execute the Refiner agent.
        """
        if state.current_solution is None:
            raise ValueError("RefinerAgent called with no solution to refine.")

        if state.critique is None:
            raise ValueError("RefinerAgent called with no critique available.")

        prompt = self.build_prompt(
            task=state.task,
            solution=state.current_solution,
            critique=state.critique,
        )

        response = self.llm.invoke(prompt)

        refined_solution = response.strip()

        # Log refined solution
        state.log_solution(refined_solution)

        return state