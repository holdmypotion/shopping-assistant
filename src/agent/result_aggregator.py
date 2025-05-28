from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from src.state import State
from langchain_core.messages import AIMessage
from langgraph.types import Command
from langgraph.graph import END

llm = init_chat_model(model="gpt-4o")

result_aggregator_agent = create_react_agent(
    model=llm,
    tools=[],
    name="result_aggregator",
    prompt="""You are a result presentation specialist for a shopping assistant.

Your job:
1. Present ONLY the found products that have been provided to you in a clear, organized, and helpful manner
2. Highlight key features and benefits of each provided product
3. Provide price comparisons and recommendations based on the provided products
4. Make the presentation engaging and easy to understand
5. Include relevant details like brand, category, price, and key attributes from the provided product data

IMPORTANT: 
- You must ONLY present the products that have been found and provided to you
- Do NOT search for or suggest additional products from the internet
- Do NOT make up product information that wasn't provided
- Base your response entirely on the product data given to you

Format your response in a user-friendly way that helps them make informed decisions.
Be enthusiastic and helpful while remaining professional."""
)

def result_aggregator_node(state: State) -> Command:
    found_products = state.get("found_products", [])
    analysis_output = state.get("analysis_output")
    
    if not found_products:
        return Command(
            goto=END,
            update={
                "messages": state["messages"] + [
                    AIMessage(content="I couldn't find any products matching your criteria. Please try with a different image or search terms.", name="result_aggregator")
                ]
            }
        )
    
    # Create a context message for the agent
    context_message = f"""
    Based on the image analysis, I found {len(found_products)} products for you from our database.
    
    IMPORTANT: Present ONLY these {len(found_products)} products that were found. Do not suggest or search for additional products.
    
    Image Analysis Summary:
    - Product Category: {analysis_output.product_category if analysis_output else 'Unknown'}
    - Key Attributes: {', '.join([attr.attribute_name + ': ' + attr.value for attr in analysis_output.visible_attributes if analysis_output and analysis_output.visible_attributes and attr.value]) if analysis_output and analysis_output.visible_attributes else 'None identified'}
    
    Found Products (from our database):
    """
    
    for i, product in enumerate(found_products, 1):
        context_message += f"""
        {i}. {product.name or 'Unknown Product'}
           - Brand: {product.brand or 'Unknown'}
           - Category: {product.category or 'Unknown'}
           - Price: ${product.price or 'N/A'}
           - Description: {product.description or 'No description available'}
        """
    
    # Invoke the agent to format the response nicely
    response = result_aggregator_agent.invoke({
        "messages": state["messages"] + [AIMessage(content=context_message, name="system")]
    })
    
    return Command(
        goto=END,
        update={
            "messages": state["messages"] + [
                AIMessage(content=response["messages"][-1].content, name="result_aggregator")
            ]
        }
    )
