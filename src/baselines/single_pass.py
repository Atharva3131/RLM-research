# src/baselines/single_pass.py
"""
Single-Pass Baseline

A minimal baseline that invokes the LLM exactly once
to solve the task, with no reasoning prompts,
no critique, and no recursion.
"""

from typing import Optional


class SinglePassBaseline:
    def __init__(self, llm):
        """
        llm: Any callable LLM interface with a `.invoke(prompt)` method
        """
        self.llm = llm

    def build_prompt(self, task: str) -> str:
        """
        Construct a minimal prompt for single-pass inference.
        """
        return (
            "Solve the following task.\n\n"
            f"Task:\n{task}\n\n"
            "Answer:"
        )

    def run(self, task: str) -> str:
        """
        Execute single-pass inference.
        """
        prompt = self.build_prompt(task)
        response = self.llm.invoke(prompt)
        return response.strip()