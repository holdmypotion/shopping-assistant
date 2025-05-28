from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langgraph.types import Command
from langchain.prompts import PromptTemplate
from src.state import State, UserPreferences
from langchain_core.messages import AIMessage, HumanMessage
from pydantic import BaseModel, Field
from typing import Optional, List


class PreferenceUpdate(BaseModel):
    """Structured update to user preferences based on human response."""
    budget_range: Optional[str] = Field(default=None, description="Budget range if mentioned")
    preferred_brands: Optional[List[str]] = Field(default=None, description="Brands mentioned")
    size_requirements: Optional[str] = Field(default=None, description="Size requirements if mentioned")
    specific_features: Optional[List[str]] = Field(default=None, description="Features mentioned")
    use_case: Optional[str] = Field(default=None, description="How they plan to use it")


prompt = PromptTemplate(
    template="""
    Extract user preferences from their response to a shopping question.
    
    Only extract information that is clearly mentioned. Leave fields as null if not mentioned.
    
    For budget_range, use formats like "$100-200", "under $500", "around $1000", etc.
    For brands, extract any brand names mentioned.
    For features, extract specific features or capabilities mentioned.
    For use_case, extract how they plan to use the product.
    For size_requirements, extract size information if mentioned.
    
    Return your analysis in the PreferenceUpdate format.
    """,
)


info_gatherer_agent = create_react_agent(
    name="info_gatherer",
    model=init_chat_model(model="gpt-4o", temperature=0.1),
    tools=[],
    prompt=prompt,
    response_format=PreferenceUpdate,
)


def info_gatherer_node(state: State) -> Command:
    """Extract preferences from user's response and update state."""
    messages = state.get("messages", [])
    human_response = messages[-1].content[0]

    response = info_gatherer_agent.invoke(human_response)
    parsed_update = response["structured_response"]
    
    current_prefs = state.get("user_preferences", UserPreferences())
    
    updated_prefs = UserPreferences(
        budget_range=parsed_update.budget_range or current_prefs.budget_range,
        preferred_brands=(parsed_update.preferred_brands or []) + (current_prefs.preferred_brands or []),
        size_requirements=parsed_update.size_requirements or current_prefs.size_requirements,
        specific_features=(parsed_update.specific_features or []) + (current_prefs.specific_features or []),
        use_case=parsed_update.use_case or current_prefs.use_case,
    )

    updated_state = {
        "user_preferences": updated_prefs,
        "current_question": None,
        "messages": state["messages"] + [AIMessage(content="Got it, thanks!", name="info_gatherer")],
    }

    return Command(goto="supervisor", update=updated_state)
