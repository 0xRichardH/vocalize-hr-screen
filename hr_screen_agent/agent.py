import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt.chat_agent_executor import create_react_agent
from langgraph.pregel.protocol import PregelProtocol

from hr_screen_agent.configuration import Configuration
from hr_screen_agent.prompts import agent_instructions


def create_hr_screen_agent(debug: bool = False) -> PregelProtocol:
    configurable = Configuration.from_runnable_config()
    llm = ChatGoogleGenerativeAI(
        model=configurable.chat_model,
        temperature=1.0,
        max_retries=3,
        api_key=os.getenv("GEMINI_API_KEY"),
    )

    return create_react_agent(
        name="hr_screen_agent",
        model=llm,
        tools=[],
        prompt=agent_instructions,
        debug=debug,
    )


if __name__ == "__main__":
    agent = create_hr_screen_agent(debug=True)
    response = agent.invoke(
        input={
            "messages": [
                {
                    "role": "user",
                    "content": "Hello, I am looking for a job in software development. Can you help me?",
                }
            ],
            "configurable": {
                "chat_model": "gemini-2.5-flash",
            },
        }
    )
    print(response)
