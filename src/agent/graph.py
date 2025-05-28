"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations
from src.agent.supervisor import supervisor_node
from src.agent.image_analyser import image_analyser_node
from src.agent.info_prober import info_prober_node
from src.agent.info_gatherer import info_gatherer_node
from src.agent.result_aggregator import result_aggregator_node
from src.agent.product_finder import product_finder_node
from src.state import State
from langgraph.graph import StateGraph, START
from langgraph.graph import END

# class Configuration(TypedDict):
#     """Configurable parameters for the agent.

#     Set these when creating assistants OR when invoking the graph.
#     See: https://langchain-ai.github.io/langgraph/cloud/how-tos/configuration_cloud/
#     """

#     my_configurable_param: str


# @dataclass
# class State:
#     """Input state for the agent.

#     Defines the initial structure of incoming data.
#     See: https://langchain-ai.github.io/langgraph/concepts/low_level/#state
#     """

#     changeme: str = "example"

def route_supervisor(state: State):
    """Route from supervisor based on the next_node in state."""
    return state.get("next_node")

graph = (
    StateGraph(State)
    .add_node("supervisor", supervisor_node)
    .add_node("image_analyser", image_analyser_node)
    .add_node("info_prober", info_prober_node)
    .add_node("info_gatherer", info_gatherer_node)
    .add_node("product_finder", product_finder_node)
    .add_node("result_aggregator", result_aggregator_node)
    .add_edge(START, "supervisor")
    .compile(name="Shopping Assistant")
)