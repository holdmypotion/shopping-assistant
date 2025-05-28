from langchain.chat_models import init_chat_model
from langgraph.types import Command
from src.state import State, UserPreferences
from langchain_core.messages import AIMessage, SystemMessage
from pydantic import BaseModel, Field
from typing import Optional
from src.core.config import settings

class InfoGathererResponse(BaseModel):
    """Response format for info gatherer that can handle both greetings and preference extraction."""
    response_message: str = Field(description="The conversational response to the user")
    extracted_preferences: Optional[UserPreferences] = Field(default=None, description="Extracted preferences if any, null if this is just a greeting or no preferences mentioned")


PROMPT = """
You are a helpful shopping assistant. Analyze the user's message and respond appropriately.

Context available to you:
- Current user preferences: {user_preferences}

If the user is greeting you (like "hi", "hello", etc.):
- Respond with a friendly greeting and ask what they're looking for
- Set extracted_preferences to null since no shopping info was provided

If the user provides shopping preferences or product information:
- Acknowledge what you understood
- Extract any preferences mentioned into the extracted_preferences field
- Only extract information that is clearly mentioned - do not make up or assume anything
- Consider the existing user preferences to avoid redundant extraction
- Do NOT ask follow-up questions - simply acknowledge the information received

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
- If the user mentions preferences that are already captured, acknowledge them but don't duplicate in extracted_preferences
- Do NOT ask questions - another agent will handle that
"""

llm = init_chat_model(model=settings.OPENAI_MODEL, temperature=0.1, disable_streaming=True)

def info_gatherer_node(state: State) -> Command:
    """Extract preferences from user's response and update state."""
    prompt_content = PROMPT.format(user_preferences=state.get("user_preferences"))
    messages = [SystemMessage(content=prompt_content)] + state["messages"]
    
    response = llm.with_structured_output(InfoGathererResponse).invoke(messages)
    
    ai_response = response.response_message
    
    current_prefs = state.get("user_preferences", UserPreferences())

    if response.extracted_preferences:
        # Merge extracted preferences with existing ones
        extracted = response.extracted_preferences
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
