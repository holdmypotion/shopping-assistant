from langchain.chat_models import init_chat_model
from langgraph.types import Command
from src.state import State, ProductSearchDetails
from langchain_core.messages import AIMessage, SystemMessage
from pydantic import BaseModel, Field
from typing import Optional
from src.core.config import settings

class InfoGathererResponse(BaseModel):
    """Response format for info gatherer that can handle both greetings and preference extraction."""
    response_message: str = Field(description="The conversational response to the user")
    extracted_details: Optional[ProductSearchDetails] = Field(default=None, description="Extracted product search details if any, null if this is just a greeting or no details mentioned")


PROMPT = """
You are a helpful shopping assistant. Analyze the user's message and respond appropriately.

Context available to you:
- Current product search details: {product_search_details}

If the user is greeting you (like "hi", "hello", etc.):
- Respond with a friendly greeting and ask what they're looking for
- Set extracted_details to null since no shopping info was provided

If the user provides product information:
- Acknowledge what you understood
- Extract any product details mentioned into the extracted_details field
- Only extract information that is clearly mentioned - do not make up or assume anything
- Consider the existing product details to avoid redundant extraction
- Do NOT ask follow-up questions - simply acknowledge the information received

For product details extraction guidelines:
- category: type of product they're looking for
- brand: any brand names mentioned
- price: price information like "$100-200", "under $500" 
- color: color preferences mentioned
- size: size information if mentioned
- material: material preferences
- style: style preferences
- gender: gender if specified

IMPORTANT: 
- Be conversational and helpful in your response_message
- Only populate extracted_details when the user actually provides product information
- NEVER make up fake data in extracted_details
- If no details are mentioned, set extracted_details to null
- If the user mentions details that are already captured, acknowledge them but don't duplicate in extracted_details
- Do NOT ask questions - another agent will handle that
"""

llm = init_chat_model(model=settings.OPENAI_MODEL, temperature=0.1, disable_streaming=True)

def info_gatherer_node(state: State) -> Command:
    """Extract product details from user's response and update state."""
    prompt_content = PROMPT.format(product_search_details=state.get("product_search_details"))
    messages = [SystemMessage(content=prompt_content)] + state["messages"]
    
    response = llm.with_structured_output(InfoGathererResponse).invoke(messages)
    
    ai_response = response.response_message
    
    current_details = state.get("product_search_details", ProductSearchDetails())

    if response.extracted_details:
        extracted = response.extracted_details
        updated_details = ProductSearchDetails(
            category=extracted.category or current_details.category,
            brand=extracted.brand or current_details.brand,
            price=extracted.price or current_details.price,
            color=extracted.color or current_details.color,
            size=extracted.size or current_details.size,
            material=extracted.material or current_details.material,
            style=extracted.style or current_details.style,
            gender=extracted.gender or current_details.gender
        )
        updated_state = {
            "product_search_details": updated_details,
            "current_question": None,
            "messages": state["messages"] + [AIMessage(content=ai_response, name="info_gatherer")],
            "next_node": "product_search",
        }
        goto = "supervisor"
    else:
        updated_details = current_details
        updated_state = {
            "product_search_details": updated_details,
            "current_question": None,
            "next_node": "info_prober",
            "messages": state["messages"] + [AIMessage(content=ai_response, name="info_gatherer")],
        }
        goto = "supervisor"


    return Command(goto=goto, update=updated_state)
