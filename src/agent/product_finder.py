from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from src.tools.db_tool import search_products, get_product_by_id
from src.state import State, FoundProducts
from langchain_core.messages import AIMessage
from langgraph.types import Command
from langgraph.graph import END

llm = init_chat_model(model="gpt-4o")
product_search_agent = create_react_agent(
    model=llm,
    tools=[search_products, get_product_by_id],
    name="product_finder",
    response_format=FoundProducts,
    prompt="""You are a product search expert for a shopping assistant.

Your job:
1. Use search_products to find relevant products based on `analysis_output` and `user_preferences` from our local database ONLY
2. Use get_product_by_id to get detailed product information from our local database ONLY
3. Help users find products that match their needs from our available inventory
4. Consider factors like category, brand, price range, color, size, style, and user preferences

IMPORTANT: 
- You can ONLY search products from our local database using the provided tools
- Do NOT search for or suggest products from external sources or the internet
- Only return products that are found in our database through the search_products tool
- Prioritize products that match the user's stated preferences (budget, brands, features, etc.)
- Consider both the image analysis results AND the user preferences when searching

When searching, consider:
- Product category from image analysis
- User's budget range
- Preferred brands
- Size requirements
- Color preferences
- Specific features requested
- Use case mentioned by the user

Provide helpful product recommendations with clear explanations of why these products match the user's requirements.

IMPORTANT: Your response must be structured as FoundProducts with:
- products: List of Product objects found in our database that best match user preferences
- reason: Explanation of why these products were selected from our available inventory, referencing both image analysis and user preferences"""
)

def product_finder_node(state: State) -> Command:
    response = product_search_agent.invoke(state)
    
    result = response["structured_response"]
    
    # Check if no products were found
    if not result.products or len(result.products) == 0:
        return Command(
            goto=END,
            update={
                "messages": state["messages"] + [
                    AIMessage(content="I couldn't find any products matching your criteria in our database. Please try with a different image or adjust your preferences.", name="product_finder")
                ]
            }
        )
    
    updated_messages = state["messages"] + [
        AIMessage(content=result.reason, name="product_searcher")
    ]
    
    return Command(
        goto="supervisor",
        update= {
            "messages": updated_messages,
            "found_products": result.products
        }
    )