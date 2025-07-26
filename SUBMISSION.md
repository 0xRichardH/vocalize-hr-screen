---
title: "Vocalize HR Screen: AI-Powered Voice Screening Agent for Professional Interviews"
published: true
tags: devchallenge, assemblyaichallenge, ai, api
---

*This is a submission for the [AssemblyAI Voice Agents Challenge](https://dev.to/challenges/assemblyai-2025-07-16)*

## What I Built

**Vocalize HR Screen** is an intelligent voice-powered HR screening agent that conducts professional 15-minute interviews to evaluate candidates across four key areas: basic qualifications, motivation, logistical fit, and communication skills.

This project addresses the **Business Automation** category by automating the time-consuming initial HR screening process while maintaining the human touch through natural voice conversations. The agent acts as "Rachel," a professional HR recruiter who can:

- 🎯 Conduct structured, time-aware interviews
- 📄 Automatically analyze candidate CVs and job descriptions
- 🌐 Research company context in real-time
- 🛡️ Maintain professional boundaries with built-in guardrails
- 📊 Generate comprehensive evaluation reports
- ⏱️ Manage interview flow with precise timing

The system combines cutting-edge voice AI with intelligent conversation management to scale HR processes without losing the personal connection that's crucial in recruitment.

## Demo

🔗 **GitHub Repository**: [https://github.com/0xRichardH/vocalize-hr-screen](https://github.com/0xRichardH/vocalize-hr-screen)

### Live Demo Video
*[Add your demo video link here when available]*

### Demo Flow Screenshots

**Interview Setup & Document Analysis:**
- Agent automatically reads candidate CV and job description
- Initializes 15-minute timer for structured interview

**Natural Voice Conversation:**
- Professional introduction as "Rachel" from the company
- Intelligent follow-up questions based on resume analysis
- Real-time company research for contextual questions

**Comprehensive Evaluation:**
- Automated summary generation with detailed assessment
- Structured recommendations for next interview rounds
- Professional call termination with clear next steps

## GitHub Repository

{% github 0xRichardH/vocalize-hr-screen %}

**Key Repository Highlights:**
- 📁 Well-structured codebase with clear separation of concerns
- 📚 Comprehensive documentation and setup instructions
- 🔧 Easy configuration through environment variables
- 🧪 Ready-to-test with LiveKit Agents Playground
- 📝 MIT License for open source collaboration

## Technical Implementation & AssemblyAI Integration

### AssemblyAI Universal-Streaming Integration

The core of our voice processing leverages **AssemblyAI's Universal-Streaming technology** for superior speech recognition with advanced turn detection:

```python
# voice_agent/agent.py
from livekit.plugins import assemblyai

class VoiceAgent(Agent):
    def __init__(self, agent: PregelProtocol, thread_id: str) -> None:
        super().__init__(
            instructions="",
            llm=LLMAdapter(
                graph=agent, 
                config={"configurable": {"thread_id": thread_id}}
            ),
            # AssemblyAI's advanced turn detection
            stt=assemblyai.STT(
                end_of_turn_confidence_threshold=0.7,
                min_end_of_turn_silence_when_confident=160,
                max_turn_silence=2400,
            ),
            tts=cartesia.TTS(
                language="en",
                speed="normal",
            ),
            vad=silero.VAD.load(),  # Voice Activity Detection
            turn_detection="stt",  # Use AssemblyAI's STT-based turn detection
            allow_interruptions=True,
        )
```

### Key AssemblyAI Features Leveraged

**1. Intelligent Turn Detection**
- `end_of_turn_confidence_threshold=0.7`: Ensures natural conversation flow
- `min_end_of_turn_silence_when_confident=160ms`: Quick response times
- `max_turn_silence=2400ms`: Handles thoughtful pauses during interviews

**2. Professional Voice Processing**
```python
# Advanced configuration for interview scenarios
stt=assemblyai.STT(
    # Optimized for professional conversations
    end_of_turn_confidence_threshold=0.7,
    # Quick turn-around for responsive dialogue
    min_end_of_turn_silence_when_confident=160,
    # Allows for candidate thinking time
    max_turn_silence=2400,
)
```

**3. Real-time Streaming Architecture**
The system processes voice input through AssemblyAI's streaming API, enabling:
- Immediate response to candidate speech
- Natural interruption handling during conversations
- Seamless integration with LiveKit's real-time infrastructure

### Technical Architecture

**Voice-to-Intelligence Pipeline:**
```python
# voice_agent/llm_adapter.py
class LangGraphStream(llm.LLMStream):
    async def _run(self) -> None:
        state = self._chat_ctx_to_state()
        
        # Stream through LangGraph for intelligent processing
        async for output in self._graph.astream(
            state, self._config, stream_mode="updates"
        ):
            updates = next(iter(output.values()))
            if not updates:
                continue
            last_message = updates["messages"][-1]
            
            chat_chunk = _to_chat_chunk(last_message)
            if chat_chunk:
                self._event_ch.send_nowait(chat_chunk)
```

**Intelligent Agent Integration:**
```python
# hr_screen_agent/agent.py
def create_hr_screen_agent(
    checkpointer: Optional[Checkpointer] = None, debug: bool = False
) -> PregelProtocol:
    return create_react_agent(
        name="hr_screen_agent",
        model=llm,
        state_schema=HrScreenAgentState,
        pre_model_hook=pre_model_hook,  # Safety guardrails
        tools=[
            think, web_search, read_input_file,
            start_timer, check_time_remaining,
            write_interview_summary, end_call,
        ],
        prompt=agent_instructions,
        checkpointer=checkpointer,  # Persistent conversation state
        debug=debug,
    )
```

### Advanced Features

**1. Context-Aware Processing**
- Document analysis integration with voice responses
- Real-time web search for company research
- Persistent conversation state across interview sessions

**2. Professional Safety Guardrails**
```python
# hr_screen_agent/hooks/pre_model_hook.py
async def pre_model_hook(state: HrScreenAgentState, config: RunnableConfig):
    # Jailbreak prevention
    jailbreak_result = await jailbreak_guardrail(llm, last_messages)
    if not jailbreak_result.is_safe:
        return Command(goto="agent", update={"messages": safety_response})
    
    # Relevance filtering for professional context
    relevance_result = await relevance_guardrail(llm, last_messages)
    if not relevance_result.is_relevant:
        return Command(goto="agent", update={"messages": redirect_response})
```

**3. Time-Aware Interview Management**
```python
# Intelligent time tracking with AssemblyAI streaming
async def check_time_remaining():
    elapsed = (datetime.now(timezone.utc) - state["start_time"]).total_seconds() / 60
    remaining = interview_duration - elapsed
    
    if remaining <= warning_threshold:
        return f"⚠️ Warning: Only {remaining:.1f} minutes remaining"
```

### Why AssemblyAI Was Essential

**Superior Speech Recognition**: AssemblyAI's Universal-Streaming technology provides the accuracy needed for professional interviews where every word matters.

**Natural Conversation Flow**: The advanced turn detection enables natural back-and-forth dialogue essential for effective HR screening.

**Real-time Performance**: Streaming capabilities ensure responsive interactions that feel human-like rather than robotic.

**Professional Reliability**: Enterprise-grade accuracy and reliability required for business-critical HR processes.

This technical implementation showcases how AssemblyAI's cutting-edge voice technology can be leveraged to create sophisticated business automation solutions that maintain the human touch while scaling professional processes.

---

*Built with 💙 using AssemblyAI, LiveKit, LangGraph, and Google Gemini* 