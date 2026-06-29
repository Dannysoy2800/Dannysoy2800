# Danny AI Workspace Structure

This repository includes a top-level workspace layout for organizing agents, memory,
projects, prompts, scripts, configuration, documentation, logs, and tests.

```text
danny-ai-workspace/
├── agents/
│   ├── coding_agent/
│   ├── planner_agent/
│   ├── research_agent/
│   ├── memory_agent/
│   ├── github_agent/
│   ├── automation_agent/
│   └── content_agent/
├── memory/
│   ├── preferences/
│   ├── workflows/
│   ├── knowledge/
│   └── corrections/
├── projects/
├── prompts/
├── scripts/
├── config/
├── docs/
├── logs/
├── tests/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Directory purposes

- `agents/`: Workspace folders for role-specific agent assets and future custom logic.
- `memory/`: Human-readable memory categories for preferences, workflows, knowledge, and corrections.
- `projects/`: Project-specific working files and outputs.
- `prompts/`: Reusable system, developer, and task prompts.
- `scripts/`: Utility scripts for local automation.
- `config/`: Configuration templates or non-secret runtime configuration.
- `docs/`: Documentation for architecture and workflows.
- `logs/`: Local runtime logs. Keep generated log files out of version control.
- `tests/`: Automated tests for the Python package and workspace behavior.

Empty directories contain `.gitkeep` files so the scaffold is preserved in Git.
