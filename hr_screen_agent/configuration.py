import os
from typing import Any, Optional

from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field


class Configuration(BaseModel):
    """The configuration for the agent."""

    chat_model: str = Field(
        default="google_genai:gemini-2.5-flash",
        description="The name of the language model to use for the agent's query generation.",
    )
    guardrail_model: str = Field(
        default="google_genai:gemini-2.5-flash-lite",
        description="The name of the language model to use for the guardrails.",
    )
    web_search_model: str = Field(
        default="gemini-2.0-flash",
        description="The name of the language model to use for web search.",
    )
    interview_duration_minutes: int = Field(
        default=15,
        description="The total duration of the interview in minutes.",
    )
    warning_threshold_minutes: int = Field(
        default=5,
        description="Number of minutes before end to show warning.",
    )
    candidate_name: str = Field(
        ..., description="The name of the candidate being interviewed."
    )
    company_name: str = Field(
        ..., description="The name of the company conducting the interview."
    )
    job_role: str = Field(
        ..., description="The job role for which the candidate is being interviewed."
    )

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )

        # Get raw values from environment or config
        raw_values: dict[str, Any] = {
            name: os.environ.get(name.upper(), configurable.get(name))
            for name in cls.model_fields.keys()
        }

        # Filter out None values
        values = {k: v for k, v in raw_values.items() if v is not None}

        return cls(**values)
