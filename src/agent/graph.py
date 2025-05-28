"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations
from src.agent.supervisor import supervisor_node
from src.agent.image_analyser import image_analyser_node
from src.agent.info_prober import info_prober_node
from src.agent.info_gatherer import info_gatherer_node
from src.agent.product_finder import product_finder_node
from src.agent.explorer import explore_products_node
from src.state import State
from langgraph.graph import StateGraph, START

graph = (
    StateGraph(State)
    .add_node("supervisor", supervisor_node)
    .add_node("image_analyser", image_analyser_node)
    .add_node("info_prober", info_prober_node)
    .add_node("info_gatherer", info_gatherer_node)
    .add_node("product_finder", product_finder_node)
    .add_node("explorer", explore_products_node)
    .add_edge(START, "supervisor")
    .compile(name="Shopping Assistant")
)