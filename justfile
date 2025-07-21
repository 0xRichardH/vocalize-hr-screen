set dotenv-load
set dotenv-path := ".env"

uv *ARG:
  uv {{ARG}}

run:
  uv run hello.py
