from typing import Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, get_buffer_string

from hr_screen_agent.prompts import (
    jailbreak_guardrail_instructions,
    relevance_guardrail_instructions,
)
from hr_screen_agent.tools_and_schemas import JailbreakOutput, RelevanceOutput


async def relevance_guardrail(
    llm: BaseChatModel, messages: Sequence[BaseMessage]
) -> RelevanceOutput:
    """Guardrail to check if the action is relevant to the query."""

    result = await llm.with_structured_output(RelevanceOutput).ainvoke(
        relevance_guardrail_instructions.format(
            chat_history=get_buffer_string(messages)
        )
    )

    return RelevanceOutput.model_validate(result)


async def jailbreak_guardrail(
    llm: BaseChatModel, messages: Sequence[BaseMessage]
) -> JailbreakOutput:
    """Guardrail to prevent jailbreak attempts."""

    result = await llm.with_structured_output(JailbreakOutput).ainvoke(
        jailbreak_guardrail_instructions.format(
            chat_history=get_buffer_string(messages)
        )
    )

    # Ensure we return the correct type
    return JailbreakOutput.model_validate(result)
