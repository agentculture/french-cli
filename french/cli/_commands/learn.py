"""``french learn`` — the learnability affordance.

Prints a structured self-teaching prompt for an agent operating the CLI. Must
satisfy the agent-first rubric: >=200 chars and mention purpose, command map,
exit codes, --json, and explain. Also the front door to the tutor surface: it
documents the eight subject-plugin verbs the driver drives.
"""

from __future__ import annotations

import argparse

from french import __version__
from french.cli._output import emit_result

_TEXT = """\
french — a private French tutor (PyPI package: french-cli).

Purpose
-------
An LLM-free tutor engine that implements the learn subject-plugin contract:
french owns the committed French content (stories, lessons, exercises) and each
learner's mastery state, resolves what to teach next, and emits structured
teaching DIRECTIVES. You — the driving agent — do the conversational tutoring
the directive describes (present, explain, quiz), grade pass|partial|fail, and
write the result back with `record`. french never converses, grades free text,
or computes scores; learn-cli's motivation layer does the scoring.

Commands — tutor verbs (the contract surface)
---------------------------------------------
  french overview             Subject self-description: modules + content counts.
  french progress             The learner's mastery, counters, and next step.
  french advice               Deterministic study advice from stored state.
  french story list|read <id> Graded stories + a reading directive.
  french lesson start|next|repeat  Teaching directives from the curriculum.
  french practice [<scope>]   A batch of exercises to run (no scope = review).
  french record --item <id> --result pass|partial|fail   Write back one outcome.
  french doctor               Self-check + the pinned contract version.

Agent-first verbs
-----------------
  french whoami   Identity from culture.yaml.
  french learn    This self-teaching prompt.
  french explain <path>   Markdown docs for any noun/verb path.
  french cli overview     Describe the CLI surface itself.

Learner + state
---------------
Pass --learner <id> on learner-scoped verbs (default: $FRENCH_CLI_LEARNER or the
OS user; the resolved id is echoed back). State persists per learner under
$FRENCH_CLI_LEARN_HOME (or $XDG_DATA_HOME/french_cli/learn) and resumes across
sessions.

Machine-readable output
-----------------------
Every command supports --json. Errors in JSON mode emit
{"code", "message", "remediation"} to stderr. Stdout and stderr never mix.

Exit-code policy
----------------
  0 success
  1 user-input error (bad flag, unknown item/story, missing arg)
  2 environment / setup error (unwritable state, unhealthy doctor)
  3+ reserved

More detail
-----------
  french explain french
  french explain lesson
"""


def _as_json_payload() -> dict[str, object]:
    return {
        # `tool` is the distribution / mesh nick; `command` is what you invoke.
        "tool": "french-cli",
        "command": "french",
        "version": __version__,
        "purpose": "An LLM-free French tutor implementing the learn subject-plugin "
        "contract: it emits teaching directives and records graded outcomes; the "
        "driving agent does the tutoring.",
        "commands": [
            {"path": ["overview"], "summary": "Subject self-description (subject_overview)."},
            {"path": ["progress"], "summary": "Learner mastery, counters, next step."},
            {"path": ["advice"], "summary": "Deterministic study advice from state."},
            {"path": ["story", "list"], "summary": "Story summaries for the catalog."},
            {"path": ["story", "read"], "summary": "One story + a reading directive."},
            {"path": ["lesson", "start"], "summary": "A lesson directive (start)."},
            {"path": ["lesson", "next"], "summary": "Continue from mastery state."},
            {"path": ["lesson", "repeat"], "summary": "Re-issue a lesson; --harder raises it."},
            {"path": ["practice"], "summary": "A batch of exercises to run."},
            {"path": ["record"], "summary": "Write back a graded outcome; updates mastery."},
            {"path": ["doctor"], "summary": "Self-check + contract pin."},
            {"path": ["whoami"], "summary": "Identity probe from culture.yaml."},
            {"path": ["learn"], "summary": "This self-teaching prompt."},
            {"path": ["explain"], "summary": "Markdown docs by path."},
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
