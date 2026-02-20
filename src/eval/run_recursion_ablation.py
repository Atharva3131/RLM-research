# src/eval/run_recursion_ablation.py
"""
Recursion-depth ablation study for RLM-Agent.
"""

import csv
from dotenv import load_dotenv
import os

from src.core.llm import MistralLLM
from src.graph.rlm_graph import build_rlm_graph
from src.core.state import RLMState
from src.eval.metrics import success_proxy, output_length


def main():
    load_dotenv()

    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY not found")

    llm = MistralLLM(
        api_key=api_key,
        model="mistral-large-latest",
        temperature=0.0,
    )

    task = "Explain the difference between BFS and DFS."

    results = []

    for max_depth in [1, 2, 3, 4, 5]:
        graph = build_rlm_graph(llm)

        state = RLMState(
            task=task,
            max_recursion_steps=max_depth,
        )

        final_state = graph.invoke(state)
        out = final_state["current_solution"]

        results.append({
            "max_recursion_depth": max_depth,
            "recursion_steps_used": final_state["recursion_step"],
            "success": success_proxy(out),
            "num_llm_calls": len(final_state["solution_history"]) * 2,
            "output_length": output_length(out),
        })

    # ---- Save CSV ----
    with open("recursion_ablation.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print("Recursion-depth ablation complete.")
    print("Saved to recursion_ablation.csv")


if __name__ == "__main__":
    main()