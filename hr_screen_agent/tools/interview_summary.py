from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command


@tool(
    "write_interview_summary",
    description="Write the interview summary to both the agent state and a markdown file in the output folder. This should be called when the interview is complete to generate the final evaluation report.",
)
def write_interview_summary(
    summary: Annotated[str, "The complete interview summary"],
    state: Annotated[dict, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Write the interview summary to both the agent state and a markdown file.

    Args:
        summary: The complete interview summary

    Returns:
        Command updating the state and confirming the summary was written
    """

    # Generate timestamp for filename
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    # Generate filename
    filename = f"interview_summary_{timestamp}.md"

    # Ensure output directory exists
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Write to file
    file_path = output_dir / filename

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(summary)

        confirmation_message = f"Interview summary successfully written to {file_path} and stored in agent state."

    except Exception as e:
        confirmation_message = f"Error writing interview summary to file: {str(e)}. Summary has been stored in agent state only."

    return Command(
        update={
            # Store the summary in agent state
            "interview_summary": summary,
            # Update the message history with confirmation
            "messages": [ToolMessage(confirmation_message, tool_call_id=tool_call_id)],
        }
    )


@tool(
    "get_interview_summary",
    description="Retrieve the current interview summary from the agent state if it exists.",
)
def get_interview_summary(
    state: Annotated[dict, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Retrieve the current interview summary from the agent state.

    Returns:
        Command with the current interview summary or a message if none exists
    """

    current_summary = state.get("interview_summary")

    if current_summary:
        message = f"Current interview summary:\n\n{current_summary}"
    else:
        message = "No interview summary has been written yet."

    return Command(
        update={
            "messages": [ToolMessage(message, tool_call_id=tool_call_id)],
        }
    )
