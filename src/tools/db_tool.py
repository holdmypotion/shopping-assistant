from typing import Dict, List, Optional, Any
from src.data.db import MOCK_PRODUCTS
import re


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
    """Simple product search function for POC.
    
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
    
    # Convert price parameters to float if they're strings
    if price_min is not None:
        try:
            price_min = float(price_min)
        except (ValueError, TypeError):
            price_min = None
    
    if price_max is not None:
        try:
            price_max = float(price_max)
        except (ValueError, TypeError):
            price_max = None
    
    for product in MOCK_PRODUCTS:
        match = True
        
        # Check category - simple case-insensitive contains check
        if category:
            category_lower = category.lower()
            product_category = product.get("category", "").lower()
            product_name = product.get("name", "").lower()
            
            # Check if category matches product category, or if category is mentioned in product name
            if not (category_lower in product_category or 
                   category_lower in product_name or
                   product_category in category_lower):
                match = False
        
        # Check brand - simple case-insensitive contains check
        if brand and match:
            brand_lower = brand.lower()
            product_brand = product.get("brand", "").lower()
            if brand_lower not in product_brand and product_brand not in brand_lower:
                match = False
        
        # Check price range
        if (price_min or price_max) and match:
            try:
                product_price = float(product["price"])
                if price_min and product_price < price_min:
                    match = False
                if price_max and product_price > price_max:
                    match = False
            except (ValueError, TypeError):
                match = False
        
        # Check attributes
        if match:
            attrs = product.get("attributes", {})
            
            # Check color
            if color:
                color_lower = color.lower()
                product_color = attrs.get("color", "").lower()
                if color_lower not in product_color and product_color not in color_lower:
                    match = False
            
            # Check size
            if size and match:
                size_lower = size.lower()
                product_sizes = attrs.get("size")
                if isinstance(product_sizes, list):
                    size_match = any(size_lower in str(s).lower() for s in product_sizes)
                    if not size_match:
                        match = False
                elif product_sizes:
                    if size_lower not in str(product_sizes).lower():
                        match = False
                else:
                    match = False
            
            # Check style
            if style and match:
                style_lower = style.lower()
                product_style = attrs.get("style", "").lower()
                if style_lower not in product_style and product_style not in style_lower:
                    match = False
        
        # Add to results if all criteria match
        if match:
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


def get_all_categories() -> List[str]:
    """Get all unique product categories in the database.
    
    Returns:
        List of unique categories
    """
    categories = set()
    for product in MOCK_PRODUCTS:
        categories.add(product.get("category", ""))
    return sorted(list(categories))


def get_all_brands() -> List[str]:
    """Get all unique brands in the database.
    
    Returns:
        List of unique brands
    """
    brands = set()
    for product in MOCK_PRODUCTS:
        brands.add(product.get("brand", ""))
    return sorted(list(brands))


def get_products_by_category(category: str) -> List[Dict[str, Any]]:
    """Get all products in a specific category.
    
    Args:
        category: The category to search for
        
    Returns:
        List of products in that category
    """
    return search_products(category=category) 