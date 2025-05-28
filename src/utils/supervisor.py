from src.state import State

def has_image_in_message(message):
    """Check if a message contains an image."""
    if hasattr(message, 'content') and isinstance(message.content, list):
        for content_item in message.content:
            if isinstance(content_item, dict) and content_item.get('type') == 'image':
                return True
    return False

def is_human_message(message):
    """Check if a message is from a human."""
    return hasattr(message, 'type') and message.type == 'human'

def is_enough_info_for_product_search(state: State) -> bool:
    """Check if we have enough information to search for products."""
    user_preferences = state.get("user_preferences")

    if not user_preferences:
        return False

    has_budget = user_preferences.budget_range is not None
    has_other_pref = any([
        user_preferences.preferred_brands,
        user_preferences.size_requirements,
        user_preferences.specific_features,
        user_preferences.use_case
    ])
    
    return has_budget and has_other_pref

def no_image_no_data(state: State) -> bool:
    return state.get("image_registered") in [None, False] and not is_enough_info_for_product_search(state) and state.get("found_products") in [None, []]