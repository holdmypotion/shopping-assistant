from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from langgraph.graph import MessagesState

# class AttributeExtraction(BaseModel):
#     """Represents an extracted attribute with its value and confidence."""
#     attribute_name: Optional[str] = Field(default=None, description="Name of the attribute (e.g., 'color', 'brand', 'size')")
#     value: Optional[str] = Field(default=None, description="Extracted value for the attribute, None if not visible in image")
#     confidence: Optional[float] = Field(default=None, description="Confidence level between 0.0 and 1.0")
#     is_visible: Optional[bool] = Field(default=None, description="Whether this attribute is visible/extractable from the image")

# class ImageAnalysisOutput(BaseModel):
#     """Structured output for image analysis results."""
#     product_category: Optional[str] = Field(default=None, description="Identified product category/type")
#     visible_attributes: Optional[List[AttributeExtraction]] = Field(default=None, description="Attributes extracted from the image with values")
#     relevant_attributes: Optional[List[str]] = Field(default=None, description="Additional important attributes for this product category that should be researched but aren't visible in the image")
#     overall_confidence: Optional[float] = Field(default=None, description="Overall confidence in the analysis")
#     message: Optional[str] = Field(default=None, description="Describe the product in 1 or 2 sentences")

# class UserPreferences(BaseModel):
#     """Represents user preferences and requirements for the product they want to buy."""
#     budget_range: Optional[str] = Field(default=None, description="User's budget range (e.g., '$50-100', 'under $200')")
#     preferred_brands: Optional[List[str]] = Field(default=None, description="List of preferred brands")
#     size_requirements: Optional[str] = Field(default=None, description="Size requirements (e.g., 'Medium', 'Large', '32 inches')")
#     specific_features: Optional[List[str]] = Field(default=None, description="Specific features the user wants")
#     use_case: Optional[str] = Field(default=None, description="How the user plans to use the product")

class ProductSearchDetails(BaseModel):
    """Represents the details of a product search."""
    category: Optional[str] = Field(default=None, description="Product category/type")
    brand: Optional[str] = Field(default=None, description="Brand of the product")
    price: Optional[str] = Field(default=None, description="Price of the product")
    color: Optional[str] = Field(default=None, description="Color of the product")
    size: Optional[str] = Field(default=None, description="Size of the product")
    material: Optional[str] = Field(default=None, description="Material of the product")
    style: Optional[str] = Field(default=None, description="Style of the product")
    gender: Optional[str] = Field(default=None, description="Gender of the product")

class State(MessagesState):
    """State for the agent."""
    product_search_details: Optional[ProductSearchDetails] = None
    next_node: str = "supervisor"
    image_registered: Optional[bool] = Field(default=False, description="Whether an image has been registered and processed")
    remaining_steps: Optional[List[str]] = None
