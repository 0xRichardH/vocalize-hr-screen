from typing import Annotated

from langgraph.prebuilt.chat_agent_executor import AgentState

from hr_screen_agent.utils import override_reducer


class HrScreenAgentState(AgentState):
    thoughts: Annotated[list[str], override_reducer]
