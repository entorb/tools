"""Tests for git."""

import datetime as dt
from pathlib import Path

from oura import datestr_to_dt, main_oura


def test_datestr_to_dt() -> None:
    assert datestr_to_dt("2025-05-18T20:13:41.000+02:00") == dt.datetime(  # noqa: DTZ001
        2025, 5, 18, 20, 13, 0, 0, tzinfo=None
    )


def test_main_oura() -> None:
    db = main_oura(Path("tests/testdata/oura.csv"))
    assert db == {
        "2025-01-22": ["22:21 Start sleep"],
        "2025-01-23": [
            "06:00 Wake up",
            "11:32 Start sleep",
            "12:55 Wake up",
            "21:08 Start sleep",
        ],
        "2025-01-24": ["05:06 Wake up"],
    }
