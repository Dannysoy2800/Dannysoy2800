# Self-hosting Personal AI OS

This project can run as a local Docker container with persistent memory and a bind-mounted workspace.

## Prerequisites

- Docker Engine with Docker Compose support.
- An OpenAI API key for the `ask` and `chat` commands.

## Quick start

1. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set `OPENAI_API_KEY`.

3. Build the image:

   ```bash
   docker compose build
   ```

4. Start interactive chat:

   ```bash
   docker compose run --rm personal-ai-os chat --new
   ```

## Running one-off commands

Run the local manager workflow without calling an API:

```bash
docker compose run --rm personal-ai-os run "plan my day"
```

Ask the OpenAI-powered agent once:

```bash
docker compose run --rm personal-ai-os ask "Summarize my workspace"
```

## Persistence and workspace layout

- Conversation history and memory are stored in the named Docker volume at `/data/memory.sqlite3`.
- Files the agent can read are mounted from `./workspace` into `/workspace`.
- Model-initiated file writes are disabled by default through `PAI_ENABLE_MODEL_WRITES=false`.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `OPENAI_API_KEY` | empty | Secret API key used by OpenAI-powered commands. |
| `OPENAI_MODEL` | `gpt-4.1-mini` | Model name passed to the OpenAI Responses API. |
| `PAI_WORKSPACE` | `.` locally, `/workspace` in Docker Compose | Root directory exposed to file tools. |
| `PAI_DB_PATH` | `.personal_ai_os/memory.sqlite3` locally, `/data/memory.sqlite3` in Docker Compose | SQLite memory database path. |
| `PAI_LOG_LEVEL` | `INFO` | Application log level. |
| `PAI_MAX_TOOL_ROUNDS` | `6` | Maximum tool-calling turns per response. |
| `PAI_SEARCH_PROVIDER` | `duckduckgo` | Search backend used by search tools. |
| `PAI_ENABLE_MODEL_WRITES` | `false` | Enables model-requested file writes only when set to a truthy value. |

## Local Python usage

The example `.env` keeps local Python defaults relative to the repository so these commands continue to work outside Docker:

```bash
python -m personal_ai_os.cli run "plan my day"
```

Docker Compose overrides `PAI_WORKSPACE` and `PAI_DB_PATH` at runtime so container data still lands in the mounted `/workspace` and `/data` paths.

Keep `.env` private and rotate the API key if it is ever exposed.
