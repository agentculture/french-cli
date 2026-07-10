"""``french learn`` — the learnability affordance.

Prints a structured self-teaching prompt. Must satisfy the agent-first rubric:
>=200 chars and mention purpose, command map, exit codes, --json, and explain.
"""

from __future__ import annotations

import argparse

from french import __version__
from french.cli._output import emit_result

_TEXT = """\
french — a private French tutor (PyPI package: french-cli).

Purpose
-------
Track progress, get an overview, get advice, read stories, and learn & practice
French (written and spoken) online from your phone. Built on an agent-first CLI
(cited from the teken `python-cli` reference) with a Culture mesh identity
(culture.yaml + AGENTS.colleague.md) and the guildmaster skill kit under
.claude/skills/.

Commands
--------
  french whoami             Identity from culture.yaml.
  french learn              This self-teaching prompt.
  french explain <path>...  Markdown docs for any noun/verb path.
  french overview           Descriptive snapshot of the agent.
  french doctor             Check the agent-identity invariants.
  french cli overview       Describe the CLI surface itself.

Machine-readable output
-----------------------
Every command supports --json. Errors in JSON mode emit
{"code", "message", "remediation"} to stderr. Stdout and stderr never mix.

Exit-code policy
----------------
  0 success
  1 user-input error (bad flag, bad path, missing arg)
  2 environment / setup error
  3+ reserved

More detail
-----------
  french explain french
"""


def _as_json_payload() -> dict[str, object]:
    return {
        # `tool` is the distribution / mesh nick; `command` is what you invoke.
        "tool": "french-cli",
        "command": "french",
        "version": __version__,
        "purpose": "A private French tutor: track progress, read stories, and "
        "practice French written and spoken.",
        "commands": [
            {"path": ["whoami"], "summary": "Identity probe from culture.yaml."},
            {"path": ["learn"], "summary": "Self-teaching prompt."},
            {"path": ["explain"], "summary": "Markdown docs by path."},
            {"path": ["overview"], "summary": "Descriptive snapshot of the agent."},
            {"path": ["doctor"], "summary": "Check the agent-identity invariants."},
            {"path": ["cli", "overview"], "summary": "Describe the CLI surface."},
        ],
        "exit_codes": {
            "0": "success",
            "1": "user-input error",
            "2": "environment/setup error",
        },
        "json_support": True,
        "explain_pointer": "french explain <path>",
    }


def cmd_learn(args: argparse.Namespace) -> int:
    if getattr(args, "json", False):
        emit_result(_as_json_payload(), json_mode=True)
    else:
        emit_result(_TEXT, json_mode=False)
    return 0


def register(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser(
        "learn",
        help="Print a structured self-teaching prompt for agent consumers.",
    )
    p.add_argument("--json", action="store_true", help="Emit structured JSON.")
    p.set_defaults(func=cmd_learn)
