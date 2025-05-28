from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from langgraph.graph import MessagesState

class AttributeExtraction(BaseModel):
    """Represents an extracted attribute with its value and confidence."""
    attribute_name: Optional[str] = Field(default=None, description="Name of the attribute (e.g., 'color', 'brand', 'size')")
    value: Optional[str] = Field(default=None, description="Extracted value for the attribute, None if not visible in image")
    confidence: Optional[float] = Field(default=None, description="Confidence level between 0.0 and 1.0")
    is_visible: Optional[bool] = Field(default=None, description="Whether this attribute is visible/extractable from the image")

class ImageAnalysisOutput(BaseModel):
    """Structured output for image analysis results."""
    product_category: Optional[str] = Field(default=None, description="Identified product category/type")
    visible_attributes: Optional[List[AttributeExtraction]] = Field(default=None, description="Attributes extracted from the image with values")
    relevant_attributes: Optional[List[str]] = Field(default=None, description="Additional important attributes for this product category that should be researched but aren't visible in the image")
    overall_confidence: Optional[float] = Field(default=None, description="Overall confidence in the analysis")
    message: Optional[str] = Field(default=None, description="Describe the product in 1 or 2 sentences")

class UserPreferences(BaseModel):
    """Represents user preferences and requirements for the product they want to buy."""
    budget_range: Optional[str] = Field(default=None, description="User's budget range (e.g., '$50-100', 'under $200')")
    preferred_brands: Optional[List[str]] = Field(default=None, description="List of preferred brands")
    size_requirements: Optional[str] = Field(default=None, description="Size requirements (e.g., 'Medium', 'Large', '32 inches')")
    specific_features: Optional[List[str]] = Field(default=None, description="Specific features the user wants")
    use_case: Optional[str] = Field(default=None, description="How the user plans to use the product")

class Product(BaseModel):
    """Represents a product from the database."""
    id: Optional[str] = Field(default=None, description="Product ID")
    name: Optional[str] = Field(default=None, description="Product name")
    category: Optional[str] = Field(default=None, description="Product category")
    brand: Optional[str] = Field(default=None, description="Product brand")
    price: Optional[float] = Field(default=None, description="Product price")
    attributes: Optional[Dict[str, str]] = Field(default=None, description="Product attributes")
    description: Optional[str] = Field(default=None, description="Product description")

class FoundProducts(BaseModel):
    """Structured output for found products."""
    products: Optional[List[Product]] = Field(default=None, description="List of products found")
    reason: Optional[str] = Field(default=None, description="Explanation of why these products were selected")


class State(MessagesState):
    """State for the agent."""
    analysis_output: Optional[ImageAnalysisOutput] = None
    user_preferences: Optional[UserPreferences] = None
    found_products: Optional[List[Product]] = None
    remaining_steps: Optional[List[str]] = None
    next_node: Optional[str] = None
    image_registered: Optional[bool] = Field(default=False, description="Whether an image has been registered and processed")
    current_question: Optional[str] = Field(default=None, description="Current question to ask the user")
    questions_asked_count: Optional[int] = Field(default=0, description="Number of questions asked to the user")
