"""Command-line interface for the Personal AI Operating System."""

from __future__ import annotations

import argparse

from personal_ai_os.agents import CodingAgent, ManagerAgent, ResearchAgent, ReviewAgent, WritingAgent
from personal_ai_os.core.formatting import render_results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="personal-ai-os",
        description="Run a modular local Personal AI Operating System.",
    )
    subparsers = parser.add_subparsers(dest="command")

    for command, help_text in {
        "run": "Run the full manager-led workflow.",
        "research": "Run only the research agent.",
        "code": "Run only the coding agent.",
        "write": "Run only the writing agent.",
        "review": "Run only the review agent.",
    }.items():
        sub = subparsers.add_parser(command, help=help_text)
        sub.add_argument("task", nargs="+", help="Task or goal for the agent.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 0

    task = " ".join(args.task)
    if args.command == "run":
        result = ManagerAgent().run(task)
    else:
        agent_map = {
            "research": ResearchAgent,
            "code": CodingAgent,
            "write": WritingAgent,
            "review": ReviewAgent,
        }
        result = agent_map[args.command]().run(task)

    print(render_results([result]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
