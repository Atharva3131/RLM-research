# src/eval/metrics.py
"""
Utility functions for computing evaluation metrics.
"""

def success_proxy(output: str) -> int:
    """
    Proxy success metric.
    For now: non-empty and reasonably long answer.
    Later: replace with task-specific evaluators.
    """
    if not output:
        return 0
    return 1 if len(output.strip()) > 50 else 0


def output_length(output: str) -> int:
    return len(output.strip())