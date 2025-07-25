from langgraph.pregel.protocol import PregelProtocol
from livekit.agents import Agent
from livekit.plugins import (
    assemblyai,
    cartesia,
    silero,
)

from .llm_adapter import LLMAdapter


class VoiceAgent(Agent):
    def __init__(self, agent: PregelProtocol, thread_id: str) -> None:
        super().__init__(
            instructions="",
            llm=LLMAdapter(
                graph=agent, config={"configurable": {"thread_id": thread_id}}
            ),
            # AssemblyAI's advanced turn detection
            stt=assemblyai.STT(
                end_of_turn_confidence_threshold=0.7,
                min_end_of_turn_silence_when_confident=160,
                max_turn_silence=2400,
            ),
            tts=cartesia.TTS(
                # model="sonic-2",
                # voice="f786b574-daa5-4673-aa0c-cbe3e8534c02",  # Katie
                language="en",
                speed="normal",
            ),
            vad=silero.VAD.load(),  # Voice Activity Detection for interruptions
            turn_detection="stt",  # Use AssemblyAI's STT-based turn detection
            allow_interruptions=True,
        )

    async def on_enter(self):
        self.session.generate_reply(
            user_input="Hello",
        )

    async def llm_node(self, chat_ctx, tools, model_settings=None):
        async def process_stream():
            async with self.llm.chat(chat_ctx=chat_ctx, tools=tools) as stream:  # type: ignore
                async for chunk in stream:
                    if chunk:
                        yield chunk

        return process_stream()
