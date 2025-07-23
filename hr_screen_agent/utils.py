import operator
from datetime import datetime, timezone
from textwrap import dedent


def current_time_context() -> str:
    return dedent(
        f"""
<current_time_context>
- Current UTC time: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}
- Use this time context when processing date ranges
- Apply this timestamp as reference when needed
</current_time_context>
        """
    ).strip()


def remove_duplicates(items: list) -> list:
    """
    Remove duplicates from a list while preserving order.

    Args:
        items: List that may contain duplicates

    Returns:
        List with duplicates removed, preserving order of first occurrence
    """
    return list(dict.fromkeys(items))


def create_override(value: list) -> dict:
    """
    Create an override marker for a value to be used with override_reducer.

    This function wraps a value in a special dictionary structure that signals
    to the override_reducer that this value should completely replace the current
    value instead of being combined with it.

    Args:
        value: The value to mark for override behavior

    Returns:
        Dict with override metadata containing the value

    Example:
        >>> current = [1, 2, 3]
        >>> new_override = create_override([4, 5])
        >>> result = override_reducer(current, new_override)
        >>> result
        [4, 5]  # Completely replaced, not combined
    """
    return {
        "type": "override",
        "value": value,
    }


def override_reducer(current_value, new_value):
    """
    Custom reducer that supports override functionality and removes duplicates from lists.

    Args:
        current_value: Existing value
        new_value: New value to add or override with

    Returns:
        Combined value with duplicates removed if applicable
    """
    if isinstance(new_value, dict) and new_value.get("type") == "override":
        override_value = new_value.get("value", new_value)
        # Remove duplicates if override value is a list
        if isinstance(override_value, list):
            return remove_duplicates(override_value)
        return override_value
    else:
        result = operator.add(current_value, new_value)
        # Remove duplicates if result is a list
        if isinstance(result, list):
            return remove_duplicates(result)
        return result
