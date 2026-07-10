"""Markdown catalog for ``french explain <path>``.

Each entry is verbatim markdown. Keys are command-path tuples. The empty tuple
and both spellings of the tool's name — ``("french",)`` (the installed console
script) and ``("french-cli",)`` (the distribution / repo / mesh nick) — resolve
to the root entry. The agent-first rubric resolves the tool's own name from
``[project.scripts]`` and requires ``explain <that name>`` to work; the
distribution alias is kept because that is the name on PyPI and in the mesh.

Keep bodies self-contained: an agent reading one entry should get enough
context without chaining reads.
"""

from __future__ import annotations

_ROOT = """\
# french

A private French tutor: track progress, get an overview, get advice, read
stories, and learn & practice French (written and spoken) online from your
phone.

Installed command: `french`. PyPI package and repo: `french-cli`. Mesh nick:
`french-cli`.

## Verbs

- `french whoami` — identity probe from `culture.yaml`.
- `french learn` — structured self-teaching prompt.
- `french explain <path>` — markdown docs for any noun/verb.
- `french overview` — descriptive snapshot of the agent.
- `french doctor` — check the agent-identity invariants.
- `french cli overview` — describe the CLI surface.

## Exit-code policy

- `0` success
- `1` user-input error
- `2` environment / setup error
- `3+` reserved

## See also

- `french explain whoami`
- `french explain doctor`
"""

_WHOAMI = """\
# french whoami

Reports the agent's identity from `culture.yaml`: nick (`suffix`), backend,
served model, and the package version. Read-only.

## Usage

    french whoami
    french whoami --json
"""

_LEARN = """\
# french learn

Prints a structured self-teaching prompt covering purpose, command map,
exit-code policy, `--json` support, and the `explain` pointer.

## Usage

    french learn
    french learn --json
"""

_EXPLAIN = """\
# french explain <path>

Prints markdown documentation for any noun/verb path. Unlike `--help` (terse,
positional), `explain` is global and addressable by path.

Both `french explain french` and `french explain french-cli` resolve to this
root entry — the command is `french`, the distribution is `french-cli`.

## Usage

    french explain french
    french explain whoami
    french explain --json <path>
"""

_OVERVIEW = """\
# french overview

Read-only descriptive snapshot of the agent: identity (from `culture.yaml`), the
verb surface, and the sibling-pattern artifacts the template carries. Accepts an
ignored `target` so a stray path never hard-fails.

## Usage

    french overview
    french overview --json
"""

_DOCTOR = """\
# french doctor

Checks the agent-identity invariants `steward doctor` verifies:
prompt-file-present and backend-consistency (`colleague` → `AGENTS.colleague.md`), plus a
skills-present check. Exits 1 when unhealthy.

## Usage

    french doctor
    french doctor --json
"""

_CLI = """\
# french cli

Noun group for CLI-surface introspection. `cli overview` describes the CLI
itself (distinct from the global `overview`, which describes the agent).

## Usage

    french cli overview
    french cli overview --json
"""


ENTRIES: dict[tuple[str, ...], str] = {
    (): _ROOT,
    # Both the console script and the distribution name resolve to the root.
    ("french",): _ROOT,
    ("french-cli",): _ROOT,
    ("whoami",): _WHOAMI,
    ("learn",): _LEARN,
    ("explain",): _EXPLAIN,
    ("overview",): _OVERVIEW,
    ("doctor",): _DOCTOR,
    ("cli",): _CLI,
    ("cli", "overview"): _CLI,
}
