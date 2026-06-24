# Personal AI Operating System

A GitHub-ready Python starter project for a local-first **Personal AI Operating System**. It ships with a manager agent, specialized worker agents, and a CLI that produces structured Markdown output without requiring external API credentials.

## Features

- **Manager Agent** orchestrates a full workflow across specialized agents.
- **Research Agent** turns a goal into assumptions, focus areas, and open questions.
- **Coding Agent** proposes implementation structure and engineering next steps.
- **Writing Agent** converts context into user-facing documentation plans.
- **Review Agent** checks completeness, risks, and follow-up actions.
- **CLI interface** supports full workflows or direct access to individual agents.
- **Modular folder structure** ready for tests, provider adapters, tools, and memory.

## Project structure

```text
personal_ai_os/
  agents/
    base.py
    manager.py
    research.py
    coding.py
    writing.py
    review.py
  core/
    formatting.py
  cli.py
tests/
  test_cli.py
requirements.txt
README.md
```

## Installation

```bash
git clone <your-repo-url>
cd <your-repo>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The current implementation uses only the Python standard library at runtime.

## Usage

Run the full manager-led operating system workflow:

```bash
python -m personal_ai_os.cli run "Plan a portfolio website launch"
```

Run a specialized agent directly:

```bash
python -m personal_ai_os.cli research "Evaluate competitors for a SaaS idea"
python -m personal_ai_os.cli code "Design a FastAPI service"
python -m personal_ai_os.cli write "Draft onboarding documentation"
python -m personal_ai_os.cli review "Review a product launch plan"
```

## Development

Run the test suite:

```bash
python -m pytest
```

## Extension ideas

- Add LLM provider adapters for OpenAI or other model APIs.
- Add tool permissions and human approval policies before autonomous actions.
- Add persistent memory with SQLite, Postgres, or a vector database.
- Add richer terminal output with optional dependencies such as `rich`.
- Add task files, run logs, and workspace-aware coding tools.

## License

Choose a license before publishing if you plan to distribute this project.
