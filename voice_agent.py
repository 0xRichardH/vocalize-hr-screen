from livekit import agents
from livekit.agents import Agent, AgentSession, RoomInputOptions
from livekit.plugins import (
    assemblyai,
    cartesia,
    langchain,
    noise_cancellation,
    silero,
)

from hr_screen_agent import create_hr_screen_agent


async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    agent = create_hr_screen_agent(debug=True)

    # Create agent session with AssemblyAI's advanced turn detection
    session = AgentSession(
        stt=assemblyai.STT(
            end_of_turn_confidence_threshold=0.7,
            min_end_of_turn_silence_when_confident=160,
            max_turn_silence=2400,
        ),
        tts=cartesia.TTS(),
        vad=silero.VAD.load(),  # Voice Activity Detection for interruptions
        turn_detection="stt",  # Use AssemblyAI's STT-based turn detection
    )

    await session.start(
        room=ctx.room,
        agent=Agent(
            llm=langchain.LLMAdapter(agent),
            instructions="You are a helpful HR screening assistant. Keep your responses concise and conversational.",
        ),
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
