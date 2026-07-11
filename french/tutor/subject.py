"""Subject identity — the French-specific knobs.

This module is the *first* thing a sibling language tutor (e.g. spanish-cli)
rewrites when porting french-cli: everything here is language-specific, and
nothing else in :mod:`french.tutor` hard-codes "French", "fr", or the persona.
The contract plumbing (``state``, ``engine``, ``stories``, ``contract_cite``,
and the CLI command chassis) is subject-agnostic and ports unchanged.

Port checklist for spanish-cli (see ``docs/contract-provenance.md`` for the full
token map):

* ``SUBJECT_ID`` ``"french"`` → ``"spanish"``
* ``COMMAND``    ``"french"`` → ``"spanish"``  (the console script on PATH)
* ``DISPLAY_NAME`` / ``LANGUAGE`` / ``TAGLINE`` / ``DESCRIPTION`` / ``PERSONA``
* the whole of :mod:`french.tutor.curriculum` (module/lesson/item content)
* the ``content/stories/*.json`` files
"""

from __future__ import annotations

#: The subject's registry id (matches ``^[a-z][a-z0-9-]*$``). The value learn-cli
#: keys this subject on, and the ``subject`` field of every contract payload.
SUBJECT_ID = "french"

#: The installed console script on PATH. Embedded verbatim in every ``command``
#: and ``record_with`` line a directive hands the driver, so it must be runnable.
COMMAND = "french"

#: Human-facing display name (the web face's course title).
DISPLAY_NAME = "French"

#: BCP-47 tag of the language being taught.
LANGUAGE = "fr"

#: One-line hook for the catalog.
TAGLINE = "Written and spoken French through graded stories, lessons, and practice."

#: Longer self-description for ``overview``.
DESCRIPTION = (
    "A graded-reader French tutor: greeting-to-getting-around lessons, market "
    "and cafe stories, and spaced practice from A1 upward. The CLI is LLM-free "
    "— it resolves what to teach and emits structured teaching directives; an "
    "agent or human driver does the conversational tutoring over --json."
)

#: The tutor persona a directive hands the driving agent (verb-agnostic voice).
PERSONA = (
    "You are a patient, practical French tutor. Teach in short spoken exchanges, "
    "start from what the learner already knows, and lean less on English as they "
    "improve. Encourage, correct gently, and keep every turn usable out loud."
)
