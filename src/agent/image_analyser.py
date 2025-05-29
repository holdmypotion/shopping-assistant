from pydantic import BaseModel, Field
from typing import Optional
from langchain.chat_models import init_chat_model
from langgraph.types import Command
from src.state import State, ProductSearchDetails
from langchain_core.messages import AIMessage, SystemMessage
from src.core.config import settings
from langgraph.graph import END

PROMPT = """
    You are an expert product image analyzer with advanced vision capabilities. You can see and analyze images that are provided to you.

    IMPORTANT: You have vision capabilities and can analyze images. Do not claim that you cannot see images.

    Your task is to analyze the product image that has been provided and extract relevant attributes and their values.

    Given the product image, you need to:
    1. Identify the type/category of the product shown in the image
    2. Extract visible attributes and their values from the image
    3. Identify additional important attributes for this product category that would be valuable for product research, even if they're not visible in the image

    For example:
    - For clothing: 
      * Visible: color, style, pattern, general material type
      * Important for research: exact size, fabric composition, care instructions, price, brand reputation, country of origin
    - For electronics: 
      * Visible: brand, model (if shown), color, general form factor
      * Important for research: technical specifications, warranty, price, user reviews, compatibility, energy efficiency
    - For furniture: 
      * Visible: material, color, general style, approximate dimensions
      * Important for research: exact dimensions, weight capacity, assembly requirements, price, durability ratings
    - For books: 
      * Visible: title, author, condition, cover design
      * Important for research: publication date, edition, ISBN, price, reviews, availability

    Analyze the image carefully and provide structured output with:
    - Product category
    - Visible attributes extracted from the image with confidence levels
    - Additional relevant attributes that should be researched for this product type (even if not visible)
    - Overall confidence in the visual analysis
    - A brief message describing what you found

    Be thorough in identifying both what you can see and what additional information would be valuable for comprehensive product research.
    
    Return your analysis in the following structured format using the ProductSearchDetails schema.
"""

class ImageAnalyserOutput(BaseModel):
    """Represents the output of the image analyser."""
    product_search_details: ProductSearchDetails = Field(description="The product search details")
    overall_confidence: Optional[float] = Field(default=None, description="Overall confidence in the analysis")
    message: Optional[str] = Field(default=None, description="Describe the product in 1 or 2 sentences")

llm = init_chat_model(
    model=settings.OPENAI_MODEL,
    disable_streaming=True
).with_structured_output(ImageAnalyserOutput)

def image_analyser_node(state: State) -> Command:
    messages = [SystemMessage(content=PROMPT)] + state["messages"]
    
    response = llm.invoke(messages)

    message = response.message
    if not message:
        message = f"I've analyzed the {response.product_search_details.category} in your image and extracted the visible attributes."

    updated_state = {
        "product_search_details": response.product_search_details,
        "image_registered": True,
        "next_node": "product_search",
        "messages":[AIMessage(content=message, name="image_analyser")],
    }
    goto = "supervisor"

    if response.overall_confidence is None or response.overall_confidence < 0.5:
        message = "I'm not sure what the product is. Please provide more information or upload a different image."
        updated_state = {
            "next_node": "supervisor",
            "messages": state["messages"] + [AIMessage(content=message, name="image_analyser")],
        }
        goto = END

    return Command(goto=goto, update=updated_state)