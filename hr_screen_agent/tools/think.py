from textwrap import dedent
from typing import Annotated

from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command


@tool(
    "think",
    description="Use the tool to think about something. It will not obtain new information or take any actions, but just append the thought to the log and return the result. Use it when complex reasoning or some cache memory or a scratchpad is needed.",
)
def think(
    thought: Annotated[str, "A thought to think about and log."],
    state: Annotated[dict, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Use the tool to think about something.

    It will not obtain new information or take any actions, but just append the thought to the log and return the result.
    Use it when complex reasoning or some cache memory or a scratchpad is needed.

    Args:
        thought: A thought to think about and log.

    Returns:
        The full log of thoughts and the new thought.
    """

    # Get existing thoughts for display purposes
    existing_thoughts = state.get("thoughts", [])
    all_thoughts = existing_thoughts + [thought]

    # Return the full log of thoughts and the new thought
    thoughts = "\n".join([f"<thought>{t}</thought>" for t in all_thoughts])
    formatted_thoughts = dedent(
        f"""Thoughts:
        {thoughts}
        """
    ).strip()

    return Command(
        update={
            # Pass list to custom reducer (will automatically limit to MAX_THOUGHTS)
            "thoughts": [thought],
            # update the message history
            "messages": [ToolMessage(formatted_thoughts, tool_call_id=tool_call_id)],
        }
    )


@tool(
    "clear_thoughts",
    description="Clear all thoughts from the agent's thought log. This tool removes all stored thoughts and provides a fresh start for thinking. Useful when you want to reset the thought context or start a new reasoning session.",
)
def clear_thoughts(
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Clear all thoughts from the agent's thought log.

    This tool removes all stored thoughts and provides a fresh start for thinking.
    Useful when you want to reset the thought context or start a new reasoning session.

    Returns:
        Confirmation that thoughts have been cleared.
    """
    from hr_screen_agent.utils import create_override

    confirmation = "All thoughts have been cleared. Starting fresh."

    return Command(
        update={
            # Use override to completely replace thoughts with empty list
            "thoughts": create_override([]),
            # update the message history
            "messages": [ToolMessage(confirmation, tool_call_id=tool_call_id)],
        }
    )
