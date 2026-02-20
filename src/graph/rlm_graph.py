# src/graph/rlm_graph.py
"""
LangGraph wiring for Recursive Self-Refinement Agent (RLM-Agent).

This graph connects:
Generator → Critic → Refiner → Controller
and loops until the Controller halts execution.
"""

from langgraph.graph import StateGraph, END

from src.core.state import RLMState
from src.agents.generator import GeneratorAgent
from src.agents.critic import CriticAgent
from src.agents.refiner import RefinerAgent
from src.agents.controller import ControllerAgent


def build_rlm_graph(llm):
    """
    Build and return a compiled LangGraph for the RLM-Agent.
    """

    # ---- Instantiate Agents ----
    generator = GeneratorAgent(llm)
    critic = CriticAgent(llm)
    refiner = RefinerAgent(llm)
    controller = ControllerAgent()

    # ---- Create Graph ----
    graph = StateGraph(RLMState)

    # ---- Register Nodes ----
    graph.add_node("generator", generator)
    graph.add_node("critic", critic)
    graph.add_node("refiner", refiner)
    graph.add_node("controller", controller)

    # ---- Define Edges ----
    graph.set_entry_point("generator")

    graph.add_edge("generator", "critic")
    graph.add_edge("critic", "refiner")
    graph.add_edge("refiner", "controller")

    # ---- Conditional Recursion ----
    def route_after_controller(state: RLMState):
        if state.should_halt():
            return END
        return "critic"

    graph.add_conditional_edges(
        "controller",
        route_after_controller,
        {
            "critic": "critic",
            END: END,
        },
    )

    # ---- Compile Graph ----
    return graph.compile()