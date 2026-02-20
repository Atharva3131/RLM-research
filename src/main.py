# src/main.py
"""
Main entry point for running Recursive Self-Refinement Agent (RLM-Agent)
and all baseline comparisons.
"""

from dotenv import load_dotenv
import os

# ---- Core system ----
from src.graph.rlm_graph import build_rlm_graph
from src.core.state import RLMState
from src.core.llm import MistralLLM

# ---- Baselines ----
from src.baselines.single_pass import SinglePassBaseline
from src.baselines.cot import ChainOfThoughtBaseline
from src.baselines.react import ReActBaseline


def main():
    # ---- Load environment variables ----
    load_dotenv()

    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY not found in .env file")

    # ---- Initialize LLM (shared across all methods) ----
    llm = MistralLLM(
        api_key=api_key,
        model="mistral-large-latest",
        temperature=0.0,
    )

    # ---- Task (can be replaced by dataset later) ----
    task = "Explain recursion with a simple example."

    print("\n==============================")
    print("TASK:")
    print(task)
    print("==============================\n")

    # ======================================================
    # Baseline 1: Single-Pass
    # ======================================================
    single_pass = SinglePassBaseline(llm)
    sp_output = single_pass.run(task)

    print("----- Single-Pass Baseline -----")
    print(sp_output)
    print()

    # ======================================================
    # Baseline 2: Chain-of-Thought
    # ======================================================
    cot = ChainOfThoughtBaseline(llm)
    cot_output = cot.run(task)

    print("----- Chain-of-Thought Baseline -----")
    print(cot_output)
    print()

    # ======================================================
    # Baseline 3: ReAct (No Recursion)
    # ======================================================
    react = ReActBaseline(llm, max_steps=3)
    react_output = react.run(task)

    print("----- ReAct Baseline -----")
    print(react_output)
    print()

    # ======================================================
    # Proposed Method: Recursive Self-Refinement Agent
    # ======================================================
    graph = build_rlm_graph(llm)

    rlm_state = RLMState(
        task=task,
        max_recursion_steps=5,
    )

    final_state = graph.invoke(rlm_state)

    print("----- Recursive Self-Refinement Agent (RLM) -----")
    print(final_state["current_solution"])
    print()

    # ---- Optional debug info ----
    print("Recursion steps used:", final_state["recursion_step"])
    print("Total solution versions:", len(final_state["solution_history"]))
    print("===============================================")


if __name__ == "__main__":
    main()