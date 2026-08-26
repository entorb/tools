"""Tests for Strava."""

import datetime as dt
from pathlib import Path

from strava import datestr_to_dt, main_strava


def test_datestr_to_datetime() -> None:
    assert datestr_to_dt("20250531T125001Z") == dt.datetime(  # noqa: DTZ001
        2025, 5, 31, 12 + 2, 50, 0, 0, tzinfo=None
    )


def test_main_strava() -> None:
    db = main_strava(Path("tests/testdata/strava.ics"))
    # cspell:disable
    assert db == {
        "2025-05-31": [
            "14:50 Cycling: Erster 1000er des Jahres: Marloffstein, EBS, Muggendorf, Gößweinstein, Rödlas (205 min)"  # noqa: E501
        ],
        "2025-05-30": ["13:51 Hike: Gößweinstein (282 min)"],
    }

    # cspell:enable
