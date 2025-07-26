import logging

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from livekit import agents
from livekit.agents import AgentSession, RoomInputOptions
from livekit.plugins import (
    noise_cancellation,
)

from hr_screen_agent import create_hr_screen_agent
from voice_agent import VoiceAgent

logger = logging.getLogger("vocalize-hr-screen-agent")
logger.setLevel(logging.INFO)


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
        agent=VoiceAgent(agent, thread_id),
        room_input_options=RoomInputOptions(
            audio_enabled=True,
            video_enabled=False,
            text_enabled=False,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
