from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langgraph.types import Command
from langchain.prompts import PromptTemplate
from src.state import State, UserPreferences
from langchain_core.messages import AIMessage
from typing import Optional
from pydantic import BaseModel, Field


class QuestionOutput(BaseModel):
    """Output format for info_prober to generate questions."""
    question: Optional[str] = Field(default=None, description="The specific question to ask the user")
    is_complete: Optional[bool] = Field(default=False, description="Whether enough information has been collected")
    reasoning: Optional[str] = Field(default=None, description="Why this question is being asked")


prompt = PromptTemplate(
    template="""
    You are a helpful shopping assistant that determines what questions to ask users to understand their preferences for the product they want to buy.

    Your role:
    1. Analyze the image analysis output to understand what product the user is interested in
    2. Review existing user preferences to see what information is already collected
    3. Check how many questions have already been asked (in questions_asked_count field)
    4. Determine the next most important question to ask
    5. Focus on gathering the key preference fields: budget_range, preferred_brands, size_requirements, specific_features, and use_case
    6. Avoid asking questions that have already been answered

    IMPORTANT: Generate SPECIFIC, ACTIONABLE questions that help with product search. Focus on the UserPreferences fields.

    Priority order for gathering preferences:
    1. budget_range - Essential for filtering products by price
    2. use_case - Helps understand the context and requirements
    3. size_requirements - Critical for products with size variations
    4. specific_features - Important capabilities or characteristics
    5. preferred_brands - Brand preferences for filtering

    EXAMPLES OF GOOD QUESTIONS BY PREFERENCE TYPE:

    Budget Range:
    - "What's your budget range for these headphones - under $100, $100-200, or over $200?"
    - "How much are you looking to spend on this item?"

    Use Case:
    - "What will you primarily use these headphones for - music listening, gaming, work calls, or exercise?"
    - "Are you looking for everyday casual wear or something for special occasions?"

    Size Requirements:
    - "What size do you typically wear?"
    - "Are you looking for a specific screen size or dimensions?"

    Specific Features:
    - "Which features are most important to you - noise cancellation, wireless connectivity, or long battery life?"
    - "Do you need any specific capabilities like water resistance or fast charging?"

    Preferred Brands:
    - "Do you have any preferred brands like Sony, Bose, or Apple, or are you open to any brand?"
    - "Are there any brands you particularly like or want to avoid?"

    Guidelines:
    - Generate ONE specific question at a time
    - Check existing user_preferences to avoid asking about information already collected
    - Make questions that directly map to UserPreferences fields
    - Be conversational but specific
    - Focus on gathering information that helps filter and search products
    - Prioritize budget_range and use_case first as they're most impactful for search

    Current user preferences to consider:
    {preferences}

    Return your response in the QuestionOutput format.
    Only mark is_complete as True if you have budget_range AND at least 2 other preference fields filled.
    """,
)


info_prober_agent = create_react_agent(
    name="info_prober",
    model=init_chat_model(model="gpt-4o", temperature=0.3),
    tools=[],
    prompt=prompt.format(preferences=UserPreferences.model_json_schema()),
    response_format=QuestionOutput,
)

def info_prober_node(state: State) -> Command:
    response = info_prober_agent.invoke(state)
    result = response["structured_response"]
    
    if result.question:
        updated_state = {
            "current_question": result.question,
            "questions_asked_count": state.get("questions_asked_count", 0) + 1,
        }
        return Command(goto="supervisor", update=updated_state)
    else:
        return Command(goto="supervisor")
