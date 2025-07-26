from typing import Optional

from langchain.chat_models import init_chat_model
from langgraph.prebuilt.chat_agent_executor import create_react_agent
from langgraph.pregel.protocol import PregelProtocol
from langgraph.types import Checkpointer

from hr_screen_agent.configuration import Configuration
from hr_screen_agent.hooks.pre_model_hook import pre_model_hook
from hr_screen_agent.prompts import agent_instructions, think_tool_instructions
from hr_screen_agent.state import HrScreenAgentState
from hr_screen_agent.tools import (
    check_time_remaining,
    clear_thoughts,
    end_call,
    get_interview_summary,
    list_input_files,
    read_input_file,
    start_timer,
    think,
    web_search,
    write_interview_summary,
)
from hr_screen_agent.utils import current_time_context


def create_hr_screen_agent(
    checkpointer: Optional[Checkpointer] = None, debug: bool = False
) -> PregelProtocol:
    configurable = Configuration.from_runnable_config()
    llm = init_chat_model(
        model=configurable.chat_model,
        temperature=0.5,
        max_retries=3,
    )

    return create_react_agent(
        name="hr_screen_agent",
        model=llm,
        state_schema=HrScreenAgentState,
        pre_model_hook=pre_model_hook,
        tools=[
            think,
            clear_thoughts,
            web_search,
            list_input_files,
            read_input_file,
            start_timer,
            check_time_remaining,
            write_interview_summary,
            get_interview_summary,
            end_call,
        ],
        prompt=agent_instructions.format(
            current_time_context=current_time_context(),
            think_tool_instructions=think_tool_instructions,
            candidate_name=configurable.candidate_name,
            company_name=configurable.company_name,
            job_role=configurable.job_role,
            interview_duration_minutes=configurable.interview_duration_minutes,
        ),
        checkpointer=checkpointer,
        debug=debug,
    )


# just uv run -m hr_screen_agent.agent
if __name__ == "__main__":
    import asyncio
    from datetime import datetime, timezone

    async def main():
        agent = create_hr_screen_agent(debug=False)
        async for output in agent.astream(
            {
                "start_time": datetime.now(timezone.utc),
                "messages": [
                    {
                        "role": "system",
                        "content": "Greet the user and offer your assistance.",
                    },
                    {
                        "role": "user",
                        "content": "Hello",
                    },
                ],
            },
            stream_mode="updates",
            config={
                "callbacks": [],
                "recursion_limit": 25,
                "configurable": {"thread_id": "hr_screen_agent_thread"},
            },
        ):
            updates = next(iter(output.values()))
            if not updates:
                continue
            last_message = updates["messages"][-1]
            last_message.pretty_print()

    asyncio.run(main())
