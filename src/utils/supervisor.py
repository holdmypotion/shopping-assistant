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
    analysis_output = state.get("analysis_output")
    user_preferences = state.get("user_preferences")
    
    # Need image analysis
    if not analysis_output:
        return False
    
    # Need some user preferences
    if not user_preferences:
        return False
    
    # Consider it enough if we have budget and at least one other preference
    has_budget = user_preferences.budget_range is not None
    has_other_pref = any([
        user_preferences.preferred_brands,
        user_preferences.size_requirements,
        user_preferences.specific_features,
        user_preferences.use_case
    ])
    
    return has_budget and has_other_pref