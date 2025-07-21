from google.genai import types
from livekit import agents
from livekit.agents import Agent, AgentSession, RoomInputOptions
from livekit.plugins import (
    assemblyai,
    cartesia,
    google,
    noise_cancellation,
    silero,
)


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="You are a helpful AI assistant. Keep your responses concise and conversational. You're having a real-time voice conversation, so avoid long explanations unless asked."
        )


async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    # Create agent session with AssemblyAI's advanced turn detection
    session = AgentSession(
        stt=assemblyai.STT(
            end_of_turn_confidence_threshold=0.7,
            min_end_of_turn_silence_when_confident=160,
            max_turn_silence=2400,
        ),
        llm=google.LLM(
            model="gemini-2.0-flash-exp",
            gemini_tools=[types.GoogleSearch()],
        ),
        tts=cartesia.TTS(),
        vad=silero.VAD.load(),  # Voice Activity Detection for interruptions
        turn_detection="stt",  # Use AssemblyAI's STT-based turn detection
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Greet the user when they join
    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
