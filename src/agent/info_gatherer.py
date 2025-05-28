from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langgraph.types import Command
from langchain.prompts import PromptTemplate
from src.state import State, UserPreferences
from langchain_core.messages import AIMessage
from pydantic import BaseModel, Field
from typing import Optional
from src.core.config import settings

class InfoGathererResponse(BaseModel):
    """Response format for info gatherer that can handle both greetings and preference extraction."""
    response_message: str = Field(description="The conversational response to the user")
    extracted_preferences: Optional[UserPreferences] = Field(default=None, description="Extracted preferences if any, null if this is just a greeting or no preferences mentioned")


prompt = PromptTemplate(
    template="""
    You are a helpful shopping assistant. Analyze the user's message and respond appropriately.
    
    If the user is greeting you (like "hi", "hello", etc.):
    - Respond with a friendly greeting and ask what they're looking for
    - Set extracted_preferences to null since no shopping info was provided
    
    If the user provides shopping preferences or product information:
    - Acknowledge what you understood
    - Extract any preferences mentioned into the extracted_preferences field
    - Only extract information that is clearly mentioned - do not make up or assume anything
    
    For preference extraction guidelines:
    - budget_range: formats like "$100-200", "under $500", "around $1000", etc.
    - preferred_brands: any brand names mentioned
    - specific_features: specific features or capabilities mentioned  
    - use_case: how they plan to use the product
    - size_requirements: size information if mentioned
    
    IMPORTANT: 
    - Be conversational and helpful in your response_message
    - Only populate extracted_preferences when the user actually provides shopping information
    - NEVER make up fake data in extracted_preferences
    - If no preferences are mentioned, set extracted_preferences to null
    """,
)


info_gatherer_agent = create_react_agent(
    name="info_gatherer",
    model=init_chat_model(model=settings.OPENAI_MODEL, temperature=0.1),
    tools=[],
    prompt=prompt,
    response_format=InfoGathererResponse,
)


def info_gatherer_node(state: State) -> Command:
    """Extract preferences from user's response and update state."""
    response = info_gatherer_agent.invoke(state)
    structured_response = response["structured_response"]
    
    ai_response = structured_response.response_message
    
    current_prefs = state.get("user_preferences", UserPreferences())

    if structured_response.extracted_preferences:
        # Merge extracted preferences with existing ones
        extracted = structured_response.extracted_preferences
        updated_prefs = UserPreferences(
            budget_range=extracted.budget_range or current_prefs.budget_range,
            preferred_brands=(extracted.preferred_brands or []) + (current_prefs.preferred_brands or []),
            size_requirements=extracted.size_requirements or current_prefs.size_requirements,
            specific_features=(extracted.specific_features or []) + (current_prefs.specific_features or []),
            use_case=extracted.use_case or current_prefs.use_case,
        )
    else:
        # No preferences extracted, keep existing ones
        updated_prefs = current_prefs
    
    updated_state = {
        "user_preferences": updated_prefs,
        "current_question": None,
        "messages": state["messages"] + [AIMessage(content=ai_response, name="info_gatherer")],
    }

    return Command(goto="supervisor", update=updated_state)
