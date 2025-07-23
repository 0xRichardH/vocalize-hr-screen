from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END
from langgraph.types import Command

from hr_screen_agent.configuration import Configuration
from hr_screen_agent.hooks.guardrail import (
    jailbreak_guardrail,
    relevance_guardrail,
)
from hr_screen_agent.state import HrScreenAgentState


async def pre_model_hook(state: HrScreenAgentState, config: RunnableConfig) -> Command:
    state = state.copy()
    messages = state["messages"]

    # skip guardrails if the last message is not a user message
    if not isinstance(messages[-1], HumanMessage):
        return Command(update={**state})

    configure = Configuration.from_runnable_config(config)
    llm = init_chat_model(configure.guardrail_model)
    # send the last 3 messages to the guardrails
    last_messages = messages[-15:] if len(messages) >= 15 else messages

    # Check jailbreak guardrail
    jailbreak_result = await jailbreak_guardrail(llm, last_messages)
    if not jailbreak_result.is_safe:
        return Command(
            graph=Command.PARENT,
            goto=END,
            update={"messages": [AIMessage(content=jailbreak_result.reasoning)]},
        )

    # Check relevance guardrail
    relevance_result = await relevance_guardrail(llm, last_messages)
    if not relevance_result.is_relevant:
        return Command(
            graph=Command.PARENT,
            goto=END,
            update={"messages": [AIMessage(content=relevance_result.reasoning)]},
        )

    return Command(update={**state})
