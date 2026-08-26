"""Tests for Journal."""

from pathlib import Path

from lifelog import format_time_prefix, main_journal


def test_journal() -> None:
    db = main_journal(Path("tests/testdata/journal.md"))
    # cspell:disable
    assert db == {
        "2025-05-19": ["07:00 aufgestanden", "08:00 Rad ins Büro"],
        "2025-05-20": [
            "Hier ein Beispiel für einen gemixten Tag",
            "12:00 Mittagessen",
            "Früh ins Bett",
        ],
    }
    # cspell:enable


def test_format_time_prefix() -> None:
    s = "Some text"
    assert format_time_prefix(s) == s

    s = "1200 Some text"
    assert format_time_prefix(s) == "12:00 Some text"

    s = "12:00 Some text"
    assert format_time_prefix(s) == "12:00 Some text"

    s = "+1200 Some text"
    assert format_time_prefix(s) == "12:00 schön: Some text"

    s = "+12:00 Some text"
    assert format_time_prefix(s) == "12:00 schön: Some text"

    s = "+ 12:00 Some text"
    assert format_time_prefix(s) == "12:00 schön: Some text"

    s = "+T1200 Some text"
    assert format_time_prefix(s) == "12:00 gut Torben: Some text"

    s = "+T12:00 Some text"
    assert format_time_prefix(s) == "12:00 gut Torben: Some text"

    s = "+T 12:00 Some text"
    assert format_time_prefix(s) == "12:00 gut Torben: Some text"
