"""Top-level entry point for Danny's AI workspace.

This wrapper keeps the repository layout friendly for workspace-oriented usage while
reusing the packaged Personal AI OS command-line interface.
"""

from personal_ai_os.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
