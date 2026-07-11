"""The committed French curriculum — modules, lessons, items, exercises.

This is the *content* half of the LLM-free tutor engine (the other half is
per-learner state). It is French-specific data only: the surrounding engine,
state, and CLI never hard-code course content, so a sibling language tutor swaps
this module (plus :mod:`french.tutor.subject` and ``content/stories/``) and
inherits the whole contract implementation unchanged.

Shape (mirrors culture-guide's proven ``curriculum`` layout — structured Python
data, path-addressable):

* a course is an ordered tuple of :class:`Module` (the web face renders one
  sub-page per module);
* each module holds ordered :class:`Lesson` groups; each lesson holds ordered
  :class:`Item` (curriculum items — the join key across lessons, practice,
  stories, ``record``, and ``progress.mastery``);
* each item carries the teachable ``points`` a driver must explain and check,
  plus its practice :class:`Exercise` batch.

Item ids are namespaced ``fr.<area>.<topic>`` and match the contract id pattern
``^[a-z0-9][a-z0-9._-]*$``.
"""

from __future__ import annotations

from typing import NamedTuple


class Exercise(NamedTuple):
    """One checkable/gradable exercise (same shape as the contract exercise)."""

    id: str
    type: str  # multiple_choice|true_false|cloze|short_answer|translation|open|discussion
    item_id: str
    prompt: str
    choices: tuple[str, ...] = ()
    answer: str = ""
    rubric: str = ""


class Item(NamedTuple):
    """One curriculum item: a stable id, a label, teachable points, exercises."""

    id: str
    label: str
    points: tuple[str, ...]
    exercises: tuple[Exercise, ...]
    body: str = ""


class Lesson(NamedTuple):
    """An ordered group of items taught together as one lesson directive."""

    id: str
    title: str
    objectives: tuple[str, ...]
    items: tuple[Item, ...]


class Module(NamedTuple):
    """A course module. ``level`` is the coarse contract rung; CEFR lives in stories."""

    id: str
    title: str
    summary: str
    level: str  # beginner|intermediate|advanced
    lessons: tuple[Lesson, ...]


# ---------------------------------------------------------------------------
# Module 1 — Premiers pas (beginner / A1)
# ---------------------------------------------------------------------------
_M1 = Module(
    id="premiers-pas",
    title="Premiers pas",
    summary="Greetings, introductions, numbers, and prices — the survival core.",
    level="beginner",
    lessons=(
        Lesson(
            id="l.greetings",
            title="Salutations et presentations",
            objectives=(
                "Greet and take leave at the right time of day.",
                "Introduce yourself and ask someone's name.",
            ),
            items=(
                Item(
                    id="fr.greetings.bonjour",
                    label="Greetings and politeness",
                    points=(
                        "Bonjour by day, bonsoir in the evening; salut is informal.",
                        "Politeness markers: s'il vous plait, merci, de rien, pardon.",
                        "« Ca va ? » asks how are you; reply « Ca va bien » or « Pas mal ».",
                    ),
                    exercises=(
                        Exercise(
                            id="bonjour-1",
                            type="translation",
                            item_id="fr.greetings.bonjour",
                            prompt="Say in French: 'Hello, how are you?'",
                            answer="Bonjour, ca va ?",
                        ),
                        Exercise(
                            id="bonjour-2",
                            type="multiple_choice",
                            item_id="fr.greetings.bonjour",
                            prompt="Quelle salutation convient le soir ?",
                            choices=("Bonjour", "Bonsoir", "Salut"),
                            answer="Bonsoir",
                        ),
                    ),
                ),
                Item(
                    id="fr.greetings.presentations",
                    label="Introducing yourself",
                    points=(
                        "« Je m'appelle ... » gives your name; « Comment vous "
                        "appelez-vous ? » asks it.",
                        "« Enchante(e) » = pleased to meet you (agree the -e if feminine).",
                        "« Je suis ... » + role/origin: je suis anglais, je suis etudiant.",
                    ),
                    exercises=(
                        Exercise(
                            id="presentations-1",
                            type="cloze",
                            item_id="fr.greetings.presentations",
                            prompt="« Comment vous ___-vous ? » — « Je m'appelle Claire. »",
                            answer="appelez",
                        ),
                        Exercise(
                            id="presentations-2",
                            type="open",
                            item_id="fr.greetings.presentations",
                            prompt="Introduce yourself in three short French sentences "
                            "(name, origin, one detail).",
                            rubric="Passes with a well-formed « je m'appelle » plus « je "
                            "suis »/« je viens de »; partial if one sentence is malformed.",
                        ),
                    ),
                ),
            ),
        ),
        Lesson(
            id="l.numbers",
            title="Nombres et prix",
            objectives=(
                "Count aloud from 0 to 20.",
                "Ask for and understand prices in euros.",
            ),
            items=(
                Item(
                    id="fr.numbers.compter",
                    label="Counting 0-20",
                    points=(
                        "0-16 are single words; 17-19 compose: dix-sept, dix-huit, dix-neuf.",
                        "Learn 0-20 by ear first — they recur in prices, times, and dates.",
                        "Liaison: « deux euros » links the x — /do.z‿o.ro/.",
                    ),
                    exercises=(
                        Exercise(
                            id="compter-1",
                            type="translation",
                            item_id="fr.numbers.compter",
                            prompt="Count aloud from 11 to 15 in French.",
                            answer="onze, douze, treize, quatorze, quinze",
                        ),
                        Exercise(
                            id="compter-2",
                            type="multiple_choice",
                            item_id="fr.numbers.compter",
                            prompt="Quel nombre est « quatorze » ?",
                            choices=("12", "14", "40"),
                            answer="14",
                        ),
                    ),
                ),
                Item(
                    id="fr.numbers.prix",
                    label="Prices in euros",
                    points=(
                        "« C'est combien ? » and « Ca fait combien ? » both ask the price.",
                        "Prices read 'X euros Y': quatre euros cinquante — never 'euros et'.",
                        "Round it off politely: « Ca fait dix euros. » — « Voila, merci ! »",
                    ),
                    exercises=(
                        Exercise(
                            id="prix-1",
                            type="translation",
                            item_id="fr.numbers.prix",
                            prompt="Say in French: 'That comes to seven euros fifty.'",
                            answer="Ca fait sept euros cinquante.",
                        ),
                        Exercise(
                            id="prix-2",
                            type="cloze",
                            item_id="fr.numbers.prix",
                            prompt="« C'est ___ ? » — « Deux euros, madame. »",
                            answer="combien",
                        ),
                    ),
                ),
            ),
        ),
    ),
)

# ---------------------------------------------------------------------------
# Module 2 — La vie quotidienne (intermediate / A2)
# ---------------------------------------------------------------------------
_M2 = Module(
    id="la-vie-quotidienne",
    title="La vie quotidienne",
    summary="Food and the market, ordering at a cafe, and daily-routine verbs.",
    level="intermediate",
    lessons=(
        Lesson(
            id="l.food",
            title="Au marche et au cafe",
            objectives=(
                "Name common foods and buy them by quantity.",
                "Order politely at a cafe and ask for the bill.",
            ),
            items=(
                Item(
                    id="fr.food.marche",
                    label="Market and food vocabulary",
                    points=(
                        "Staples: le pain, le fromage, les pommes, une baguette.",
                        "Quantities take de: un kilo de pommes, une tranche de jambon.",
                        "Some = du / de la / des: du pain, de la confiture, des oeufs.",
                    ),
                    exercises=(
                        Exercise(
                            id="marche-1",
                            type="multiple_choice",
                            item_id="fr.food.marche",
                            prompt="Comment dit-on 'goat cheese' ?",
                            choices=(
                                "le fromage de chevre",
                                "le pain de campagne",
                                "la pomme de terre",
                            ),
                            answer="le fromage de chevre",
                        ),
                        Exercise(
                            id="marche-2",
                            type="cloze",
                            item_id="fr.food.marche",
                            prompt="Claire achete un ___ de pommes.",
                            answer="kilo",
                        ),
                    ),
                ),
                Item(
                    id="fr.food.commander",
                    label="Ordering at a cafe",
                    points=(
                        "« Je voudrais ..., s'il vous plait » is the polite order frame.",
                        "« Un cafe » is an espresso; « un cafe au lait » comes with milk.",
                        "« L'addition, s'il vous plait » asks for the bill.",
                    ),
                    exercises=(
                        Exercise(
                            id="commander-1",
                            type="translation",
                            item_id="fr.food.commander",
                            prompt="Order politely: 'I would like a coffee and a "
                            "croissant, please.'",
                            answer="Je voudrais un cafe et un croissant, s'il vous plait.",
                        ),
                        Exercise(
                            id="commander-2",
                            type="open",
                            item_id="fr.food.commander",
                            prompt="Role-play ordering two items at a cafe and asking "
                            "for the bill.",
                            rubric="Passes with a polite « je voudrais » order plus "
                            "« l'addition »; partial if the bill request is missing.",
                        ),
                    ),
                ),
            ),
        ),
        Lesson(
            id="l.routine",
            title="La journee",
            objectives=(
                "Describe a daily routine with reflexive verbs.",
                "Say how often you do things.",
            ),
            items=(
                Item(
                    id="fr.routine.journee",
                    label="Daily-routine verbs",
                    points=(
                        "Reflexives: je me leve, je me lave, je m'habille.",
                        "Time of day: le matin, l'apres-midi, le soir.",
                        "Frequency: tous les jours, souvent, parfois, ne ... jamais.",
                    ),
                    exercises=(
                        Exercise(
                            id="journee-1",
                            type="cloze",
                            item_id="fr.routine.journee",
                            prompt="Le matin, je ___ leve a sept heures.",
                            answer="me",
                        ),
                        Exercise(
                            id="journee-2",
                            type="short_answer",
                            item_id="fr.routine.journee",
                            prompt="Decris ta matinee en deux phrases.",
                            rubric="Passes with two well-formed reflexive-verb sentences; "
                            "one is partial.",
                        ),
                    ),
                ),
            ),
        ),
    ),
)

# ---------------------------------------------------------------------------
# Module 3 — En ville (advanced rung of this ladder / A2)
# ---------------------------------------------------------------------------
_M3 = Module(
    id="en-ville",
    title="En ville",
    summary="Getting around town: asking directions and taking public transport.",
    level="advanced",
    lessons=(
        Lesson(
            id="l.directions",
            title="Demander son chemin et prendre les transports",
            objectives=(
                "Ask for and follow simple directions.",
                "Buy a ticket and use public transport.",
            ),
            items=(
                Item(
                    id="fr.ville.directions",
                    label="Asking for directions",
                    points=(
                        "« Pardon, ou est ... ? » / « Je cherche la gare. »",
                        "Directions: tout droit, a gauche, a droite, jusqu'au coin.",
                        "« C'est loin ? » — « Non, c'est a cinq minutes a pied. »",
                    ),
                    exercises=(
                        Exercise(
                            id="directions-1",
                            type="translation",
                            item_id="fr.ville.directions",
                            prompt="Ask politely: 'Excuse me, where is the station?'",
                            answer="Pardon, ou est la gare ?",
                        ),
                        Exercise(
                            id="directions-2",
                            type="multiple_choice",
                            item_id="fr.ville.directions",
                            prompt="'Turn left' se dit :",
                            choices=("tout droit", "a gauche", "a droite"),
                            answer="a gauche",
                        ),
                    ),
                ),
                Item(
                    id="fr.ville.transport",
                    label="Public transport",
                    points=(
                        "Prendre le metro / le bus / le train; un ticket, un carnet.",
                        "« Quel bus va a ... ? » — « Le 27 va au centre. »",
                        "« Un aller-retour pour Lyon, s'il vous plait. »",
                    ),
                    exercises=(
                        Exercise(
                            id="transport-1",
                            type="cloze",
                            item_id="fr.ville.transport",
                            prompt="Je prends le ___ pour aller au travail.",
                            answer="metro",
                        ),
                        Exercise(
                            id="transport-2",
                            type="open",
                            item_id="fr.ville.transport",
                            prompt="Buy a round-trip train ticket to Lyon and ask what "
                            "time it leaves.",
                            rubric="Passes with a polite « aller-retour » request plus a "
                            "time question (« a quelle heure »); partial if one is missing.",
                        ),
                    ),
                ),
            ),
        ),
    ),
)

#: The course, in order. The web face renders one sub-page per module.
MODULES: tuple[Module, ...] = (_M1, _M2, _M3)


# ---------------------------------------------------------------------------
# Indices + lookups (built once, module-level)
# ---------------------------------------------------------------------------
def all_lessons() -> tuple[tuple[Module, Lesson], ...]:
    """Every (module, lesson) pair in course order."""
    return tuple((m, lesson) for m in MODULES for lesson in m.lessons)


def all_items() -> tuple[tuple[Module, Lesson, Item], ...]:
    """Every (module, lesson, item) triple in course order."""
    return tuple((m, lesson, item) for m, lesson in all_lessons() for item in lesson.items)


def all_item_ids() -> tuple[str, ...]:
    """Stable item ids in course order (the mastery-map / join keys)."""
    return tuple(item.id for _, _, item in all_items())


def all_exercises() -> tuple[Exercise, ...]:
    """Every practice exercise across the curriculum, in course order."""
    return tuple(ex for _, _, item in all_items() for ex in item.exercises)


_ITEM_INDEX: dict[str, tuple[Module, Lesson, Item]] = {
    item.id: (m, lesson, item) for m, lesson, item in all_items()
}
_LESSON_INDEX: dict[str, tuple[Module, Lesson]] = {
    lesson.id: (m, lesson) for m, lesson in all_lessons()
}
_MODULE_INDEX: dict[str, Module] = {m.id: m for m in MODULES}


def find_item(item_id: str) -> tuple[Module, Lesson, Item] | None:
    return _ITEM_INDEX.get(item_id)


def find_lesson(lesson_id: str) -> tuple[Module, Lesson] | None:
    return _LESSON_INDEX.get(lesson_id)


def find_module(module_id: str) -> Module | None:
    return _MODULE_INDEX.get(module_id)


class LessonTarget(NamedTuple):
    """A resolved lesson-verb target: the module + the lesson to teach."""

    module: Module
    lesson: Lesson


def resolve_lesson_target(token: str) -> LessonTarget:
    """Resolve a lesson token — a lesson id, a module id, or an item id.

    A module id resolves to its first lesson; an item id resolves to the lesson
    that contains it. Raises :class:`KeyError` with the token if nothing matches
    (the CLI turns that into a ``CliError`` listing valid targets).
    """
    needle = token.strip()
    hit = find_lesson(needle)
    if hit is not None:
        return LessonTarget(module=hit[0], lesson=hit[1])
    module = find_module(needle)
    if module is not None:
        return LessonTarget(module=module, lesson=module.lessons[0])
    item_hit = find_item(needle)
    if item_hit is not None:
        return LessonTarget(module=item_hit[0], lesson=item_hit[1])
    raise KeyError(token)


def valid_lesson_targets() -> list[str]:
    """All accepted lesson tokens (module ids + lesson ids), for error hints."""
    return [m.id for m in MODULES] + [lesson.id for _, lesson in all_lessons()]


def exercises_for_scope(scope: str) -> tuple[str, tuple[Exercise, ...]] | None:
    """Resolve a practice ``scope`` to ``(resolved_scope, exercises)``.

    ``scope`` may be an item id (that item's exercises), a module id (all its
    items' exercises), or a lesson id (that lesson's exercises). Returns ``None``
    when nothing matches (the caller raises a ``CliError``).
    """
    item_hit = find_item(scope)
    if item_hit is not None:
        return item_hit[2].id, item_hit[2].exercises
    module = find_module(scope)
    if module is not None:
        exercises = tuple(
            ex for lesson in module.lessons for it in lesson.items for ex in it.exercises
        )
        return module.id, exercises
    lesson_hit = find_lesson(scope)
    if lesson_hit is not None:
        exercises = tuple(ex for it in lesson_hit[1].items for ex in it.exercises)
        return lesson_hit[1].id, exercises
    return None


def counts() -> dict[str, int]:
    """Deterministic content counts for the overview payload."""
    return {
        "modules": len(MODULES),
        "lessons": len(all_lessons()),
        "items": len(all_item_ids()),
        "exercises": len(all_exercises()),
    }
