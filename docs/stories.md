# The French graded-reader story ladder

`content/stories/*.json` is french-cli's committed story content: short,
self-contained graded readers a learner reads through the tutor's `story`
verbs. Each file is one story, validated against the shared story schema that
`learn-cli` ships at `learn/contract/schemas/story.json` (contract version
`1.0`) — the same schema culture-guide's scenario stories validate against, so
a `story read` payload can never drift from what the CLI, the MCP tool, and the
web page all show.

This document is the reproducible pipeline: how the ladder was produced, how
to validate a story, how to add another one, and the checklist a human
reviews before a story merges.

## The ladder

11 stories across the three schema-level rungs (`beginner` / `intermediate` /
`advanced`), with a CEFR `level_detail` tag for finer grading:

| id | level | level_detail | title | words |
|----|-------|---------------|-------|------:|
| `fr-a1-le-marche` | beginner | A1 | Le marché du mercredi | 169 |
| `fr-a1-la-rentree` | beginner | A1 | La rentrée de Nina | 175 |
| `fr-a2-le-cafe-du-coin` | beginner | A2 | Un café entre amis | 211 |
| `fr-a2-le-weekend-a-la-montagne` | beginner | A2 | Un week-end à la montagne | 217 |
| `fr-b1-la-recherche-appartement` | intermediate | B1 | La recherche d'appartement | 244 |
| `fr-b1-le-covoiturage` | intermediate | B1 | Le covoiturage | 232 |
| `fr-b1-la-fete-des-voisins` | intermediate | B1 | La fête des voisins | 266 |
| `fr-b1-entretien-embauche` | intermediate | B1 | Un entretien d'embauche | 262 |
| `fr-b2-le-teletravail` | advanced | B2 | Le télétravail, une révolution silencieuse | 277 |
| `fr-b2-la-transition-ecologique` | advanced | B2 | La transition écologique, vue d'un petit village | 312 |
| `fr-c1-le-vieux-libraire` | advanced | C1 | Le vieux libraire | 368 |

Word count scales with level (150-220 for A1/A2, 230-270 for B1, 275-370 for
B2/C1), each story carries 3-5 glossary entries per 100 words of body text,
and 4 comprehension exercises mixing `multiple_choice` with an
open-ended type (`open`, `discussion`, or `short_answer`) plus one of
`true_false`/`cloze` — never comprehension-by-recognition alone.

## Filename / id convention

The directory is **flat**: `content/stories/<id>.json`, where `<id>` is also
the story's `id` field (so a broken symlink between filename and content is
structurally impossible — a glob test can diff the two). Ids follow
`fr-<level_detail-lowercase>-<slug>`, e.g. `fr-b1-le-covoiturage.json` holds
`"id": "fr-b1-le-covoiturage"`. Exercise ids extend the story id
(`fr-b1-le-covoiturage-q1`); `item_id` — the curriculum item an exercise
evidences, per the schema — is namespaced `fr.story.<story-id>.<n>` (e.g.
`fr.story.fr-b1-le-covoiturage.1`) so results recorded against one story's
exercises never collide with another's in a learner's cross-story progress.

## Reproducible pipeline

### Batch drafting with cloudai-cli — pending availability

The intended pipeline is a `cloudai-cli` batch draft pass, one invocation per
target `(level_detail, theme)` pair, followed by the human-review checklist
below before any draft is committed:

```bash
# INTENDED command — cloudai-cli was not installed/reachable in this
# environment (`command -v cloudai` failed), so this batch step is pending
# cloudai availability, not yet exercised. Batch drafts still land as
# candidate JSON that a human reviews and edits before commit — cloudai only
# accelerates the first draft, it does not replace review.
cloudai run \
  --task "Write a French graded-reader short story matching learn-cli's story \
schema (schema_version 1.0, kind story, subject french). Level: <level> \
(<level_detail>). Theme: <theme>. 150-400 words scaling with level, everyday \
or literary French matching the level, self-contained, no copyrighted text. \
Emit valid JSON: id, subject, title, level, level_detail, language=fr, \
summary, body, glossary (3-5 entries per 100 words, term+definition+optional \
note), exercises (>=3, mixing multiple_choice with an open-ended type, \
item_id namespaced fr.story.<id>.<n>), audio: null, source.generator." \
  --output content/stories/<id>.json
```

Until `cloudai` is on `PATH` in an authoring environment, every story in this
ladder was **hand-authored directly to the target JSON shape** (`generator:
"hand-authored"` in each file's `source` block), following the same schema
constraints the prompt above encodes. When `cloudai` becomes available, run it
per new story, then apply the same review checklist — a cloudai draft is a
first draft, not a merge-ready file.

### Validating a story

french-cli has no runtime dependency on `learn-cli`'s validator (the contract
schema lives there, read-only, as the cross-subject reference); a story is
validated by calling the validator from a `learn-cli` checkout during
authoring, and again by `learn-cli`'s own CI (a glob test over every subject
repo's `content/stories/*.json`) after this repo merges:

```bash
cd <path-to-a-learn-cli-checkout>
uv run python -c "
import json, sys
from learn.contract import validate

path = sys.argv[1]
data = json.load(open(path))
errors = validate(data, 'story')
print('OK' if not errors else '\n'.join(errors))
" <path-to-story.json>
```

`validate(instance, schema_name)` returns an empty list on success; every
story in this ladder currently returns `[]`.

### How to add a story

1. Pick a level (`beginner`/`intermediate`/`advanced`) and a CEFR
   `level_detail` (`A1`-`C1`+) that keeps the ladder's rungs populated —
   don't stack every new story onto one rung.
2. Draft via `cloudai` (once available) or hand-author directly to the shape
   above; target word count for the chosen level (150-220 beginner, 230-270
   intermediate, 275-370+ advanced) and 3-5 glossary entries per 100 words.
3. Write >=3 comprehension exercises tied to specifics in the body (not
   generic questions answerable without reading), mixing `multiple_choice`
   with at least one open-ended type; namespace `item_id` as
   `fr.story.<story-id>.<n>`.
4. Save as `content/stories/<story-id>.json`, filename matching `id` exactly.
5. Run the validation snippet above against a `learn-cli` checkout.
6. Run the human-review checklist below before committing.
7. `markdownlint-cli2 "**/*.md" "#node_modules" "#.claude/skills"` still needs
   to pass if this file changed.

## Human-review checklist

A human (the operator) reviews samples at merge, not just the schema
validator. Check, per story:

- **Level-appropriateness** — does the grammar, tense range, and vocabulary
  actually match the CEFR tag? A1 stays in the present tense with short
  sentences; B1 can carry passé composé, imparfait, and simple subordinate
  clauses; B2/C1 can carry subjunctive, idiomatic phrasing, and longer
  sentences without becoming impenetrable. A story that reads harder or
  easier than its `level_detail` needs the tag or the text fixed.
- **Glossary accuracy** — does each `term` actually appear in the `body` in
  that form (or an obviously inflected form), is the `definition` correct and
  concise, and does an optional `note` add real value (grammar point,
  cultural aside) rather than repeat the definition? Flag any glossary entry
  for a word most learners at that level would already know — it's noise.
- **Exercise answerability** — can every exercise actually be answered from
  the body alone, without outside knowledge? For `multiple_choice`, are the
  distractors plausible but unambiguously wrong, and does exactly one
  `choices` entry match `answer` verbatim? For open/`discussion`/`short_answer`
  items, does the `rubric` state what passes vs. partial in a way a grader
  (human or agent) could apply consistently?
- **Cultural naturalness** — would a native speaker recognize the scene,
  dialogue, and register as authentic rather than a translated fixture (stiff
  phrasing, non-idiomatic word order, foreign-holiday assumptions)? Dialogue
  should sound like something a person would actually say out loud.
- **Originality** — the story must be original prose, not adapted from a
  copyrighted source (published graded readers, textbooks, song lyrics,
  etc.).

## Schema reference

The schema this ladder validates against lives at
`learn/contract/schemas/story.json` in the `learn-cli` repo (read-only from
french-cli's perspective — french-cli does not vendor or copy it). Required
fields: `schema_version` (`"1.0"`), `kind` (`"story"`), `id`, `subject`,
`title`, `level`, `body`, `glossary`, `exercises`. `level_detail`, `language`,
`summary`, `audio`, and `source` are optional but used by every story in this
ladder for full downstream fidelity (CEFR tagging, BCP-47 language tag,
catalog teaser, the reserved audio slot set to `null`, and generation
provenance).
