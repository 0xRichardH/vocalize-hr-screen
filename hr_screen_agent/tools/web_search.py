import os
from typing import Annotated

from google.genai import Client
from google.genai.types import GoogleSearch, Tool
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg, tool

from hr_screen_agent.configuration import Configuration

# Used for Google Search API
genai_client = Client(api_key=os.getenv("GOOGLE_API_KEY"))
google_search_tool = Tool(google_search=GoogleSearch())


@tool(
    "web_search",
    description="Perform a web search using the native Google Search API",
)
def web_search(
    query: Annotated[str, "The search query to perform"],
    config: Annotated[RunnableConfig, InjectedToolArg],
) -> str:
    """Perform web research using the native Google Search API tool.

    Executes a web search using the native Google Search API tool in combination with Gemini 2.0 Flash.
    """
    configurable = Configuration.from_runnable_config(config)
    response = genai_client.models.generate_content(
        model=configurable.web_search_model,
        contents=query,
        config={
            "tools": [google_search_tool],
            "temperature": 0,
        },
    )
    return response.text or "No results found."
