from typing import TypedDict
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate
from src.state import State
from langgraph.types import Command
from langgraph.graph import END
from langchain_core.messages import AIMessage
from typing import Literal

prompt = PromptTemplate(
    template="""
You are a supervisor coordinating a shopping assistant workflow.
Your job is to route the user to the appropriate agent based on the user's request.

Role:
1. Greet the user and introduce yourself.
2. If the user has provided an image, route to the image_analyser agent.
3. If the user has not provided an image, ask them to provide an image.
4. After image analysis, route to the info_prober agent to gather user preferences.
5. If user preferences are complete, route to the product_finder agent.
6. If products have been found, route to the result_aggregator agent to present them.

NOTE: When you have enough information to provide a complete response to the user, respond with FINISH.
    """,
    input_variables=["members"],
)

MEMBERS = ["image_analyser", "info_prober", "product_finder", "result_aggregator"]
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
    messages = state.get("messages", [])
    image_registered = state.get("image_registered", False)
    analysis_output = state.get("analysis_output")
    user_preferences = state.get("user_preferences")
    found_products = state.get("found_products")
    
    # If products have been found, route to result aggregator
    if found_products:
        return Command(
            goto="result_aggregator",
            update={
                "next_node": "result_aggregator",
                "messages": state["messages"] + [AIMessage(content="Perfect! I found some products for you. Let me present them in a nice format...", name="supervisor")]
            }
        )
    
    # If we have user preferences and they're complete, route to product finder
    if user_preferences and user_preferences.is_complete and analysis_output:
        return Command(
            goto="product_finder",
            update={
                "next_node": "product_finder",
                "messages": state["messages"] + [AIMessage(content="Perfect! Now let me search for products that match your preferences...", name="supervisor")]
            }
        )
    
    # If image has been analyzed but no user preferences collected yet, route to info_prober
    if image_registered and analysis_output and (not user_preferences or not user_preferences.is_complete):
        return Command(
            goto="info_prober",
            update={
                "next_node": "info_prober",
                "messages": state["messages"] + [AIMessage(content="Great! I've analyzed your image. Now let me ask you a few questions to better understand what you're looking for...", name="supervisor")]
            }
        )
    
    # If image is registered but no analysis output, something went wrong
    if image_registered and not analysis_output:
        return Command(
            goto=END,
            update={
                "next_node": END,
                "messages": state["messages"] + [AIMessage(content="There was an issue processing your image. Please try again.", name="supervisor")]
            }
        )
    
    # Check if there's an image in the current messages to process
    has_image = False
    if messages:
        latest_message = messages[-1]
        if hasattr(latest_message, 'content') and isinstance(latest_message.content, list):
            for content_item in latest_message.content:
                if isinstance(content_item, dict) and content_item.get('type') == 'image':
                    has_image = True
                    break
    
    # If no image is found, ask for one
    if not has_image:
        return Command(
            goto=END,
            update={
                "next_node": END,
                "messages": state["messages"] + [AIMessage(content="Please provide an image for me to analyze.", name="supervisor")]
            }
        )
    
    # If image is present and not yet registered, route to image_analyser
    return Command(
        goto="image_analyser",
        update={
            "next_node": "image_analyser",
            "messages": state["messages"] + [AIMessage(content="I can see you've provided an image. Let me analyze it for you...", name="supervisor")]
        }
    )

