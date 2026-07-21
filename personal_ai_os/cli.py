"""Command-line interface for the Personal AI Operating System."""

from __future__ import annotations

import argparse
import logging
import sys
from uuid import uuid4

from personal_ai_os.agents import CodingAgent, ManagerAgent, ResearchAgent, ReviewAgent, WritingAgent
from personal_ai_os.config import load_settings
from personal_ai_os.core.formatting import render_results
from personal_ai_os.logging_config import configure_logging
from personal_ai_os.runtime import DEFAULT_SYSTEM_PROMPT, build_agent

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="personal-ai-os",
        description="Run a modular OpenAI-powered Personal AI Operating System.",
    )
    parser.add_argument("--conversation", default="default", help="Conversation id for persisted history.")
    parser.add_argument("--env-file", default=None, help="Optional .env file path.")
    subparsers = parser.add_subparsers(dest="command")

    ask = subparsers.add_parser("ask", help="Ask the OpenAI-powered agent once.")
    ask.add_argument("message", nargs="+", help="Message for the agent.")

    chat = subparsers.add_parser("chat", help="Start interactive chat mode.")
    chat.add_argument("--new", action="store_true", help="Start a fresh conversation id.")

    for command, help_text in {
        "run": "Run the local manager-led workflow without calling an API.",
        "research": "Run only the local research agent.",
        "code": "Run only the local coding agent.",
        "write": "Run only the local writing agent.",
        "review": "Run only the local review agent.",
    }.items():
        sub = subparsers.add_parser(command, help=help_text)
        sub.add_argument("task", nargs="+", help="Task or goal for the agent.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    settings = load_settings(args.env_file)
    configure_logging(settings.log_level)
    if not args.command:
        parser.print_help()
        return 0

    if args.command == "ask":
        message = " ".join(args.message)
        try:
            print(build_agent(settings).respond(args.conversation, message, DEFAULT_SYSTEM_PROMPT))
        except RuntimeError as exc:
            logger.error("Agent runtime failed: %s", exc)
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        return 0

    if args.command == "chat":
        conversation_id = str(uuid4()) if args.new else args.conversation
        return _interactive_chat(conversation_id, settings)

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


def _interactive_chat(conversation_id: str, settings) -> int:
    try:
        agent = build_agent(settings)
    except RuntimeError as exc:
        logger.error("Agent runtime failed: %s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Personal AI OS chat started. conversation={conversation_id}")
    print("Type /exit or press Ctrl-D to quit.")
    while True:
        try:
            user_input = input("you> ").strip()
        except EOFError:
            print()
            return 0
        except KeyboardInterrupt:
            print("\nExiting.", file=sys.stderr)
            return 130
        if not user_input:
            continue
        if user_input.lower() in {"/exit", "/quit"}:
            return 0
        try:
            answer = agent.respond(conversation_id, user_input, DEFAULT_SYSTEM_PROMPT)
        except RuntimeError as exc:
            logger.error("Agent response failed: %s", exc)
            print(f"Error: {exc}", file=sys.stderr)
            continue
        print(f"ai> {answer}")


if __name__ == "__main__":
    raise SystemExit(main())
