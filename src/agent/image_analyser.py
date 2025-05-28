from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langgraph.types import Command
from langchain.prompts import PromptTemplate
from src.state import State, ImageAnalysisOutput
from langchain_core.messages import AIMessage
from src.core.config import settings


prompt = PromptTemplate(
    template="""
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
    
    Return your analysis in the following structured format using the ImageAnalysisOutput schema.
    """,
)


image_analyser_agent = create_react_agent(
    name="image_analyser",
    model=init_chat_model(model=settings.OPENAI_MODEL, temperature=0.1),
    tools=[],
    prompt=prompt,
    response_format=ImageAnalysisOutput,
)

def image_analyser_node(state: State) -> Command:
    response = image_analyser_agent.invoke(state)
    result = response["structured_response"]

    message = result.message
    if not message:
        category = result.product_category
        message = f"I've analyzed the {category} in your image and extracted the visible attributes."

    updated_state = {
        "analysis_output": result,
        "image_registered": True,
        "messages": state["messages"] + [AIMessage(content=message, name="image_analyser")],
    }

    return Command(goto="supervisor", update=updated_state)