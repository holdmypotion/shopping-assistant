from typing import TypedDict
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate
from src.state import State
from langgraph.types import Command
from langgraph.graph import END
from langchain_core.messages import AIMessage
from typing import Literal
from src.utils.supervisor import has_image_in_message, is_human_message, is_enough_info_for_product_search

prompt = PromptTemplate(
    template="""
You are a supervisor coordinating a shopping assistant workflow.
Your job is to route the user to the appropriate agent based on the user's request.

Role:
1. If the user has provided an image, route to the image_analyser agent.
2. If the user has not provided an image, ask them to provide an image.
3. After image analysis, route to the info_prober agent to gather user preferences (maximum 3 questions).
4. If user preferences are complete, route to the product_finder agent.
5. If products have been found, route to the result_aggregator agent to present them.

NOTE: The system will ask at most 3 questions to gather user preferences efficiently.
    """,
    input_variables=["members"],
)

MEMBERS = ["image_analyser", "info_prober", "info_gatherer", "product_finder", "result_aggregator"]
OPTIONS = ["FINISH"] + MEMBERS

class Router(TypedDict):
    """Route to the next node."""
    next_node: Literal[*OPTIONS]
    message: str


supervisor = create_react_agent(
    name="supervisor",
    model=init_chat_model(model="gpt-4o"),
    tools=[],
    prompt=prompt.format(members=MEMBERS),
    response_format=Router,
)


def supervisor_node(state: State) -> Command:
    """
    Simple supervisor logic:
    1. if latest_message is a human message
        1. if message has_image then route to image_analyser
        2. else route to info_gatherer
    2. if current_question is not None, route to END
    3. if is_enough_info_for_product_search() is True, route to product_finder 
       else route to info_prober (do this max 3 times otherwise route to product_finder)
    4. if found_products is not None, route to result_aggregator
    """
    messages = state.get("messages", [])
    current_question = state.get("current_question")
    found_products = state.get("found_products")
    questions_asked_count = state.get("questions_asked_count", 0)
    
    # Step 1: Check if latest message is human
    if messages:
        latest_message = messages[-1]
        if is_human_message(latest_message):
            # Step 1.1: If message has image, route to image_analyser
            if has_image_in_message(latest_message):
                return Command(goto="image_analyser")
            # Step 1.2: Else route to info_gatherer
            else:
                return Command(goto="info_gatherer")
    
    # Step 2: If current_question is not None, route to END
    if current_question is not None:
        return Command(
            goto=END,
            update={"messages": state["messages"] + [AIMessage(content=current_question, name="supervisor")]}
        )
    
    # Step 4: If found_products is not None, route to result_aggregator
    if found_products is not None:
        return Command(goto="result_aggregator")
    
    # Step 3: Check if enough info for product search
    if is_enough_info_for_product_search(state):
        return Command(goto="product_finder")
    else:
        # Route to info_prober max 3 times, otherwise route to product_finder
        if questions_asked_count < 3:
            return Command(goto="info_prober")
        else:
            return Command(goto="product_finder")

