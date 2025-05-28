from langchain.chat_models import init_chat_model
from langgraph.types import Command
from src.state import State, UserPreferences
from langchain_core.messages import AIMessage, SystemMessage
from typing import Optional
from pydantic import BaseModel, Field
from src.core.config import settings

class QuestionOutput(BaseModel):
    """Output format for info_prober to generate questions."""
    question: Optional[str] = Field(default=None, description="The specific question to ask the user")
    is_complete: Optional[bool] = Field(default=False, description="Whether enough information has been collected")
    reasoning: Optional[str] = Field(default=None, description="Why this question is being asked")


PROMPT = """
You are a helpful shopping assistant that determines what questions to ask users to understand their preferences for the product they want to buy.

Your role:
1. Analyze the image analysis output to understand what product the user is interested in
2. Review existing user preferences to see what information is already collected
3. Check how many questions have already been asked (in questions_asked_count field)
4. Determine the next most important question to ask
5. Focus on gathering the key preference fields: budget_range, preferred_brands, size_requirements, specific_features, and use_case
6. Avoid asking questions that have already been answered

Context available to you:
- Image analysis output: {analysis_output}
- Current user preferences: {user_preferences}
- Questions asked so far: {questions_asked_count}

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
- Use the product category from analysis_output to make questions more specific and relevant

Return your response in the QuestionOutput format.
Only mark is_complete as True if you have budget_range AND at least 2 other preference fields filled.
"""

llm = init_chat_model(model=settings.OPENAI_MODEL, temperature=0.3, disable_streaming=True)

def info_prober_node(state: State) -> Command:
    questions_asked_count = state.get("questions_asked_count", 0)
    
    # Check if we've already asked 3 questions
    if questions_asked_count > 3:
        return Command(goto="supervisor")
    
    prompt_content = PROMPT.format(
        analysis_output=state.get("analysis_output"),
        user_preferences=state.get("user_preferences"),
        questions_asked_count=questions_asked_count
    )
    messages = [SystemMessage(content=prompt_content)]
    
    response = llm.with_structured_output(QuestionOutput).invoke(messages)
    
    if response.question:
        updated_state = {
            "current_question": response.question,
            "questions_asked_count": questions_asked_count + 1,
        }
        return Command(goto="supervisor", update=updated_state)
    else:
        return Command(goto="supervisor")
