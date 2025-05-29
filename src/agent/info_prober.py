from langchain.chat_models import init_chat_model
from langgraph.types import Command
from src.state import State, ProductSearchDetails
from langchain_core.messages import AIMessage, SystemMessage
from typing import Optional
from pydantic import BaseModel, Field
from src.core.config import settings
from langgraph.graph import END

class QuestionOutput(BaseModel):
    """Output format for info_prober to generate questions."""
    question: Optional[str] = Field(default=None, description="The specific question to ask the user")
    is_complete: Optional[bool] = Field(default=False, description="Whether enough information has been collected")
    reasoning: Optional[str] = Field(default=None, description="Why this question is being asked")


PROMPT = """
You are a helpful shopping assistant that determines what questions to ask users to understand their preferences for the product they want to buy.

Your role:
1. Analyze the image analysis output to understand what product the user is interested in
2. Review existing product search details to see what information is already collected
3. Determine the next most important question to ask
4. Focus on gathering the key fields: category, brand, price, color, size, material, style, and gender
5. Avoid asking questions that have already been answered

Context available to you:
- Product search details: {product_search_details}

IMPORTANT: Be conversational and natural in your responses. If the user is just saying hello or starting a conversation, welcome them warmly first before asking questions.

For initial greetings:
- "Hi there! I'm here to help you find the perfect product. What kind of item are you looking for today?"
- "Hello! I'd love to help you with your shopping. What brings you here today?"
- "Welcome! I'm your personal shopping assistant. How can I help you find what you're looking for?"

For follow-up questions, focus on gathering SPECIFIC, ACTIONABLE information that helps with product search, prioritizing the ProductSearchDetails fields.

Priority order for gathering details:
1. price - Essential for filtering products by price
2. category - Helps understand what type of product to search for
3. size - Critical for products with size variations
4. brand - Brand preferences for filtering
5. color - Color preferences
6. material - Material preferences
7. style - Style preferences
8. gender - Gender if applicable

EXAMPLES OF GOOD FOLLOW-UP QUESTIONS BY TYPE:

Price:
- "What's your budget range for these headphones - under $100, $100-200, or over $200?"
- "How much would you like to spend on this item?"

Category:
- "What specific type of headphones interests you - over-ear, in-ear, or wireless?"
- "Are you looking for casual shoes or formal shoes?"

Size:
- "What size do you typically wear?"
- "Are you looking for a specific screen size or dimensions?"

Brand:
- "Do you have any preferred brands like Sony, Bose, or Apple, or are you open to any brand?"
- "Are there any brands you particularly like or want to avoid?"

Guidelines:
- Generate ONE response at a time
- Check existing product_search_details to avoid asking about information already collected
- Make questions that directly map to ProductSearchDetails fields
- Be conversational and natural
- Focus on gathering information that helps filter and search products
- Prioritize price and category first as they're most impactful for search
- Use the product category from product_search_details to make questions more specific and relevant

Return your response in the QuestionOutput format.
Only mark is_complete as True if you have price AND at least 2 other fields filled.
"""

llm = init_chat_model(model=settings.OPENAI_MODEL, temperature=0.3, disable_streaming=True)

def info_prober_node(state: State) -> Command:
    prompt_content = PROMPT.format(
        product_search_details=state.get("product_search_details")
    )
    messages = [SystemMessage(content=prompt_content)]
    
    response = llm.with_structured_output(QuestionOutput).invoke(messages)
    
    if response.question:
        updated_state = {
            "current_question": response.question,
            "messages": state["messages"] + [AIMessage(content=response.question, name="info_prober")],
            "next_node": "info_gatherer",
        }
        return Command(goto=END, update=updated_state)
    else:
        return Command(goto="supervisor", update={ "next_node": "supervisor" })
