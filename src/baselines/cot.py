# src/baselines/cot.py
"""
Chain-of-Thought (CoT) Baseline

A single-pass baseline that encourages explicit reasoning
but performs no self-critique, correction, or recursion.
"""

class ChainOfThoughtBaseline:
    def __init__(self, llm):
        """
        llm: Any callable LLM interface with a `.invoke(prompt)` method
        """
        self.llm = llm

    def build_prompt(self, task: str) -> str:
        """
        Construct a prompt that elicits chain-of-thought reasoning.
        """
        return (
            "You are a reasoning assistant.\n\n"
            "Solve the following task step by step, "
            "showing your reasoning clearly before giving the final answer.\n\n"
            f"Task:\n{task}\n\n"
            "Reasoning and Answer:"
        )

    def run(self, task: str) -> str:
        """
        Execute Chain-of-Thought inference.
        """
        prompt = self.build_prompt(task)
        response = self.llm.invoke(prompt)
        return response.strip()