# src/eval/evaluator.py
"""
Evaluator that runs all baselines and the recursive agent
on a single task and collects metrics.
"""

from src.baselines.single_pass import SinglePassBaseline
from src.baselines.cot import ChainOfThoughtBaseline
from src.baselines.react import ReActBaseline
from src.graph.rlm_graph import build_rlm_graph
from src.core.state import RLMState

from src.eval.metrics import success_proxy, output_length


class Evaluator:
    def __init__(self, llm):
        self.llm = llm

        self.single_pass = SinglePassBaseline(llm)
        self.cot = ChainOfThoughtBaseline(llm)
        self.react = ReActBaseline(llm, max_steps=3)
        self.rlm_graph = build_rlm_graph(llm)

    def evaluate_task(self, task: str, task_id: int = 0):
        results = []

        # ---- Single-pass ----
        out = self.single_pass.run(task)
        results.append({
            "method": "single_pass",
            "task_id": task_id,
            "success": success_proxy(out),
            "num_llm_calls": 1,
            "recursion_steps": 0,
            "output_length": output_length(out),
        })

        # ---- CoT ----
        out = self.cot.run(task)
        results.append({
            "method": "cot",
            "task_id": task_id,
            "success": success_proxy(out),
            "num_llm_calls": 1,
            "recursion_steps": 0,
            "output_length": output_length(out),
        })

        # ---- ReAct ----
        out = self.react.run(task)
        results.append({
            "method": "react",
            "task_id": task_id,
            "success": success_proxy(out),
            "num_llm_calls": 4,  # 3 steps + final answer
            "recursion_steps": 0,
            "output_length": output_length(out),
        })

        # ---- RLM Agent ----
        state = RLMState(task=task, max_recursion_steps=5)
        final_state = self.rlm_graph.invoke(state)

        out = final_state["current_solution"]
        results.append({
            "method": "rlm",
            "task_id": task_id,
            "success": success_proxy(out),
            "num_llm_calls": len(final_state["solution_history"]) * 2,
            "recursion_steps": final_state["recursion_step"],
            "output_length": output_length(out),
        })

        return results