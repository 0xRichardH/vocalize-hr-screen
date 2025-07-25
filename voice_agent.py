from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.pregel.protocol import PregelProtocol
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


class AssistantAgent(Agent):
    def __init__(self, agent: PregelProtocol, thread_id: str) -> None:
        super().__init__(
            instructions="",
            llm=langchain.LLMAdapter(
                graph=agent, config={"configurable": {"thread_id": thread_id}}
            ),
            # AssemblyAI's advanced turn detection
            stt=assemblyai.STT(
                end_of_turn_confidence_threshold=0.7,
                min_end_of_turn_silence_when_confident=160,
                max_turn_silence=2400,
            ),
            tts=cartesia.TTS(
                model="sonic-2",
                voice="f786b574-daa5-4673-aa0c-cbe3e8534c02",  # Katie
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


async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    # Create checkpointer that will persist for the entire session
    sqlite_saver = AsyncSqliteSaver.from_conn_string("checkpoints.db")

    # Initialize the checkpointer outside the session context
    checkpointer = await sqlite_saver.__aenter__()

    async def on_disconnect():
        # Clean up the checkpointer when the session ends
        await sqlite_saver.__aexit__(None, None, None)

    ctx.add_shutdown_callback(on_disconnect)

    agent = create_hr_screen_agent(checkpointer=checkpointer, debug=True)

    session = AgentSession()

    thread_id = f"{ctx.room.name}__{await ctx.room.sid}"

    # Start the session - this will run until disconnected
    await session.start(
        room=ctx.room,
        agent=AssistantAgent(agent, thread_id),
        room_input_options=RoomInputOptions(
            audio_enabled=True,
            video_enabled=False,
            text_enabled=False,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
