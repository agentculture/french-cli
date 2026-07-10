# french-cli

Agent + CLI that turns Claude into a private French tutor: track progress, get an overview, get advice, read stories, and learn & practice French (written and spoken) online from your phone.

## What you get

- **An agent-first CLI** cited from [teken](https://github.com/agentculture/teken)
  (`afi-cli`) — the runtime package has no third-party dependencies.
- **A mesh identity** — `culture.yaml` (`suffix` + `backend`) and the matching
  resident prompt file (`AGENTS.colleague.md`, since this template runs
  `backend: colleague`).
- **The canonical guildmaster skill kit** (11 skills) under `.claude/skills/`,
  vendored cite-don't-import. See [`docs/skill-sources.md`](docs/skill-sources.md).
- **A build + deploy baseline** — pytest, lint, the agent-first rubric gate, and
  PyPI Trusted Publishing wired into GitHub Actions.

## Quickstart

```bash
uv sync
uv run pytest -n auto                 # run the test suite
uv run french whoami                  # identity from culture.yaml
uv run french learn                   # self-teaching prompt (add --json)
uv run teken cli doctor . --strict    # the agent-first rubric gate CI runs
```

The installed command is **`french`**; the PyPI package and repo are
**`french-cli`**. `french explain french` and `french explain french-cli` both
resolve to the root doc entry.

## CLI

| Verb | What it does |
|------|--------------|
| `french whoami` | Report this agent's nick, version, backend, and model from `culture.yaml`. |
| `french learn` | Print a structured self-teaching prompt. |
| `french explain <path>` | Markdown docs for any noun/verb path. |
| `french overview` | Read-only descriptive snapshot of the agent. |
| `french doctor` | Check the agent-identity invariants (prompt-file-present, backend-consistency). |
| `french cli overview` | Describe the CLI surface itself. |

Every command supports `--json`. Results go to stdout, errors/diagnostics to
stderr (never mixed). Exit codes: `0` success, `1` user error, `2` environment
error, `3+` reserved.

## Status

**The French-tutor domain is not implemented yet.** The scaffold — identity,
skill kit, CI, and the agent-first CLI contract — is in place, but every verb
today is generic introspection (`whoami`, `learn`, `explain`, `overview`,
`doctor`, `cli overview`). Progress tracking, advice, stories, and written /
spoken practice are still to be built.

See [`CLAUDE.md`](CLAUDE.md) for the architecture and the full conventions
(version-bump-every-PR, the `cicd` PR lane, deploy setup).

## License

Apache 2.0 — see [`LICENSE`](LICENSE).
