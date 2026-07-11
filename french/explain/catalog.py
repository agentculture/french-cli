"""Markdown catalog for ``french explain <path>``.

Each entry is verbatim markdown. Keys are command-path tuples. The empty tuple
and both spellings of the tool's name — ``("french",)`` (the installed console
script) and ``("french-cli",)`` (the distribution / repo / mesh nick) — resolve
to the root entry. Every registered command path has an entry here
(``test_every_registered_path_has_catalog_entry`` enforces it).

Keep bodies self-contained: an agent reading one entry should get enough
context without chaining reads.
"""

from __future__ import annotations

_ROOT = """\
# french

A private, LLM-free French tutor implementing the learn subject-plugin contract.
It owns the committed French content (stories, lessons, exercises) and each
learner's mastery state, resolves what to teach next, and emits structured
teaching directives. The driving agent (or human) does the conversational
tutoring and writes graded outcomes back with `record`.

Installed command: `french`. PyPI package and repo: `french-cli`. Mesh nick:
`french-cli`.

## Tutor verbs (the contract surface)

- `french overview` — subject self-description: modules + content counts.
- `french progress` — the learner's mastery, counters, and next step.
- `french advice` — deterministic study advice from stored state.
- `french story list|read <id>` — graded stories + a reading directive.
- `french lesson start|next|repeat` — teaching directives from the curriculum.
- `french practice [<scope>]` — a batch of exercises to run (no scope = review).
- `french record --item <id> --result pass|partial|fail` — write back one outcome.
- `french doctor` — self-check + the pinned contract version.

## Agent-first verbs

- `french whoami` — identity probe from `culture.yaml`.
- `french learn` — structured self-teaching prompt.
- `french explain <path>` — markdown docs for any noun/verb.
- `french cli overview` — describe the CLI surface.

## Exit-code policy

- `0` success
- `1` user-input error
- `2` environment / setup error
- `3+` reserved

## See also

- `french explain lesson`
- `french explain record`
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

Prints a structured self-teaching prompt for an agent operating the CLI: the
tutor purpose, the eight subject-plugin verbs, the learner/state model, exit-code
policy, `--json` support, and the `explain` pointer.

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
    french explain lesson
    french explain --json <path>
"""

_OVERVIEW = """\
# french overview

The subject's self-description (contract `subject_overview`): identity, the
ordered course modules (the web face renders one sub-page per module), and
content counts. Learner-independent and side-effect free.

The `--json` payload carries the contract fields (`schema_version`, `kind`,
`subject`, `display_name`, `description`, `modules`, `content`) plus the
`sections` key the agent-first rubric checks. Accepts an ignored `target` so a
stray path never hard-fails.

## Usage

    french overview
    french overview --json
"""

_PROGRESS = """\
# french progress

Where the learner stands in this subject (contract `progress`): per-item mastery
on the ladder `unknown → introduced → practiced → mastered`, the counters
`items_total`/`items_touched`/`items_mastered`, weak items, and the subject's own
`next` recommendation. Read-only — a pure function of stored state.

## Usage

    french progress
    french progress --learner ori --json
"""

_ADVICE = """\
# french advice

Deterministic study advice derived from stored state (contract `advice`): what to
shore up and why, each entry with a runnable command. No LLM. May seed a single
"start here" entry for a brand-new learner.

## Usage

    french advice
    french advice --learner ori --json
"""

_STORY = """\
# french story

The shared content surface.

- `french story list [--level beginner|intermediate|advanced]` — level-tagged
  summaries for the catalog (contract `story_list`, learner-independent).
- `french story read <id>` — the full committed story wrapped in a teaching
  directive (contract `story_read`): present paragraph-at-a-time, use the
  glossary on demand, run the comprehension exercises, record each result.
  Learner-scoped; an unknown id exits 1.

Bare `french story` lists.

## Usage

    french story list --json
    french story read dev-cafe --learner ori --json
"""

_STORY_LIST = """\
# french story list

Level-tagged story summaries (id, title, level, exercise count) for the catalog
— contract `story_list`. Learner-independent, so the static web catalog builds
from it. Filter with `--level`.

## Usage

    french story list
    french story list --level beginner --json
"""

_STORY_READ = """\
# french story read <id>

Returns one full committed story (the shared `story` schema, verbatim) wrapped in
a teaching directive — contract `story_read`. Learner-scoped: reading updates the
learner's current position. An unknown story id exits 1 with the error shape.

## Usage

    french story read dev-cafe
    french story read dev-cafe --learner ori --json
"""

_LESSON = """\
# french lesson

Start / continue / repeat a lesson (contract `lesson_directive`). The subject
resolves *what* to teach; the directive tells the driver *how*.

- `french lesson start [<target>]` — a lesson by lesson id, module id, or item
  id (first exposure lifts its items to `introduced`).
- `french lesson next` — continue from mastery state.
- `french lesson repeat [<id>] [--harder]` — re-issue a lesson; `--harder`
  increments its integer difficulty rung (never-ending progression).

Bare `french lesson` continues from mastery state.

## Usage

    french lesson start l.greetings --json
    french lesson next --learner ori --json
    french lesson repeat l.numbers --harder --json
"""

_LESSON_START = """\
# french lesson start [<target>]

Emit a lesson directive for a specific lesson — resolved from a lesson id, a
module id (its first lesson), or an item id (the lesson containing it). With no
target, starts the next lesson from mastery state. First exposure lifts the
lesson's items to `introduced` and sets the current position.

## Usage

    french lesson start l.greetings --json
    french lesson start premiers-pas --learner ori --json
"""

_LESSON_NEXT = """\
# french lesson next

Emit the lesson directive for the first not-yet-mastered item's lesson —
continuing from the learner's mastery state.

## Usage

    french lesson next
    french lesson next --learner ori --json
"""

_LESSON_REPEAT = """\
# french lesson repeat [<id>] [--harder]

Re-issue a lesson (default: the learner's current or next lesson). `--harder`
increments the lesson's integer difficulty rung and raises the directive's bar —
the repeatable-lessons half of never-ending progression.

## Usage

    french lesson repeat l.numbers --json
    french lesson repeat l.numbers --harder --learner ori --json
"""

_PRACTICE = """\
# french practice [<scope>]

A batch of exercises for the driver to run, grade `pass|partial|fail` against the
answer/rubric, and record — contract `practice_directive`. `scope` may be an item
id, a module id, or a lesson id; with no scope (or `review`) the subject picks the
learner's weakest touched items.

## Usage

    french practice fr.numbers.prix --json
    french practice --learner ori --json      # review the weakest items
"""

_RECORD = """\
# french record --item <id> --result pass|partial|fail

The driver's write-back after grading (contract `record_ack`). The subject
appends the raw result to history, updates the item's mastery (inferred from
`--result` unless `--mastery` is given; inference never regresses), and acks with
the normalized `recorded` object — raw observations only, never a score.

Flags: `--activity lesson|practice|story` (default practice), `--exercise <id>`,
`--story <id>`, `--lesson-id <id>`, `--correct N`, `--total N`,
`--duration-seconds F`, `--notes ...`, `--mastery <level>`.

## Usage

    french record --item fr.numbers.prix --result pass --json
    french record --learner ori --item fr.numbers.prix --activity practice \\
      --exercise prix-1 --result partial --correct 1 --total 2 --json
"""

_DOCTOR = """\
# french doctor

Self-check + contract pin (contract `subject_doctor`). Keeps the mesh
agent-identity checks (`prompt-file-present`, `backend-consistency` →
`colleague` requires `AGENTS.colleague.md`, `skills-present`) and adds the
subject checks: `content-store-present` (stories validate), `learner-state-writable`
(the XDG state dir), and `contract-schemas-pinned`. Emits `contract_version`.
Exit 0 healthy, 2 unhealthy.

## Usage

    french doctor
    french doctor --json
"""

_CLI = """\
# french cli

Noun group for CLI-surface introspection. `cli overview` describes the CLI
itself (distinct from the global `overview`, which describes the subject).

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
    ("progress",): _PROGRESS,
    ("advice",): _ADVICE,
    ("story",): _STORY,
    ("story", "list"): _STORY_LIST,
    ("story", "read"): _STORY_READ,
    ("lesson",): _LESSON,
    ("lesson", "start"): _LESSON_START,
    ("lesson", "next"): _LESSON_NEXT,
    ("lesson", "repeat"): _LESSON_REPEAT,
    ("practice",): _PRACTICE,
    ("record",): _RECORD,
    ("doctor",): _DOCTOR,
    ("cli",): _CLI,
    ("cli", "overview"): _CLI,
}
