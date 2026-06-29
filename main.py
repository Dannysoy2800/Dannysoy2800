"""Top-level command-line entry point for Danny AI Workspace."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from agents.coding_agent import CodingAgent
from agents.research_agent import ResearchAgent
from personal_ai_os.cli import main as personal_ai_os_main


def build_parser() -> argparse.ArgumentParser:
    """Build the workspace CLI parser."""
    parser = argparse.ArgumentParser(description="Danny AI Workspace command line tools.")
    subparsers = parser.add_subparsers(dest="command")

    code = subparsers.add_parser("code", help="Run the local workspace Coding Agent.")
    code.add_argument("--workspace", default=".", help="Workspace root for file operations.")
    code_subparsers = code.add_subparsers(dest="code_command")

    code_subparsers.add_parser("list", help="List readable project files.")

    read = code_subparsers.add_parser("read", help="Read a project file.")
    read.add_argument("path")

    create = code_subparsers.add_parser("create", help="Create a new project file.")
    create.add_argument("path")
    create.add_argument("content")
    create.add_argument("--overwrite", action="store_true", help="Overwrite the file if it exists.")

    update = code_subparsers.add_parser("update", help="Replace text in an existing project file.")
    update.add_argument("path")
    update.add_argument("old")
    update.add_argument("new")

    explain = code_subparsers.add_parser("explain", help="Explain a project file.")
    explain.add_argument("path")

    bugs = code_subparsers.add_parser("bugs", help="Detect simple bugs in a project file.")
    bugs.add_argument("path")

    research = subparsers.add_parser("research", help="Run the local workspace Research Agent.")
    research.add_argument("--workspace", default=".", help="Workspace root for saved research notes.")
    research.add_argument("--limit", type=int, default=3, help="Results per source to collect.")
    research_subparsers = research.add_subparsers(dest="research_command")

    research_search = research_subparsers.add_parser("search", help="Search GitHub, docs, and web pages.")
    research_search.add_argument("query")
    research_search.add_argument("--limit", type=int, default=3, help="Results per source to collect.")

    research_summarize = research_subparsers.add_parser("summarize", help="Summarize research results for a query.")
    research_summarize.add_argument("query")
    research_summarize.add_argument("--limit", type=int, default=3, help="Results per source to collect.")

    research_save = research_subparsers.add_parser("save", help="Save research notes in memory/knowledge/.")
    research_save.add_argument("query")
    research_save.add_argument("--limit", type=int, default=3, help="Results per source to collect.")

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run Danny workspace commands, falling back to the packaged Personal AI OS CLI."""
    args_list = list(sys.argv[1:] if argv is None else argv)
    if args_list and args_list[0] == "code":
        parser = build_parser()
        args = parser.parse_args(args_list)
        return _run_coding_agent(args, parser)
    if args_list and args_list[0] == "research" and {"search", "summarize", "save"}.intersection(args_list[1:]):
        parser = build_parser()
        args = parser.parse_args(args_list)
        return _run_research_agent(args, parser)
    return personal_ai_os_main(argv)


def _run_coding_agent(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    agent = CodingAgent(args.workspace)
    if args.code_command is None:
        print("Danny Coding Agent is ready.")
        print("Capabilities: list, read, create, update, explain, bugs")
        print("Try: python main.py code list")
        return 0

    if args.code_command == "list":
        for path in agent.list_project_files():
            print(path)
        return 0

    if args.code_command == "read":
        print(agent.read_file(args.path))
        return 0

    if args.code_command == "create":
        path = agent.create_file(args.path, args.content, overwrite=args.overwrite)
        print(f"Created {Path(path).relative_to(agent.workspace)}")
        return 0

    if args.code_command == "update":
        path = agent.update_file(args.path, args.old, args.new)
        print(f"Updated {Path(path).relative_to(agent.workspace)}")
        return 0

    if args.code_command == "explain":
        print(agent.explain_code(args.path))
        return 0

    if args.code_command == "bugs":
        issues = agent.detect_simple_bugs(args.path)
        if not issues:
            print("No simple bugs detected.")
            return 0
        for issue in issues:
            print(f"line {issue.line}: {issue.message}")
        return 1

    parser.error(f"Unknown code command: {args.code_command}")
    return 2


def _run_research_agent(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    agent = ResearchAgent(args.workspace)
    if args.research_command == "search":
        print(agent.format_results(agent.search(args.query, limit=args.limit)))
        return 0

    if args.research_command == "summarize":
        print(agent.summarize(args.query, limit=args.limit))
        return 0

    if args.research_command == "save":
        path = agent.save(args.query, limit=args.limit)
        print(f"Saved research notes to {Path(path).relative_to(agent.workspace)}")
        return 0

    parser.error(f"Unknown research command: {args.research_command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
