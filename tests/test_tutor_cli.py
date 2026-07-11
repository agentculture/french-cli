"""Behavioural tests for the tutor verbs (exit codes, state effects, streams)."""

from __future__ import annotations

import pytest

from french.cli import main
from tests.conftest import run_json

LEARNER = "cli-bot"


def test_record_updates_progress(capsys: pytest.CaptureFixture[str]) -> None:
    # Record a pass, then progress must reflect it as mastered + completed.
    main(
        [
            "record",
            "--learner",
            LEARNER,
            "--item",
            "fr.greetings.bonjour",
            "--result",
            "pass",
            "--json",
        ]
    )
    capsys.readouterr()
    rc, progress = run_json(capsys, ["progress", "--learner", LEARNER, "--json"])
    assert rc == 0
    assert progress["items_touched"] == 1
    assert progress["items_mastered"] == 1
    assert progress["mastery"]["fr.greetings.bonjour"] == "mastered"
    assert "fr.greetings.bonjour" in progress["completed"]


def test_lesson_start_lifts_items_and_sets_current(capsys: pytest.CaptureFixture[str]) -> None:
    main(["lesson", "start", "l.greetings", "--learner", LEARNER, "--json"])
    capsys.readouterr()
    rc, progress = run_json(capsys, ["progress", "--learner", LEARNER, "--json"])
    assert rc == 0
    # Both greetings items were lifted to at least introduced.
    assert progress["mastery"]["fr.greetings.bonjour"] == "introduced"
    assert progress["mastery"]["fr.greetings.presentations"] == "introduced"
    assert progress["current"]["module_id"] == "premiers-pas"


def test_advice_targets_weak_item(capsys: pytest.CaptureFixture[str]) -> None:
    main(
        [
            "record",
            "--learner",
            LEARNER,
            "--item",
            "fr.numbers.prix",
            "--result",
            "partial",
            "--json",
        ]
    )
    capsys.readouterr()
    rc, advice = run_json(capsys, ["advice", "--learner", LEARNER, "--json"])
    assert rc == 0
    focuses = [a.get("focus") for a in advice["advice"]]
    assert "fr.numbers.prix" in focuses


def test_progress_next_recommends_practice_for_touched(capsys: pytest.CaptureFixture[str]) -> None:
    main(
        [
            "record",
            "--learner",
            LEARNER,
            "--item",
            "fr.greetings.bonjour",
            "--result",
            "partial",
            "--json",
        ]
    )
    capsys.readouterr()
    rc, progress = run_json(capsys, ["progress", "--learner", LEARNER, "--json"])
    assert rc == 0
    assert progress["next"]["item_id"] == "fr.greetings.bonjour"
    assert "practice" in progress["next"]["command"]


def test_learner_default_is_echoed(capsys: pytest.CaptureFixture[str], monkeypatch) -> None:
    monkeypatch.setenv("FRENCH_CLI_LEARNER", "envy")
    rc, progress = run_json(capsys, ["progress", "--json"])
    assert rc == 0
    assert progress["learner"] == "envy"


def test_record_requires_item(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["record", "--result", "pass", "--json"])
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert err.strip(), "argparse error must route through the structured contract"


def test_errors_go_to_stderr_not_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["story", "read", "nope", "--json"])
    assert rc == 1
    captured = capsys.readouterr()
    assert captured.out == "", "error payload must not leak to stdout"
    assert captured.err.strip()


def test_repeat_without_harder_keeps_rung(capsys: pytest.CaptureFixture[str]) -> None:
    main(["lesson", "start", "l.numbers", "--learner", LEARNER, "--json"])
    capsys.readouterr()
    rc, payload = run_json(
        capsys, ["lesson", "repeat", "l.numbers", "--learner", LEARNER, "--json"]
    )
    assert rc == 0
    assert payload["lesson"]["difficulty"] == 1


def test_story_read_sets_position(capsys: pytest.CaptureFixture[str]) -> None:
    main(["story", "read", "dev-cafe", "--learner", LEARNER, "--json"])
    capsys.readouterr()
    rc, progress = run_json(capsys, ["progress", "--learner", LEARNER, "--json"])
    assert rc == 0
    assert progress["current"] is not None
    assert progress["current"]["item_id"] == "fr.food.commander"


def test_text_mode_is_human_readable(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["progress", "--learner", LEARNER])
    assert rc == 0
    out = capsys.readouterr().out
    assert out.startswith("# Progress")
