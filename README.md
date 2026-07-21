# Personal AI OS v2

A modular Python **Personal AI Operating System** with exactly the v2 core: OpenAI Responses API calls, SQLite conversation memory, DuckDuckGo web search, `.env` configuration, an interactive chat mode, and tests.

## Features

- **OpenAI Responses API** provider for model responses and web-search tool calls.
- **SQLite conversation memory** that persists user and assistant messages by conversation id.
- **DuckDuckGo web search** exposed as a model-callable `search_web` tool.
- **Environment configuration** with `.env` support and a checked-in `.env.example`.
- **Interactive chat mode** plus one-shot `ask` mode.
- **Backward-compatible CLI commands**: `run`, `research`, `code`, `write`, and `review` still work as local deterministic commands.
- **Modular architecture** with separate `providers`, `memory`, and `tools` modules.
- **Logging and clear errors** for missing configuration, tool failures, and runtime setup.

## Project structure

```text
personal_ai_os/
  agents/                  # Existing local manager/research/coding/writing/review agents
  core/                    # Output formatting helpers
  providers/               # OpenAI Responses API provider
  tools/                   # DuckDuckGo search tool and tool registry
  cli.py                   # CLI, ask mode, and interactive chat mode
  config.py                # Centralized .env/environment settings
  logging_config.py        # Logging setup
  memory.py                # SQLite conversation memory
  runtime.py               # OpenAI runtime assembly
tests/                     # Unit tests
.env.example               # Example environment file
requirements.txt           # Runtime dependencies
pyproject.toml             # Packaging and test configuration
```

## Installation

```bash
git clone <your-repo-url>
cd <your-repo>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4.1-mini
PAI_DB_PATH=.personal_ai_os/conversations.sqlite3
PAI_LOG_LEVEL=INFO
PAI_MAX_TOOL_ROUNDS=6
```

## Usage

### Ask once with OpenAI

```bash
python -m personal_ai_os.cli ask "Search for the latest Python release and summarize it"
```

### Interactive chat mode

```bash
python -m personal_ai_os.cli chat
```

Use a named conversation id to continue history later:

```bash
python -m personal_ai_os.cli --conversation project-alpha chat
python -m personal_ai_os.cli --conversation project-alpha ask "What did we discuss?"
```

Start a fresh random conversation id:

```bash
python -m personal_ai_os.cli chat --new
```

Exit chat with `/exit`, `/quit`, Ctrl-D, or Ctrl-C.

### Existing local commands

These commands remain compatible and do not call OpenAI:

```bash
python -m personal_ai_os.cli run "Plan a portfolio website launch"
python -m personal_ai_os.cli research "Evaluate competitors for a SaaS idea"
python -m personal_ai_os.cli code "Design a Python package"
python -m personal_ai_os.cli write "Draft onboarding documentation"
python -m personal_ai_os.cli review "Review a product launch plan"
```

## Configuration

All runtime configuration is centralized in `personal_ai_os/config.py`:

| Variable | Default | Purpose |
| --- | --- | --- |
| `OPENAI_API_KEY` | none | Required for `ask` and `chat`. |
| `OPENAI_MODEL` | `gpt-4.1-mini` | Model used with the Responses API. |
| `PAI_DB_PATH` | `.personal_ai_os/conversations.sqlite3` | SQLite database path for conversation memory. |
| `PAI_LOG_LEVEL` | `INFO` | Python logging level. |
| `PAI_MAX_TOOL_ROUNDS` | `6` | Maximum Responses API tool-call loop rounds. |

## Tooling

The v2 runtime exposes one model-callable tool:

| Tool | Purpose |
| --- | --- |
| `search_web` | Search DuckDuckGo and return titles, URLs, and snippets. |

## Development

Run tests:

```bash
python -m pytest
```

Run static bytecode compilation:

```bash
python -m compileall personal_ai_os
```

Install the package locally with the console script:

```bash
pip install -e .
personal-ai-os chat
```

## Production notes

- Keep real secrets in `.env` and never commit them.
- Use separate SQLite database paths for development, test, and production.
- Keep `PAI_MAX_TOOL_ROUNDS` bounded to avoid runaway tool loops.
- Review logs when debugging OpenAI, search, or memory issues.

## License

Choose a license before publishing if you plan to distribute this project.
