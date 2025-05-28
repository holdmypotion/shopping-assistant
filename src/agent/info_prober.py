from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langgraph.types import Command
from langchain.prompts import PromptTemplate
from src.state import State, UserPreferences
from langchain_core.messages import AIMessage


prompt = PromptTemplate(
    template="""
    You are a helpful shopping assistant that asks users targeted questions to understand their preferences and requirements for the product they want to buy.

    Your role:
    1. Analyze the image analysis output to understand what product the user is interested in
    2. Ask relevant, specific questions to gather user preferences
    3. Focus on the most important attributes for the product category
    4. Avoid asking questions that have already been asked
    5. Determine when you have enough information to proceed with product search

    Based on the product category and analysis, ask about:
    - Budget range
    - Size requirements (if applicable)
    - Brand preferences
    - Color preferences
    - Specific features they want
    - How they plan to use the product
    - Any other category-specific requirements

    Guidelines:
    - Ask 1-2 focused questions at a time, not overwhelming lists
    - Be conversational and friendly
    - Prioritize the most important attributes for the product category
    - If the user provides partial information, ask follow-up questions
    - Mark is_complete as True when you have sufficient information for a good product search

    Return your response in the UserPreferences format, updating the existing preferences with new information.
    If you need to ask questions, set is_complete to False and include your questions in additional_requirements.
    If you have enough information, set is_complete to True.
    """,
)


info_prober_agent = create_react_agent(
    name="info_prober",
    model=init_chat_model(model="gpt-4o", temperature=0.3),
    tools=[],
    prompt=prompt,
    response_format=UserPreferences,
)

def info_prober_node(state: State) -> Command:
    # Get current context
    analysis_output = state.get("analysis_output")
    current_preferences = state.get("user_preferences", UserPreferences())
    
    # Prepare context for the agent
    product_category = analysis_output.product_category if analysis_output else "unknown"
    visible_attributes = analysis_output.visible_attributes if analysis_output else []
    questions_asked = current_preferences.questions_asked or []
    
    # Create a context-aware state for the agent
    context_state = {
        **state,
        "product_category": product_category,
        "visible_attributes": visible_attributes,
        "questions_asked": questions_asked,
        "current_preferences": current_preferences
    }
    
    response = info_prober_agent.invoke(context_state)
    result = response["structured_response"]
    
    # Merge with existing preferences
    if current_preferences:
        # Update existing preferences with new information
        updated_preferences = UserPreferences(
            budget_range=result.budget_range or current_preferences.budget_range,
            preferred_brands=result.preferred_brands or current_preferences.preferred_brands,
            size_requirements=result.size_requirements or current_preferences.size_requirements,
            color_preferences=result.color_preferences or current_preferences.color_preferences,
            specific_features=result.specific_features or current_preferences.specific_features,
            use_case=result.use_case or current_preferences.use_case,
            priority_attributes=result.priority_attributes or current_preferences.priority_attributes,
            additional_requirements=result.additional_requirements or current_preferences.additional_requirements,
            questions_asked=(current_preferences.questions_asked or []) + (result.questions_asked or []),
            is_complete=result.is_complete
        )
    else:
        updated_preferences = result
    
    # Create appropriate message based on completion status
    if result.is_complete:
        message = "Great! I have enough information about your preferences. Let me find some products for you."
    else:
        # Extract the question from additional_requirements or create a default
        question = result.additional_requirements or "Could you tell me more about your preferences for this product?"
        message = question
    
    updated_state = {
        "user_preferences": updated_preferences,
        "messages": state["messages"] + [AIMessage(content=message, name="info_prober")],
    }

    return Command(goto="supervisor", update=updated_state)
