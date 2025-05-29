"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations
from src.agent.supervisor import supervisor_node
from src.agent.image_analyser import image_analyser_node
from src.agent.product_search import product_search_node
from src.state import State
from langgraph.graph import StateGraph, START, END


def route_supervisor(state: State):
    """Route from supervisor based on the next_node in state."""
    return state.get("next_node")

graph = (
    StateGraph(State)
    .add_node("supervisor", supervisor_node)
    .add_node("image_analyser", image_analyser_node)
    .add_node("product_search", product_search_node)
    .add_edge(START, "supervisor")
    .compile(name="Shopping Assistant")
)
