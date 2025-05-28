from src.state import State
from langgraph.types import Command
from langgraph.graph import END
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, SystemMessage
from src.core.config import settings
from pydantic import BaseModel, Field

class Response(BaseModel):
    response: str = Field(description="The response to the user's query")

PROMPT = """
You are an expert product explorer and shopping assistant. You have access to a list of products that have been found for the user based on their search criteria.

Your task is to:
1. Analyze the found products and understand what the user is looking for
2. Answer any questions the user might have about these products
3. Provide helpful comparisons, recommendations, and insights
4. Help the user make informed decisions about their potential purchases

Context available to you:
- Found products: {found_products}
- User preferences: {user_preferences}

When responding:
- Be helpful and informative
- Provide specific details about the products when asked
- Make comparisons between products when relevant
- Suggest the best options based on the user's apparent needs and preferences
- Consider the user's budget, preferred brands, size requirements, specific features, and use case when making recommendations
- If the user asks about something not covered by the found products, let them know politely

Always base your responses on the actual product data available to you. Be conversational and helpful while remaining accurate about product details.

Note: Make sure your response resolve the user query otherwise say that you don't know the answer.
"""

llm = init_chat_model(model=settings.OPENAI_MODEL, temperature=0.2, disable_streaming=True)

def explore_products_node(state: State) -> Command:
    prompt_content = PROMPT.format(
        found_products=state["found_products"],
        user_preferences=state.get("user_preferences")
    )
    messages = [SystemMessage(content=prompt_content)] + [state["messages"][-1]]
    
    response = llm.with_structured_output(Response).invoke(messages)
    message = response.response
    
    updated_state = {
        "messages": state["messages"] + [AIMessage(content=message, name="explorer")],
    }

    return Command(goto=END, update=updated_state)