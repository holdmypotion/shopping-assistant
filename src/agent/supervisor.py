from src.state import State
from langgraph.types import Command
from langgraph.graph import END
from langchain_core.messages import AIMessage
from src.utils.supervisor import (
    has_image_in_message, is_human_message, is_enough_info_for_product_search, no_image_no_data
)


def supervisor_node(state: State) -> Command:
    messages = state.get("messages", [])
    current_question = state.get("current_question")
    found_products = state.get("found_products")
    questions_asked_count = state.get("questions_asked_count", 0)

    
    if found_products is not None:
        return Command(goto="explorer")

    if messages:
        latest_message = messages[-1]
        if is_human_message(latest_message):
            if has_image_in_message(latest_message):
                return Command(goto="image_analyser")
            else:
                return Command(goto="info_gatherer")
        else:
            if no_image_no_data(state):
                return Command(
                    goto=END,
                    update={
                        "messages": state["messages"] + [AIMessage(content="Please provide an image or some information about what you are looking for", name="supervisor")],
                    }
                ) 

    if current_question is not None:
        return Command(
            goto=END,
            update={"messages": state["messages"] + [AIMessage(content=current_question, name="supervisor")]}
        )

    if is_enough_info_for_product_search(state):
        return Command(goto="product_finder")
    else:
        if questions_asked_count < 3:
            return Command(goto="info_prober")
        else:
            return Command(goto="product_finder")

