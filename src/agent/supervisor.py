from src.state import State
from langgraph.types import Command
from langgraph.graph import END
from src.utils.common import (
    has_image_in_human_message,
)


def supervisor_node(state: State) -> Command:
    messages = state.get("messages", [])
    next_node = state.get("next_node", 'supervisor')

    if messages:
        latest_message = messages[-1]
        if has_image_in_human_message(latest_message):
            return Command(goto="image_analyser")
        else:
            return Command(goto="product_search")

    if next_node != "supervisor":
        return Command(goto=next_node)

    return Command(goto=END) 

