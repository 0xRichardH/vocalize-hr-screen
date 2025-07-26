from typing import Annotated

from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.types import Command
from livekit import api
from livekit.agents import get_job_context


async def hangup_call():
    """Helper function to hang up the current call by deleting the room."""
    ctx = get_job_context()
    if ctx is None:
        # Not running in a job context
        return False

    try:
        await ctx.api.room.delete_room(api.DeleteRoomRequest(room=ctx.room.name))
        return True
    except Exception as e:
        print(f"Error hanging up call: {e}")
        return False


@tool(
    "end_call",
    description="End the current call/conversation. This will hang up the call and terminate the session. Use this when the conversation has naturally concluded or when explicitly requested to end the call.",
)
async def end_call(
    reason: Annotated[str, "reason for ending the call"],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """End the current call/conversation.

    This will hang up the call and terminate the session. Use this when the conversation
    has naturally concluded or when explicitly requested to end the call.

    Args:
        reason: Optional reason for ending the call

    Returns:
        Command to update the state and end the call.
    """

    await hangup_call()

    message = f"Ending call: {reason}"

    return Command(
        update={"messages": [ToolMessage(message, tool_call_id=tool_call_id)]}
    )
