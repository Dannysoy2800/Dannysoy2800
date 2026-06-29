# Personal AI Operating System

A modular Python **Personal AI Operating System** that can run as a local agent shell or call the OpenAI Responses API with tool calling, web search, durable SQLite memory, file tools, conversation history, interactive chat, and logging.

## What it includes

- **OpenAI Responses API provider** for production-grade model calls and function/tool calling.
- **Manager, Research, Coding, Writing, and Review agents** for local deterministic workflows and role-specific planning.
- **Tool calling runtime** that executes model-requested tools and returns tool outputs back to the Responses API.
- **DuckDuckGo web search** tool for current web research without requiring a separate search API key.
- **SQLite memory** for durable memories plus conversation history.
- **Workspace-scoped file tools** for reading, writing, and listing files safely under a configured workspace.
- **`.env` support** for API keys and runtime configuration.
- **Interactive chat mode** plus one-shot `ask` mode.
- **Structured logging** for runtime visibility.
- **GitHub-ready packaging, requirements, tests, and `.gitignore`**.


## Danny AI workspace layout

In addition to the Python package, this repository includes a top-level workspace scaffold for organizing role-specific agents, human-readable memory, projects, prompts, scripts, config, docs, logs, and tests. See [`docs/workspace-structure.md`](docs/workspace-structure.md) for the full directory map.

You can launch the CLI through the workspace entry point:

```bash
python main.py --help
```

### Coding Agent usage

Run the first local Coding Agent:

```bash
python main.py code
```

The Coding Agent can list project files, read files, create files, update files, explain code, and detect simple bugs:

```bash
python main.py code list
python main.py code read README.md
python main.py code create notes/example.py "print('hello')"
python main.py code update notes/example.py "print('hello')" "print('hello, Danny')"
python main.py code explain main.py
python main.py code bugs main.py
```

Use `--workspace` to point the agent at a specific project directory while keeping file operations scoped to that workspace:

```bash
python main.py code --workspace ./projects/my-app list
```


### Research Agent usage

Run the local Research Agent to collect results from GitHub repositories, documentation-oriented pages, and general web pages:

```bash
python main.py research search "python agent frameworks"
```

Summarize a research query as Markdown:

```bash
python main.py research summarize "python agent frameworks"
```

Save research notes under `memory/knowledge/`:

```bash
python main.py research save "python agent frameworks"
```

Use `--workspace` when you want saved notes to go to a specific workspace root:

```bash
python main.py research --workspace ./projects/my-app save "deployment options"
```

## Project structure

```text
personal_ai_os/
  agents/                  # Local role agents and manager workflow
  core/                    # Formatting helpers
  providers/               # OpenAI Responses API adapter
  tools/                   # Search, memory, file tools, and registry
  cli.py                   # CLI and interactive chat mode
  config.py                # .env/environment settings
  logging_config.py        # Logging setup
  memory.py                # SQLite memory and conversation history
  runtime.py               # Runtime assembly
tests/                     # CLI, memory, tools, and provider tests
.env.example
requirements.txt
pyproject.toml
README.md
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

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4.1-mini
PAI_DB_PATH=.personal_ai_os/memory.sqlite3
PAI_WORKSPACE=.
PAI_LOG_LEVEL=INFO
PAI_MAX_TOOL_ROUNDS=6
PAI_SEARCH_PROVIDER=duckduckgo
```

## Usage

### One-shot AI agent call

```bash
python -m personal_ai_os.cli ask "Research Python agent frameworks and save the key takeaways to memory"
```

### Interactive chat mode

```bash
python -m personal_ai_os.cli chat
```

Start a fresh persisted conversation:

```bash
python -m personal_ai_os.cli --conversation project-alpha chat --new
```

Exit chat with `/exit`, `/quit`, Ctrl-D, or Ctrl-C.

### Conversation history

All `ask` and `chat` messages are stored in SQLite under `PAI_DB_PATH`. Reuse `--conversation <id>` to continue the same thread:

```bash
python -m personal_ai_os.cli --conversation project-alpha ask "What did we decide last time?"
```

### Local deterministic agent commands

These commands do not call OpenAI and are useful for quick scaffolding or tests:

```bash
python -m personal_ai_os.cli run "Plan a portfolio website launch"
python -m personal_ai_os.cli research "Evaluate competitors for a SaaS idea"
python -m personal_ai_os.cli code "Design a FastAPI service"
python -m personal_ai_os.cli write "Draft onboarding documentation"
python -m personal_ai_os.cli review "Review a product launch plan"
```

## Available tools

The OpenAI-powered runtime exposes these function tools to the model:

| Tool | Purpose |
| --- | --- |
| `search_web` | Search the web with DuckDuckGo and return titles, URLs, and snippets. |
| `read_file` | Read a UTF-8 file from the configured workspace. |
| `write_file` | Write a UTF-8 file inside the configured workspace. |
| `list_files` | List files in a workspace directory. |
| `remember` | Store a durable SQLite memory by namespace and key. |
| `recall` | Retrieve SQLite memories by namespace and query. |

File tools are workspace-scoped using `PAI_WORKSPACE` and reject paths that escape that directory.

## Development

Run tests:

```bash
python -m pytest
```

Run the package CLI after installing in editable mode:

```bash
pip install -e .
personal-ai-os chat
```

## Production notes

- Use separate `PAI_DB_PATH` values per environment.
- Set `PAI_WORKSPACE` to a dedicated project directory before enabling file writes.
- Keep secrets in `.env`; do not commit real keys.
- Add human approval policies before destructive file operations or shell tools.
- Consider replacing DuckDuckGo with Tavily or another commercial search provider if you need SLAs, structured citations, or higher rate limits.
- Add tracing/observability and evals before deploying autonomous workflows.

## License

Choose a license before publishing if you plan to distribute this project.
