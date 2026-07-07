# Repository Analysis: personal-ai-os

Generated from the repository contents on 2026-07-07. This report only reflects files present in this repository.

## 1. Architecture overview

### Package and entry points

- The project is a Python package named `personal-ai-os` with Python `>=3.10` and dependencies on `openai`, `python-dotenv`, and `duckduckgo-search`.
- The installable console script is `personal-ai-os = personal_ai_os.cli:main`.
- The top-level `main.py` delegates directly to `personal_ai_os.cli.main()` so the repository can be run as a workspace-style script.

### CLI layer

- `personal_ai_os.cli` builds an `argparse` CLI with global `--conversation` and `--env-file` options.
- Networked/OpenAI commands:
  - `ask`: sends one message through the OpenAI-powered runtime.
  - `chat`: starts an interactive chat loop and optionally creates a new UUID conversation.
- Deterministic local commands:
  - `run`: runs the manager workflow.
  - `research`, `code`, `write`, and `review`: run a single local specialized agent.

### Configuration

- `personal_ai_os.config.load_settings()` reads environment variables, optionally after loading a `.env` file.
- Settings include the OpenAI API key, model name, SQLite database path, log level, workspace path, maximum tool rounds, search provider string, and whether model-triggered writes are enabled.
- `PAI_ENABLE_MODEL_WRITES` defaults to disabled.

### Local deterministic agents

- `AgentResult` is the shared structured output model for local agents and can render itself as Markdown.
- `ManagerAgent` orchestrates local agents in this order: research, coding, writing, review.
- `ResearchAgent`, `CodingAgent`, `WritingAgent`, and `ReviewAgent` currently return deterministic scaffolded summaries, artifacts, and next steps.

### OpenAI runtime and tools

- `runtime.build_agent()` creates `SQLiteMemory`, registers default tools, and returns an `OpenAIResponsesAgent`.
- `OpenAIResponsesAgent.respond()` persists the user message, builds conversation input, calls the OpenAI Responses API, executes function calls for up to `max_tool_rounds`, returns tool outputs to the model, persists the assistant response, and returns assistant text.
- Tools are registered through `ToolRegistry`, which exposes OpenAI function schemas and dispatches calls by name.
- Default tools include:
  - `search_web`
  - `read_file`
  - `write_file`
  - `list_files`
  - `remember`
  - `recall`

### Persistence

- `SQLiteMemory` creates and uses SQLite tables for conversations, messages, and durable memories.
- Messages are stored with conversation id, role, content, and timestamp.
- Durable memories are keyed by `(namespace, key)` and can be recalled with a `LIKE` query against key or value.

### File and search tools

- `FileTools` scopes reads, writes, and directory listings to a configured workspace path using `Path.resolve()` plus `relative_to()` checks.
- Model-triggered writes require writes to be enabled and require a one-time exact approval token matching both path and content.
- `SearchTools` imports `duckduckgo_search.DDGS` lazily and returns up to 10 text search results.

### Tests

- Tests cover local CLI output, configuration defaults for model writes, SQLite memory persistence, file read/write scoping and write approval behavior, and fake OpenAI tool-call execution.

## 2. Missing features

These are features the repository itself references or scaffolds but does not yet implement fully.

1. **README is only a personal introduction, not product documentation.** It does not document installation, environment variables, CLI commands, architecture, tool behavior, testing, or security model.
2. **Workspace structure documentation is not matched by tracked directories.** `docs/workspace-structure.md` describes top-level `agents/`, `memory/`, `projects/`, `prompts/`, `scripts/`, and `config/` directories, but the repository currently tracks only the Python package, `docs/`, `logs/`, and `tests/`.
3. **`search_provider` setting is unused.** Configuration exposes `PAI_SEARCH_PROVIDER`, but `build_default_registry()` always instantiates `SearchTools()` and the tool description says DuckDuckGo.
4. **There is no user-facing approval flow for model writes.** `FileTools.approve_write_file()` exists, but `build_default_registry()` does not register an `approve_write_file` tool and the CLI does not provide a human approval mechanism for exact write requests.
5. **The deterministic local agents are scaffold implementations.** They return fixed planning/documentation/review outputs rather than performing real code analysis, research synthesis, writing, or review work.
6. **No migrations or schema versioning for SQLite.** `SQLiteMemory` creates tables if missing, but there is no schema version table or migration path for future schema changes.
7. **No packaging metadata for optional development tools.** The repository includes tests but has no development dependency group for `pytest`, linters, type checkers, or formatters.
8. **No CI configuration is present.** There is no tracked workflow or script that runs tests, linting, or type checks automatically.
9. **No `.env.example` is present despite workspace documentation listing it.** The docs mention `.env.example`, but the tracked files do not include one.
10. **No explicit license file is present.** The repository does not state licensing terms in tracked files.

## 3. Bugs

1. **OpenAI tool schema verification was incomplete.** `ToolDefinition.openai_schema()` is part of the runtime contract with the Responses API, but the original tests used fakes and did not validate the generated schema against the installed SDK type.
2. **`OpenAIResponsesAgent` can exceed the intended model-call budget by one initial call.** `max_tool_rounds` limits only follow-up tool execution rounds, while the initial model response is always made before the loop. The name may imply total tool/model rounds rather than additional tool rounds.
3. **If the model keeps requesting tools after the last allowed round, the final assistant text can be empty.** After the loop exhausts `max_tool_rounds`, the code extracts text from the last response even if that response still contains function calls and no text.
4. **`ToolRegistry.call()` assumes JSON object arguments.** A malformed JSON string, JSON array, or non-mapping dict-like value can raise low-level errors. The runtime catches exceptions during model tool calls, but direct callers receive unnormalized exceptions.
5. **`FileTools.list_files()` does not handle missing paths gracefully.** Listing a non-existent path raises a raw `FileNotFoundError` from `Path.iterdir()`.
6. **`SQLiteMemory.recall()` does not validate `limit`.** Negative or non-sensible limits are passed to SQLite directly, which may produce surprising behavior.
7. **The README repository link points to `danny-ai-os`, while this analyzed repository is `personal-ai-os`.** This can confuse users about the actual project location/name.

## 4. Security issues

1. **Secrets can be persisted in plaintext conversation history and memory.** User messages, assistant messages, and durable memories are stored directly in SQLite without redaction or encryption.
2. **File reads are model-accessible within the entire configured workspace.** The `read_file` tool can read any UTF-8 file under `PAI_WORKSPACE`; if users set the workspace too broadly, the model can access sensitive local files under that tree.
3. **Directory listing is model-accessible within the configured workspace.** `list_files` can reveal filenames and directory structure under `PAI_WORKSPACE`, which may expose sensitive project or personal metadata.
4. **Web search sends model-provided queries to DuckDuckGo.** There is no policy layer that prevents secrets or private context from being included in search queries.
5. **Tool exceptions are returned to the model.** Runtime tool failures are converted to strings and sent back to the model, which can disclose local paths, exception details, or operational information.
6. **Write approval tokens are process-local and unexpired.** Approval tokens are one-time and exact-match, but there is no expiration timestamp or audit log.
7. **No allowlist/denylist for file extensions or paths.** Workspace scoping prevents path traversal, but there is no further restriction for files such as `.env`, private keys, local databases, or credentials inside the workspace.
8. **No rate limiting or resource controls around tools.** Search, file reads, directory listing, and SQLite operations do not enforce explicit size/time limits beyond search result count.

## 5. Prioritized roadmap

### P0 — Make the current runtime safer and verifiable

1. Keep tests that validate the actual OpenAI Responses tool schema shape expected by the installed SDK/API.
2. Add a terminal condition for exhausted tool rounds that returns a clear error or final model request instead of silently persisting empty assistant text.
3. Add path/file policy controls for model-readable files, including default denies for `.env`, SQLite databases, private keys, and large files.
4. Redact or classify tool exception output before sending it back to the model.
5. Add size limits for `read_file`, `list_files`, memory values, and tool outputs.

### P1 — Document and complete the supported user experience

1. Expand `README.md` with install, configuration, CLI usage, security model, tool list, testing, and examples.
2. Add `.env.example` for documented environment variables.
3. Resolve the name/link mismatch between `README.md`, `pyproject.toml`, and repository naming.
4. Add CI to run the test suite.
5. Add development dependencies or a documented test environment setup.

### P2 — Improve write approvals and operational safety

1. Design an interactive human approval flow for file writes before exposing model writes to normal users.
2. Add approval expiration, audit logging, and optional persistent approval records.
3. Register an approval-request tool only if the intended UX is model-initiated approval requests; otherwise keep approvals outside model control.
4. Add non-destructive previews/diffs before writes.

### P3 — Grow product capabilities

1. Replace scaffold local agents with real local analysis/planning behaviors or clearly document them as demo agents.
2. Implement configurable search providers or remove the unused `search_provider` setting.
3. Add SQLite schema migrations/versioning.
4. Add memory management features such as delete, namespaces listing, and export/import.
5. Add structured logging around tool calls with sensitive-data safeguards.

### P4 — Repository and project hygiene

1. Add a license.
2. Align tracked directory structure with `docs/workspace-structure.md` or update the document to match the actual package-first layout.
3. Add linting and formatting configuration.
4. Add type checking configuration and annotations where currently loose, especially around provider response objects and tool argument parsing.
