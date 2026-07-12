# Hi, I'm Danny 👋

I'm building **Personal AI OS**: a modular, local-first AI workspace for agents, prompt engineering, workflow automation, memory, research, coding, writing, and review.

## Account focus

- 🤖 **AI agents:** manager, research, coding, writing, and review workflows.
- 🧠 **Memory systems:** SQLite-backed conversations plus durable key/value memory.
- ⚙️ **Automation:** CLI-first workflows that can be extended with tools and scripts.
- 🔐 **Safety:** workspace-scoped file tools and disabled-by-default model writes.
- 🧪 **Quality:** tests for CLI behavior, configuration, memory, tools, and runtime flows.

## Featured project: Personal AI OS

This repository is a Python package named `personal-ai-os` with an installable CLI:

```bash
personal-ai-os --help
```

It supports two operating modes:

1. **Local deterministic agents** for structured planning and review without API calls.
2. **OpenAI-powered conversations** with persisted memory and registered tools when an API key is configured.

## Repository layout

```text
.
├── personal_ai_os/          # Python package and runtime implementation
│   ├── agents/              # Local manager/research/coding/writing/review agents
│   ├── core/                # Shared formatting helpers
│   ├── providers/           # OpenAI Responses API provider
│   └── tools/               # File, search, memory, and registry tools
├── agents/                  # Workspace folders for future agent assets
├── memory/                  # Human-readable memory categories
├── projects/                # Project-specific working files and outputs
├── prompts/                 # Reusable prompt assets
├── config/                  # Non-secret configuration templates
├── docs/                    # Architecture and workspace documentation
├── tests/                   # Automated tests
├── main.py                  # Script entry point
├── pyproject.toml           # Package metadata
└── requirements.txt         # Runtime dependencies
```

## Quick start

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 3. Configure environment variables

Copy the example file and add your own values. Keep real secrets out of Git.

```bash
cp .env.example .env
```

Common variables:

| Variable | Purpose | Default |
| --- | --- | --- |
| `OPENAI_API_KEY` | Enables OpenAI-powered `ask` and `chat` commands. | Not set |
| `OPENAI_MODEL` | Model used by the OpenAI runtime. | `gpt-4.1-mini` |
| `PAI_DB_PATH` | SQLite memory database path. | `.personal_ai_os/memory.sqlite3` |
| `PAI_WORKSPACE` | Root directory exposed to workspace-scoped file tools. | `.` |
| `PAI_LOG_LEVEL` | Runtime log level. | `INFO` |
| `PAI_MAX_TOOL_ROUNDS` | Maximum follow-up tool rounds. | `6` |
| `PAI_SEARCH_PROVIDER` | Search provider setting. | `duckduckgo` |
| `PAI_ENABLE_MODEL_WRITES` | Allows model-triggered file writes when explicitly approved. | `false` |

## CLI examples

Run the manager-led local workflow without an API call:

```bash
personal-ai-os run "Plan my next AI automation project"
```

Run a single local specialist:

```bash
personal-ai-os research "Find risks in my launch plan"
personal-ai-os code "Design the package structure"
personal-ai-os write "Draft a project update"
personal-ai-os review "Review this implementation plan"
```

Ask the OpenAI-powered agent once:

```bash
personal-ai-os --env-file .env ask "Summarize my project priorities"
```

Start an interactive chat:

```bash
personal-ai-os --env-file .env chat --new
```

You can also run the workspace script directly:

```bash
python main.py run "Organize my AI workspace"
```

## Safety model

- File tools are scoped to `PAI_WORKSPACE` and reject path traversal outside that root.
- Model-triggered writes are disabled unless `PAI_ENABLE_MODEL_WRITES=true`.
- Write approvals are exact-match and one-time for the requested path and content.
- Do not store real API keys, private keys, credentials, or sensitive personal data in tracked files.
- Review `.env.example` for configuration names, but keep actual values in `.env` or your shell environment.

## Development

Run tests with:

```bash
python -m pytest
```

Useful documentation:

- [`docs/workspace-structure.md`](docs/workspace-structure.md) explains the top-level workspace organization.
- [`docs/repository-analysis.md`](docs/repository-analysis.md) summarizes current architecture, gaps, risks, and roadmap items.

## Roadmap

- Expand local agents from deterministic scaffolds into richer analysis workflows.
- Add a clearer human approval UX for model-generated file changes.
- Add CI, linting, formatting, and type-checking configuration.
- Introduce memory management commands such as list, delete, export, and import.
- Add stronger safeguards for sensitive files and large tool outputs.

## Profile note

This README is organized to make the account/repository easier to understand: who Danny is, what the project does, how to run it, where files live, and what comes next.
