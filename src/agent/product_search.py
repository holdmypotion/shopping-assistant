from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field
from typing import List
from src.core.config import settings
from src.tools.db_tool import (
    search_products,
    get_all_categories,
    get_all_brands,
    get_product_by_id,
    get_products_by_category
)
from src.state import State, ProductSearchDetails
from langgraph.types import Command
from langchain_core.messages import AIMessage
from langgraph.graph import END

PROMPT = """

You are a product search agent. You are given a product search details and you need to search for products that match the search details.

Only call search_products tool if you have all the details in the product search details.

You have the following tools at your disposal:
- search_products: to search for products in the database
- get_all_categories: to get all the categories in the database
- get_all_brands: to get all the brands in the database
- get_product_by_id: to get a product by its id
- get_products_by_category: to get all the products in a category
"""

class ProductSearchOutput(BaseModel):
    """Output format for product search agent."""
    products: List[ProductSearchDetails] = Field(description="The products that match the search details")
    message: str = Field(description="The message to the user. Tell them details about the products found.")


def product_search_node(state: State) -> Command:
    product_search_agent = create_react_agent(
        model=settings.OPENAI_MODEL,
        tools=[
            search_products,
            get_all_categories,
            get_all_brands,
            get_product_by_id,
            get_products_by_category
        ],
        prompt=PROMPT,
    )

    response = product_search_agent.invoke({
        "messages": state["messages"][-1],
        "product_search_details": state["product_search_details"],
    })

    return Command(
        goto=END,
        update={
            "next_node": "supervisor",
            "product_found": True,
            "messages": state["messages"] + [AIMessage(content=response['messages'][-1].content, name="product_search")]
        }
    )