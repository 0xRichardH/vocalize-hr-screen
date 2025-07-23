from langchain.chat_models import init_chat_model
from langgraph.prebuilt.chat_agent_executor import create_react_agent
from langgraph.pregel.protocol import PregelProtocol

from hr_screen_agent.configuration import Configuration
from hr_screen_agent.hooks.pre_model_hook import pre_model_hook
from hr_screen_agent.prompts import agent_instructions, think_tool_instructions
from hr_screen_agent.state import HrScreenAgentState
from hr_screen_agent.tools import clear_thoughts, think, web_search
from hr_screen_agent.utils import current_time_context


def create_hr_screen_agent(debug: bool = False) -> PregelProtocol:
    configurable = Configuration.from_runnable_config()
    llm = init_chat_model(
        model=configurable.chat_model,
        temperature=1.0,
        max_retries=3,
    )

    return create_react_agent(
        name="hr_screen_agent",
        model=llm,
        state_schema=HrScreenAgentState,
        pre_model_hook=pre_model_hook,
        tools=[think, clear_thoughts, web_search],
        prompt=agent_instructions.format(
            current_time_context=current_time_context(),
            think_tool_instructions=think_tool_instructions,
            company_name="Tech Innovators Inc.",
            job_role="Software Engineer",
        ),
        debug=debug,
    )


# just uv run -m hr_screen_agent.agent
if __name__ == "__main__":
    import asyncio

    async def main():
        agent = create_hr_screen_agent(debug=True)
        async for output in agent.astream(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "Hello, I am looking for a job in software development. Can you help me?",
                    }
                ]
            },
            stream_mode="updates",
            config={
                "callbacks": [],
                "recursion_limit": 25,
                "configurable": {"thread_id": "hr_screen_agent_thread"},
            },
        ):
            last_message = next(iter(output.values()))["messages"][-1]  # type: ignore
            last_message.pretty_print()

    asyncio.run(main())
