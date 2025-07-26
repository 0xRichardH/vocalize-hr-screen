import asyncio
from typing import Annotated

from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.types import Command
from livekit import api
from livekit.agents import get_job_context


async def hangup_call(delay_seconds: float = 15.0):
    """Helper function to hang up the current call by deleting the room.

    Args:
        delay_seconds: Time to wait before hanging up to allow speech completion
    """
    ctx = get_job_context()
    if ctx is None:
        # Not running in a job context
        return False

    try:
        # Add a delay to allow any ongoing speech to complete
        await asyncio.sleep(delay_seconds)

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
    delay_seconds: Annotated[
        float,
        "seconds to wait before hanging up to allow final message to be spoken (default: 15.0)",
    ],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """End the current call/conversation.

    This will hang up the call and terminate the session. Use this when the conversation
    has naturally concluded or when explicitly requested to end the call.

    Args:
        reason: Optional reason for ending the call
        delay_seconds: Time to wait before hanging up to allow speech completion (default: 15.0)

    Returns:
        Command to update the state and end the call.
    """

    # Schedule hangup with a delay to allow final message to be spoken
    # The delay allows the agent to finish speaking the response to this tool call
    asyncio.create_task(hangup_call(delay_seconds=delay_seconds))

    message = f"Ending call: {reason}"

    return Command(
        update={"messages": [ToolMessage(message, tool_call_id=tool_call_id)]}
    )
