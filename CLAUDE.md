# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is right now

`french-cli` is intended to become an **agent + CLI that turns Claude into a
private French tutor** (track progress, get an overview, get advice, read
stories, learn & practice French written and spoken from your phone).

**None of that is implemented yet.** What exists today is the
`culture-agent-template` scaffold, renamed: an agent-first CLI skeleton, a mesh
identity, a vendored skill kit, and a CI/publish baseline. Every verb
(`whoami`, `learn`, `explain`, `overview`, `doctor`, `cli overview`) is generic
introspection — no French domain code exists. `learn` and the `explain` root
entry now describe the tutor *intent*, but nothing behind them teaches French.
Expect to write the domain from scratch. Some prose still carries the template's
framing (`french/__init__.py`'s docstring, `overview`'s "sibling-pattern
artifacts" section); update it as the real surface lands.

## Commands

```bash
uv sync                                  # install (creates .venv)
uv run french whoami                     # run the CLI — the command is `french`
uv run pytest -n auto                    # full suite (23 tests, ~1s)
uv run pytest tests/test_cli.py::test_whoami_text -v   # a single test
```

The four gates CI runs, in the order they'll bite you:

```bash
uv run black --check french tests
uv run isort --check-only french tests
uv run flake8 french tests
uv run bandit -c pyproject.toml -r french
npx markdownlint-cli2@0.21.0 "**/*.md" "#node_modules" "#.local" "#.claude/skills" "#.teken"
uv run teken cli doctor . --strict       # the agent-first rubric gate
```

CI's coverage invocation (`fail_under = 60`):

```bash
uv run pytest -n auto --cov=french --cov-report=xml:coverage.xml --cov-report=term -v
```

## Naming: `french` is the command, `french-cli` is the package

Two names coexist **on purpose**. Don't "fix" one into the other.

| Thing | Value |
|-------|-------|
| Console script / argparse `prog` — what you type | `french` |
| Distribution, PyPI name, repo, mesh nick (`culture.yaml` `suffix`) | `french-cli` |
| Import package | `french` |

The rule when you add a string: **invocations say `french`** (usage lines,
command maps, `explain` paths, help text); **identity says `french-cli`**
(`_FALLBACK_NICK`, `learn --json`'s `tool` field, `_pkg_version("french-cli")`,
the `overview` subject, the `doctor` report header). `learn --json` exposes both
— `tool` is the distribution, `command` is what to invoke.

The agent-first rubric resolves the tool's own name from `[project.scripts]`
and requires `explain <that name>` to resolve, so `french/explain/catalog.py`
keys its root entry on **both** `("french",)` and `("french-cli",)`. Dropping
the `("french",)` key turns the CI `lint` job red with
`FAIL explain_self: explain french exit=1` — that was a real defect, fixed in
0.4.1, and `test_explain_self_matches_console_script` now guards it.

If you ever rename the console script, the argparse `prog`, the catalog keys,
`learn.py`'s hand-maintained `_TEXT` **and** `_as_json_payload`, and the README
must all move together.

## Architecture: the agent-first contract

The CLI is cited (not imported) from [teken](https://github.com/agentculture/teken)'s
`python-cli` reference. Its shape is enforced by an external rubric —
`teken cli doctor . --strict`, run in CI — so the structure below is a
**contract, not a style preference**. The runtime has zero third-party
dependencies (`dependencies = []`); `teken` is dev-only.

**Output discipline** (`french/cli/_output.py`) — results go to stdout,
errors and diagnostics go to stderr, and they never mix. Every command takes
`--json`. Agents parse this; don't break it.

**Errors** (`french/cli/_errors.py`) — every failure raises
`CliError(code, message, remediation)`. `main()` catches it, renders
`error: <message>` + `hint: <remediation>` to stderr, and exits with the code.
Any other exception is wrapped so no Python traceback ever escapes. Exit codes:
`0` success, `1` user error, `2` environment error, `3+` reserved.

Two subtleties in `french/cli/__init__.py` that look odd until you know why:

- `_CliArgumentParser` overrides argparse's `.error()` so parse failures
  (unknown verb, bad flag) route through the same `error:`/`hint:` contract and
  exit `1` — argparse's default writes its own format and exits `2`.
- Parse errors happen *before* `args.json` exists, so `main()` pre-scans raw
  argv for `--json` and stashes the answer on the class-level `_json_hint`.
  `parser_class=_CliArgumentParser` is passed to `add_subparsers` so every
  subparser (including nested noun groups) inherits both behaviors.

**Adding a verb.** Create `french/cli/_commands/<verb>.py` exposing
`register(sub)`, call it from `_build_parser()`, and **add a matching entry to
`french/explain/catalog.py`** — the rubric fails if a registered path has no
`explain` entry. Give it `--json`. Noun groups follow the same pattern; see
`_commands/cli.py`, which exists solely because the rubric requires any noun
with action-verbs to expose `overview`.

Some non-obvious rubric requirements already encoded in the code, which will
look like dead weight if you refactor blindly:

- `overview` accepts an **ignored** `target` positional — descriptive verbs must
  never hard-fail on a missing path (`overview /no/such/path` exits 0).
- `learn` must be ≥200 chars and mention purpose, the command map, exit codes,
  `--json`, and `explain`. Its text and JSON payload are maintained by hand and
  drift from reality easily — update both when you add a verb.
- `doctor` must emit `{healthy, checks: [{id, passed, severity, message, remediation}]}`.

## Identity and the mesh

`culture.yaml` declares this agent to the AgentCulture IRC mesh:

```yaml
agents:
- suffix: french-cli
  backend: colleague
  model: sakamakismile/Qwen3.6-27B-Text-NVFP4-MTP
```

The backend is **`colleague`**, so the resident prompt file this agent runs on
is **`AGENTS.colleague.md`** — not this file. `CLAUDE.md` guides Claude Code
sessions; `AGENTS.colleague.md` is what the colleague backend loads. Keep both
in mind when you change how the agent describes itself.

`french/cli/_commands/doctor.py` enforces the `backend` → prompt-file mapping
(`claude`→`CLAUDE.md`, `colleague`→`AGENTS.colleague.md`, `acp`→`AGENTS.md`,
`gemini`→`GEMINI.md`), mirroring `steward doctor`'s invariants. **Changing
`backend:` in `culture.yaml` requires updating `_PROMPT_FILE` in `doctor.py`**,
or `test_doctor_recognizes_declared_backend` fails. That test exists precisely
to catch a backend promotion that forgets the mapping.

`whoami.py` parses `culture.yaml` with hand-rolled line scanning rather than a
YAML library, to keep runtime dependencies empty. It walks up from `__file__`
(not the CWD) so the identity is always *this agent's*, not whatever
`culture.yaml` sits in the caller's working directory. In a wheel install no
`culture.yaml` ships, and both `whoami` and `doctor` degrade to defaults.

## Vendored skills — cite, don't import

`.claude/skills/` holds 14 skills, vendored verbatim: 11 from
[guildmaster](https://github.com/agentculture/guildmaster), plus `ask-colleague`
from `colleague` and `remember`/`recall` from `eidetic-cli`. Provenance and the
re-sync procedure live in [`docs/skill-sources.md`](docs/skill-sources.md).

- **Don't hand-edit script bodies.** Re-sync from upstream instead. Where an
  in-place patch was unavoidable (the `agex`→`devex` rename, the
  `outsource`→`ask-colleague` rename) it is recorded as a tracked divergence in
  `docs/skill-sources.md` with an upstream issue. Follow that pattern.
- Every `SKILL.md` must carry `type: command` in its frontmatter. This is
  **load-bearing**: `core.skill_loader` silently skips any `SKILL.md` without a
  `type:`, even where guildmaster's upstream copy omits it.
- `markdownlint` and `sonar.exclusions` both skip `.claude/skills/**` — vendored
  copies are cited verbatim and must not be reformatted.

Optional runtime tools these skills shell out to: `devex` (>=0.21, the `cicd` PR
lane), `agtag` (>=0.1, `communicate` issue I/O), `colleague` and `eidetic`
(optional; the wrappers exit with an install hint when absent).

**Reach for `ask-colleague` reflexively.** The read-only verbs (`review`,
`explore`) run isolated in a throwaway git worktree with zero side effects — run
`review` for a diverse second opinion before opening a PR on a non-trivial diff,
and `explore` for a fresh read of an unfamiliar area. The side-effecting
`write --apply` / `write --pr` needs the user's go-ahead first.

## Conventions

**Every PR bumps the version — even docs-only, config-only, or CI-only PRs.**
The `version-check` CI job diffs `pyproject.toml`'s version against `main`,
comments on the PR, and fails the build if they match. Use the skill:

```bash
python3 .claude/skills/version-bump/scripts/bump.py patch    # or minor / major
```

It updates `pyproject.toml` and prepends a [Keep a Changelog](https://keepachangelog.com/)
entry to `CHANGELOG.md`. Write the changelog entry properly — this repo's
history uses it as the real record of *why* a change happened, and existing
entries are detailed prose, not one-liners.

Formatting is line-length 100 across `black`, `isort` (profile `black`), and
`flake8` (which extends-ignores `E203`/`W503` to stop fighting `black`).

`[tool.coverage.run] relative_files = true` is not decorative: without it,
`coverage.xml` emits absolute paths that SonarCloud cannot map to
`sonar.sources=french`, and coverage silently reports as empty.

Use the `cicd` skill for the PR lifecycle (`create PR`, `review comments`,
`address feedback`, `status`, `await`). It wraps `devex pr` and appends the
`- french-cli (Claude)` signature automatically via `_resolve-nick.sh` — don't
sign PR replies by hand when using it.

## Publishing

`.github/workflows/publish.yml` fires only on changes to `pyproject.toml` or
`french/**`. Pull requests publish a `.dev<run_number>` build to TestPyPI;
pushes to `main` publish to PyPI. Both use Trusted Publishing (OIDC), so fork
PRs skip the publish step rather than failing.
