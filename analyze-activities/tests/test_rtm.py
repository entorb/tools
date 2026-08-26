"""Tests for git."""

from pathlib import Path

from rtm import main_rtm


def test_main_rtm() -> None:
    db = main_rtm(Path("tests/testdata/rtm.csv"))
    assert db == {
        "2025-06-09": [
            "06:32 Task Private: Task1 (10min)",
            "06:33 Task Private: Task2 (60min)",
        ]
    }
    # estimation of 5 min is filtered out
