set dotenv-load
set dotenv-path := ".env"

uv *ARG:
  uv {{ARG}}

dev:
  uv run voice_agent.py dev
