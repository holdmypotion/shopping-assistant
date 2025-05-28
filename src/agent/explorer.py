from src.state import State
from langgraph.types import Command
from langgraph.graph import END
from langchain.prompts import PromptTemplate
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage
from src.core.config import settings


prompt = PromptTemplate(
    template="""
    You are an expert product explorer and shopping assistant. You have access to a list of products that have been found for the user based on their search criteria.

    Your task is to:
    1. Analyze the found products and understand what the user is looking for
    2. Answer any questions the user might have about these products
    3. Provide helpful comparisons, recommendations, and insights
    4. Help the user make informed decisions about their potential purchases

    The products you have access to are stored in the 'found_products' field of the current state.

    When responding:
    - Be helpful and informative
    - Provide specific details about the products when asked
    - Make comparisons between products when relevant
    - Suggest the best options based on the user's apparent needs and preferences
    - If the user asks about something not covered by the found products, let them know politely

    Always base your responses on the actual product data available to you. Be conversational and helpful while remaining accurate about product details.
""")

explorer_agent = create_react_agent(
    name="explorer",
    model=init_chat_model(model=settings.OPENAI_MODEL, temperature=0.1),
    tools=[],
    prompt=prompt,
)

def explore_products_node(state: State) -> Command:
    response = explorer_agent.invoke(state)
    message = response["messages"][-1].content

    updated_state = {
        "messages": state["messages"] + [AIMessage(content=message, name="explorer")],
    }

    return Command(goto=END, update=updated_state)