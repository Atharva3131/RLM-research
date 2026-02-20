# src/baselines/react.py
"""
ReAct Baseline (No Recursion)

Implements a simple Plan → Act → Observe loop
without self-critique, refinement, or recursion.
"""

class ReActBaseline:
    def __init__(self, llm, max_steps: int = 3):
        """
        llm: Any callable LLM interface with a `.invoke(prompt)` method
        max_steps: Number of reasoning/action steps (fixed, no recursion)
        """
        self.llm = llm
        self.max_steps = max_steps

    def build_prompt(self, task: str, history: str) -> str:
        """
        Construct a ReAct-style prompt.
        """
        return (
            "You are an intelligent assistant using the ReAct framework.\n\n"
            "At each step, follow this format:\n"
            "Thought: your reasoning\n"
            "Action: what you do (think, compute, summarize)\n"
            "Observation: result of the action\n\n"
            "Do NOT revise past steps.\n"
            "Do NOT self-critique or refine earlier outputs.\n\n"
            f"Task:\n{task}\n\n"
            f"History:\n{history}\n\n"
            "Next step:"
        )

    def run(self, task: str) -> str:
        """
        Execute ReAct reasoning for a fixed number of steps.
        """
        history = ""

        for step in range(self.max_steps):
            prompt = self.build_prompt(task, history)
            response = self.llm.invoke(prompt)
            history += f"\nStep {step + 1}:\n{response.strip()}\n"

        # Final answer extraction
        final_prompt = (
            "Based on the reasoning above, provide the final answer only.\n\n"
            f"{history}\n\n"
            "Final Answer:"
        )

        final_response = self.llm.invoke(final_prompt)
        return final_response.strip()