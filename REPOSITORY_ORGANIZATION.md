# 📊 COMPLETE GITHUB ORGANIZATION - Dannysoy2800/Dannysoy2800

## **What This Is**

यह आपका **Professional GitHub Profile Repository** है जो एक **Personal AI Operating System (PAI)** को host करता है। यह एक modular, Python-based AI framework है जो OpenAI के साथ integrate होता है और multiple AI agents (coding, research, writing, reviewing) को manage करता है।

### Stack
- **Language:** Python 3.10+
- **Framework:** Command-line based architecture with OpenAI API integration
- **Key Dependencies:** 
  - `openai>=1.90.0` - OpenAI model access
  - `python-dotenv>=1.0.1` - Environment configuration
  - `duckduckgo-search>=6.3.0` - Web search capability

---

## **📁 Repository Structure**

```
Dannysoy2800/
├── personal_ai_os/          # Main package - AI OS core
│   ├── __init__.py
│   ├── cli.py               # Command-line interface, agent routing
│   ├── config.py            # Settings & environment loading
│   ├── memory.py            # SQLite conversation persistence
│   ├── runtime.py           # Agent runtime builder
│   ├── logging_config.py    # Logging setup
│   │
│   ├── core/                # Core utilities
│   │   └── formatting.py    # Output formatting
│   │
│   ├── providers/           # LLM providers
│   │   ├── __init__.py
│   │   └── openai_responses.py  # OpenAI API wrapper
│   │
│   ├── tools/               # AI agent tools
│   │   ├── __init__.py
│   │   ├── files.py         # File operations (read/write/safe paths)
│   │   ├── memory.py        # Memory tool for agents
│   │   ├── registry.py      # Tool registry & schema management
│   │   └── search.py        # Web search tool
│   │
│   └── agents/              # Specialized AI agents
│       ├── manager_agent    # Orchestrator
│       ├── coding_agent     # Code generation
│       ├── research_agent   # Research tasks
│       ├── writing_agent    # Content writing
│       ├── review_agent     # Code/content review
│       ├── automation_agent # Automation workflows
│       ├── github_agent     # GitHub operations
│       ├── content_agent    # Content management
│       ├── planner_agent    # Task planning
│       └── memory_agent     # Memory management
│
├── agents/                  # Legacy agent definitions (empty placeholders)
├── projects/                # Project configurations
├── docs/                    # Documentation
├── config/                  # Configuration files
├── prompts/                 # AI prompts templates
├── memory/                  # Memory/database storage
├── scripts/                 # Utility scripts
├── logs/                    # Application logs
├── tests/                   # Test suite
│
├── main.py                  # Entry point wrapper
├── index.html               # GitHub Pages profile
├── README.md                # Profile documentation
├── pyproject.toml           # Project metadata & dependencies
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
└── .github/                 # GitHub workflows & CI/CD
```

---

## **🔄 How It Fits Together**

### Runtime Flow:

1. **Entry Point** (`main.py` → `cli.py`) - Command-line parser
2. **Configuration** (`config.py`) - Settings from `.env`
3. **Memory** (`memory.py`) - SQLite conversation storage
4. **Agent Selection** - Based on command:
   - `personal-ai-os ask <msg>` → Default agent
   - `personal-ai-os chat` → Interactive mode
   - `personal-ai-os run <task>` → Manager orchestrates agents
   - `personal-ai-os code/research/write/review <task>` → Specific agent
5. **Tools** (`tools/`) - Agents use file, search, memory, registry tools
6. **Providers** (`providers/openai_responses.py`) - OpenAI API calls
7. **Output** (`core/formatting.py`) - Results formatting

---

## **🚀 How to Run It**

### Setup:
```bash
# Clone
git clone https://github.com/Dannysoy2800/Dannysoy2800.git
cd Dannysoy2800

# Install dependencies
pip install -r requirements.txt
# or
pip install -e .

# Configure
cp .env.example .env
# Edit .env with your OPENAI_API_KEY
```

### Commands:
```bash
# Interactive chat
python main.py chat

# Single query
python main.py ask "What is machine learning?"

# Run multi-agent workflow
python main.py run "Build a Python async web scraper"

# Specific agents
python main.py code "Write a FastAPI endpoint"
python main.py research "Latest AI trends 2026"
python main.py write "Article about AI governance"
python main.py review "Review this code for bugs"
```

---

## **📋 Current Work Items**

### Pull Requests Status

| # | Title | Status | Created | Updated |
|---|-------|--------|---------|---------|
| 11 | Add Docker Compose self-hosting | 🔴 OPEN | 21 days ago | 14 days ago |
| 10 | Upgrade GitHub profile README | 🔴 OPEN | 29 days ago | 29 days ago |
| 9 | Personal AI OS v2 core: CLI, agents, OpenAI | 🔴 OPEN | 56 days ago | 47 days ago |
| 8 | Build OmniRouter AI FastAPI skeleton | 🔴 OPEN | 56 days ago | 56 days ago |
| 7 | Organize profile and project documentation | ✅ MERGED | 12 July 2026 | - |
| 6 | Align tool schemas + repository analysis | ✅ MERGED | 7 July 2026 | - |
| 5 | Enforce approved model file writes | ✅ MERGED | 5 July 2026 | - |
| 4 | Secure FileTools path validation | ✅ MERGED | 5 July 2026 | - |
| 3 | Danny AI workspace scaffold | ❌ CLOSED | 29 June 2026 | - |
| 2 | Danny AI workspace scaffold | ✅ MERGED | 29 June 2026 | - |
| 1 | Personal AI OS scaffold | ✅ MERGED | 24 June 2026 | - |

### Key Metrics
- **Total PRs:** 11
- **Open:** 4 (Need attention!)
- **Merged:** 6
- **Closed/Abandoned:** 1
- **Last Push:** Sept 1, 2026

---

## **🔧 Configuration Files**

### `.env.example` Template
```env
# OpenAI Configuration
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-4o-mini

# Workspace Settings
PAI_WORKSPACE=.
PAI_DB_PATH=.personal_ai_os/memory.sqlite3

# Logging & Limits
PAI_LOG_LEVEL=INFO
PAI_MAX_TOOL_ROUNDS=6

# Search Provider
PAI_SEARCH_PROVIDER=duckduckgo

# Feature Flags
PAI_ENABLE_MODEL_WRITES=false
```

### `pyproject.toml` Details
```toml
[project]
name = "personal-ai-os"
version = "0.1.0"
description = "A modular local-first Personal AI Operating System in Python."
requires-python = ">=3.10"
dependencies = [
  "openai>=1.90.0",
  "python-dotenv>=1.0.1",
  "duckduckgo-search>=6.3.0",
]

[project.scripts]
personal-ai-os = "personal_ai_os.cli:main"
```

---

## **📚 Core Files Analysis**

### **main.py** - Entry Point
```python
from personal_ai_os.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
```
**Purpose:** Simple wrapper that delegates to CLI module

---

### **personal_ai_os/cli.py** - Command Router
**Commands Supported:**
- `ask` - Single question to agent
- `chat` - Interactive conversation mode
- `run` - Execute manager-led workflow
- `research` - Research agent only
- `code` - Coding agent only
- `write` - Writing agent only
- `review` - Review agent only

**Key Features:**
- Persistent conversation IDs
- Multi-agent routing
- Interactive REPL with history

---

### **personal_ai_os/config.py** - Settings Manager
**Loads from Environment:**
- `OPENAI_API_KEY` → OpenAI authentication
- `OPENAI_MODEL` → Model selection (default: gpt-4o-mini)
- `PAI_WORKSPACE` → Working directory
- `PAI_DB_PATH` → SQLite database location
- `PAI_LOG_LEVEL` → Logging verbosity
- `PAI_MAX_TOOL_ROUNDS` → Max iterations per task
- `PAI_SEARCH_PROVIDER` → Search backend
- `PAI_ENABLE_MODEL_WRITES` → Allow agent file writes

**Output:** Frozen `Settings` dataclass

---

### **personal_ai_os/memory.py** - SQLite Persistence
**Three Tables:**
1. `conversations` - Conversation metadata
2. `messages` - Role-based message history
3. `memories` - Key-value namespace storage

**Key Methods:**
- `add_message()` - Save user/assistant exchanges
- `get_messages()` - Retrieve last N messages
- `remember()` - Store persistent key-value pairs
- `recall()` - Query memories with fuzzy search

---

### **personal_ai_os/providers/openai_responses.py**
**Wraps OpenAI API:**
- Function calling support
- Tool schema integration
- Response streaming
- Error handling

---

### **personal_ai_os/tools/** - Agent Capabilities
| File | Purpose | Methods |
|------|---------|---------|
| `files.py` | Safe file I/O | `read_file()`, `write_file()`, `list_dir()` |
| `search.py` | Web search | `search()` - DuckDuckGo wrapper |
| `memory.py` | Agent memory | `remember()`, `recall()` |
| `registry.py` | Tool registration | Schema generation, function binding |

---

## **🎯 Key Insights**

### Architecture Patterns
✅ **Modular Design** - Each agent is independent  
✅ **Tool Registry** - Extensible capability system  
✅ **Persistence** - SQLite for conversations & memories  
✅ **Configuration** - Environment-driven settings  
✅ **CLI-First** - Command-line centric interface  

### Security Features
🔒 **Safe Path Validation** - FileTools checks paths  
🔒 **Model Write Control** - Flag to allow/deny file writes  
🔒 **Environment Secrets** - API keys via .env  

### Active Development
📌 **4 Open PRs** - Awaiting review/merge  
📌 **Last commit:** Sept 1, 2026  
📌 **Focus:** Docker setup, README improvements, Core agents  

---

## **💡 Next Steps**

### Priority Actions
1. ✅ **PR #11** - Merge Docker Compose setup
2. ✅ **PR #10** - Finalize GitHub profile README
3. ✅ **PR #9** - Review & merge Personal AI OS v2 core
4. ⏳ **PR #8** - FastAPI OmniRouter completion

### Development Opportunities
- Fill out agent implementations in `personal_ai_os/agents/`
- Add missing `docs/` documentation
- Expand `tests/` test coverage
- Populate `prompts/` with specialized prompts
- Setup `.github/workflows/` for CI/CD

---

## **🔗 Key Dependencies Map**

```
main.py
  └─> personal_ai_os.cli:main()
        ├─> load_settings() [config.py]
        ├─> configure_logging() [logging_config.py]
        └─> build_agent() [runtime.py]
              ├─> SQLiteMemory [memory.py]
              ├─> OpenAIResponses [providers/openai_responses.py]
              └─> Tool Registry [tools/registry.py]
                    ├─> FileTools [tools/files.py]
                    ├─> SearchTools [tools/search.py]
                    └─> MemoryTools [tools/memory.py]
```

---

## **📞 Support & Questions**

**For Development:**
- Check `.env.example` for configuration template
- Review test suite in `tests/` for usage examples
- See `docs/` for architecture details

**For Deployment:**
- PR #11 includes Docker Compose setup
- Use `pyproject.toml` for packaging

**For Extension:**
- Add agents in `personal_ai_os/agents/`
- Register tools in `tools/registry.py`
- Add prompts in `prompts/` directory

---

**Generated:** September 16, 2026  
**Repository:** https://github.com/Dannysoy2800/Dannysoy2800  
**Last Updated:** September 1, 2026
