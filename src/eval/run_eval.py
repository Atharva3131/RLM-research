# src/eval/run_eval.py
"""
Runs evaluation over a list of tasks and saves results to CSV.
"""

import csv
from dotenv import load_dotenv
import os

from src.core.llm import MistralLLM
from src.eval.evaluator import Evaluator


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

    evaluator = Evaluator(llm)

    tasks = [
        "Explain recursion with a simple example.",
    "Write a Python function to check if a number is prime.",
    "Explain the difference between BFS and DFS.",
    """The following Python function is intended to check whether a string
    is a palindrome, ignoring case and non-alphanumeric characters.
    Identify the bug(s) and provide a corrected version.

    def is_palindrome(s):
        s = s.lower()
        s = ''.join(c for c in s if c.isalnum())
        return s == s.reverse()
    """
    ]

    all_results = []

    for i, task in enumerate(tasks):
        results = evaluator.evaluate_task(task, task_id=i)
        all_results.extend(results)

    # ---- Save CSV ----
    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
        writer.writeheader()
        writer.writerows(all_results)

    print("Evaluation complete. Results saved to results.csv")


if __name__ == "__main__":
    main()