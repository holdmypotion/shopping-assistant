from src.tools.db_tool import search_products
from src.state import State
from langchain_core.messages import AIMessage
from langgraph.types import Command
from langgraph.graph import END
from typing import Dict, Any, List


def product_finder_node(state: State) -> Command:
    """Product finder node that searches products and formats the results."""
    analysis_output = state.get("analysis_output")
    user_preferences = state.get("user_preferences")
    
    # Build search criteria from analysis output and user preferences
    search_criteria = {}
    
    # Extract category from image analysis
    if analysis_output and analysis_output.product_category:
        search_criteria["category"] = analysis_output.product_category
    
    # Extract attributes from image analysis
    if analysis_output and analysis_output.visible_attributes:
        for attr in analysis_output.visible_attributes:
            if attr.attribute_name and attr.value and attr.is_visible:
                if attr.attribute_name.lower() in ["color", "brand", "size", "style"]:
                    search_criteria[attr.attribute_name.lower()] = attr.value
    
    # Extract preferences from user input
    if user_preferences:
        # Handle budget range
        if user_preferences.budget_range:
            budget = user_preferences.budget_range.lower()
            if "under" in budget or "below" in budget:
                # Extract number for max price
                import re
                numbers = re.findall(r'\d+', budget)
                if numbers:
                    search_criteria["price_max"] = float(numbers[0])
            elif "-" in budget:
                # Extract range
                import re
                numbers = re.findall(r'\d+', budget)
                if len(numbers) >= 2:
                    search_criteria["price_min"] = float(numbers[0])
                    search_criteria["price_max"] = float(numbers[1])
        
        # Handle size requirements
        if user_preferences.size_requirements:
            search_criteria["size"] = user_preferences.size_requirements
        
        # Handle preferred brands (use first one for simplicity)
        if user_preferences.preferred_brands and len(user_preferences.preferred_brands) > 0:
            search_criteria["brand"] = user_preferences.preferred_brands[0]
    
    # Search for products
    found_products = search_products(**search_criteria)
    
    # Check if no products were found
    if not found_products or len(found_products) == 0:
        return Command(
            goto=END,
            update={
                "messages": state["messages"] + [
                    AIMessage(content="I couldn't find any products matching your criteria in our database. Please try with a different image or adjust your preferences.", name="product_finder")
                ]
            }
        )
    
    # Format the results directly
    message_parts = [
        f"I found {len(found_products)} product{'s' if len(found_products) != 1 else ''} for you:\n"
    ]
    
    for i, product in enumerate(found_products, 1):
        try:
            # Safely extract product information
            name = product.get("name", "Unknown Product") if isinstance(product, dict) else str(product)
            brand = product.get("brand", "Unknown") if isinstance(product, dict) else "Unknown"
            category = product.get("category", "Unknown") if isinstance(product, dict) else "Unknown"
            price = product.get("price", "N/A") if isinstance(product, dict) else "N/A"
            description = product.get("description", "No description available") if isinstance(product, dict) else "No description available"
            
            product_info = f"{i}. **{name}**\n"
            product_info += f"   - Brand: {brand}\n"
            product_info += f"   - Category: {category}\n"
            product_info += f"   - Price: ${price}\n"
            product_info += f"   - Description: {description}\n"
            
            # Add attributes if available
            if isinstance(product, dict) and "attributes" in product:
                attributes = product["attributes"]
                if attributes:
                    product_info += "   - Attributes:\n"
                    for key, value in attributes.items():
                        if isinstance(value, list):
                            product_info += f"     • {key.title()}: {', '.join(map(str, value))}\n"
                        else:
                            product_info += f"     • {key.title()}: {value}\n"
            
            message_parts.append(product_info)
            
        except Exception as e:
            # If there's any error with a product, skip it but log the issue
            print(f"Error processing product {i}: {e}")
            continue
    
    final_message = "\n".join(message_parts)
    
    return Command(
        goto=END,
        update={
            "found_products": found_products,
            "messages": state["messages"] + [
                AIMessage(content=final_message, name="product_finder")
            ]
        }
    )