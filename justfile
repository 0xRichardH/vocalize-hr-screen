set dotenv-load
set dotenv-path := ".env"

uv *ARG:
  uv {{ARG}}

dev:
  uv run app.py dev
