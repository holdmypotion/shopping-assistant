from typing import Dict, List, Optional, Any
from src.data.db import MOCK_PRODUCTS

def search_products(
    category: Optional[str] = None,
    brand: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    color: Optional[str] = None,
    size: Optional[str] = None,
    style: Optional[str] = None,
    **kwargs
) -> List[Dict[str, Any]]:
    """Search products from the mock database based on criteria.
    
    Args:
        category: Product category (shoes, clothing, electronics, etc.)
        brand: Brand name
        price_min: Minimum price
        price_max: Maximum price
        color: Product color
        size: Product size
        style: Product style (casual, athletic, formal, etc.)
        **kwargs: Additional search criteria
        
    Returns:
        List of matching products
    """
    results = []
    
    for product in MOCK_PRODUCTS:
        # Check category
        if category and product["category"].lower() != category.lower():
            continue
            
        # Check brand
        if brand and product["brand"].lower() != brand.lower():
            continue
            
        # Check price range
        if price_min and product["price"] < price_min:
            continue
        if price_max and product["price"] > price_max:
            continue
            
        # Check attributes
        attrs = product.get("attributes", {})
        
        if color and attrs.get("color", "").lower() != color.lower():
            continue
            
        if size and isinstance(attrs.get("size"), list):
            if size not in attrs["size"]:
                continue
        elif size and attrs.get("size", "").lower() != size.lower():
            continue
            
        if style and attrs.get("style", "").lower() != style.lower():
            continue
            
        results.append(product)
    
    return results


def get_product_by_id(product_id: str) -> Optional[Dict[str, Any]]:
    """Get specific product details by ID.
    
    Args:
        product_id: The product ID to search for
        
    Returns:
        Product details if found, None otherwise
    """
    for product in MOCK_PRODUCTS:
        if product["id"] == product_id:
            return product
    return None 