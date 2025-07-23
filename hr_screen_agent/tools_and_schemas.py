from pydantic import BaseModel, Field


class RelevanceOutput(BaseModel):
    """Schema for relevance guardrail decisions."""

    reasoning: str = Field(
        description="Reasoning behind the decision to allow or block the action."
    )
    is_relevant: bool = Field(
        description="Indicates whether the action is relevant to the query (True) or not (False)."
    )


class JailbreakOutput(BaseModel):
    """Schema for jailbreak guardrail decisions."""

    reasoning: str = Field(
        description="Reasoning behind the decision to allow or block the action."
    )
    is_safe: bool = Field(
        description="Indicates whether the action is safe to proceed with (True) or should be blocked (False)."
    )
