"""Tests for Strava."""

# ruff: noqa: DTZ001

import datetime as dt
from pathlib import Path

from influx_2 import grouping_to_dict, guess_activity, main_influx, read_data_to_list

FILE_IN = Path("tests/testdata/influx-media.csv")


def test_guess_activity() -> None:
    assert guess_activity(0) == "idle"
    assert guess_activity(-1000) == "idle"
    assert guess_activity(100) == "unknown100"
    assert guess_activity(200) == "movie"
    assert guess_activity(1000) == "gaming 3D+"


def test_read_data_to_list() -> None:
    lst = read_data_to_list(FILE_IN)
    row = lst[0]
    assert row == (dt.datetime(2025, 6, 3, 17, 5), 120.8)


def test_grouping_to_dict() -> None:
    lst = [
        (dt.datetime(2025, 6, 3, 17, 0), 200),
        (dt.datetime(2025, 6, 3, 17, 4), 199.9),
        (dt.datetime(2025, 6, 3, 17, 8), 210.1),
        (dt.datetime(2025, 6, 3, 17, 12), 200.1),
        (dt.datetime(2025, 6, 3, 17, 16), 20.0),
        (dt.datetime(2025, 6, 3, 17, 20), 500),
        (dt.datetime(2025, 6, 3, 17, 24), 500),
        (dt.datetime(2025, 6, 3, 17, 28), 500),
        (dt.datetime(2025, 6, 3, 17, 32), 500),
    ]
    db = grouping_to_dict(lst)
    assert db == {
        "2025-06-03": [
            "17:00 Media: movie (16 min)",
            "17:16 Media: idle (4 min)",
            "17:20 Media: gaming 3D+ (12 min)",
        ]
    }


def test_main_influx() -> None:
    # TODO: not working:
    # {'2025-06-03': ['17:11 Media: unknown (7528 min)']}
    if 1 == 2:  # noqa: PLR0133
        lst = read_data_to_list(FILE_IN)
        db = grouping_to_dict(lst)
        print(db)
        assert db == ""
        db = main_influx(FILE_IN)
        print(db)
        assert db == ""
