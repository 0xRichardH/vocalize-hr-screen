from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg, InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

from hr_screen_agent.configuration import Configuration


@tool(
    "check_time_remaining",
    description="Check how much time remains in the interview and notify if the interview is about to end. Use this tool periodically to track interview progress and ensure proper time management.",
)
def check_time_remaining(
    state: Annotated[dict, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
    config: Annotated[RunnableConfig, InjectedToolArg],
) -> Command:
    """Check the remaining time in the interview and provide warnings when time is running out.

    Uses configuration settings for interview duration and warning thresholds.

    Returns:
        Time status and warnings if applicable
    """
    # Get configuration settings
    configuration = Configuration.from_runnable_config(config)
    interview_duration_minutes = configuration.interview_duration_minutes
    warning_threshold_minutes = configuration.warning_threshold_minutes
    start_time: Optional[datetime] = state.get("start_time") if state else None

    if not start_time:
        message = "⚠️ Interview start time not set. Unable to track time remaining."
        return Command(
            update={
                "messages": [ToolMessage(message, tool_call_id=tool_call_id)],
            }
        )

    current_time = datetime.now(timezone.utc)
    elapsed_time = current_time - start_time
    total_duration = timedelta(minutes=interview_duration_minutes)
    remaining_time = total_duration - elapsed_time

    # Calculate remaining minutes
    remaining_minutes = int(remaining_time.total_seconds() / 60)
    elapsed_minutes = int(elapsed_time.total_seconds() / 60)

    # Determine status and message
    if remaining_time <= timedelta(0):
        message = f"⏰ **TIME IS UP!** The {interview_duration_minutes}-minute interview has ended. Please wrap up the conversation politely and thank the candidate for their time."

    elif remaining_time <= timedelta(minutes=warning_threshold_minutes):
        message = f"⚠️ **TIME WARNING:** Only {remaining_minutes} minutes remaining in the interview! Please begin wrapping up the conversation and prepare to conclude."

    elif remaining_time <= timedelta(minutes=warning_threshold_minutes * 2):
        message = f"⏳ **HEADS UP:** {remaining_minutes} minutes remaining in the interview. Consider moving toward concluding questions."

    else:
        message = f"✅ Time check: {elapsed_minutes} minutes elapsed, {remaining_minutes} minutes remaining in the {interview_duration_minutes}-minute interview."

    return Command(
        update={
            "messages": [ToolMessage(message, tool_call_id=tool_call_id)],
        }
    )


@tool(
    "start_timer",
    description="Start or restart the interview timer by setting the start time to the current time. Use this at the beginning of the interview or to reset the timer.",
)
def start_timer(
    tool_call_id: Annotated[str, InjectedToolCallId],
    config: Annotated[RunnableConfig, InjectedToolArg],
) -> Command:
    """Start or restart the interview timer.

    Sets the start_time to the current UTC time, which initializes or resets
    the interview timer for time tracking purposes.

    Returns:
        Confirmation that the timer has been started
    """
    current_time = datetime.now(timezone.utc)
    configuration = Configuration.from_runnable_config(config)

    message = f"""⏱️ **Interview Timer Started**

🚀 **Timer Started:** {current_time.strftime("%H:%M:%S UTC")}
📅 **Interview Duration:** {configuration.interview_duration_minutes} minutes
⏰ **Expected End Time:** {(current_time + timedelta(minutes=configuration.interview_duration_minutes)).strftime("%H:%M:%S UTC")}

✅ Time tracking is now active. Use `check_time_remaining` to monitor progress."""

    return Command(
        update={
            "start_time": current_time,
            "messages": [ToolMessage(message, tool_call_id=tool_call_id)],
        }
    )
