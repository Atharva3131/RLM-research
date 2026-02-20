# src/agents/generator.py
"""
Generator Agent

Responsible for producing the initial candidate solution
for a given task. This agent does NOT perform self-critique
or reflection. It is intentionally fast and greedy.
"""

from typing import Dict, Any
from src.core.state import RLMState


class GeneratorAgent:
    def __init__(self, llm):
        """
        llm: Any callable LLM interface with a `.invoke(prompt)` method
        """
        self.llm = llm

    def build_prompt(self, task: str) -> str:
        """
        Construct a minimal prompt for first-pass solution generation.
        """
        return (
            "You are a capable problem-solving assistant.\n\n"
            "Solve the following task to the best of your ability.\n"
            "Do not critique or reflect on your answer.\n\n"
            f"Task:\n{task}\n\n"
            "Answer:"
        )

    def __call__(self, state: RLMState) -> RLMState:
        """
        Execute the Generator agent.
        """
        prompt = self.build_prompt(state.task)
        response = self.llm.invoke(prompt)

        # Normalize response
        solution = response.strip()

        # Log solution in state
        state.log_solution(solution)

        return state