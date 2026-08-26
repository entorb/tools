"""Tests for cal.py."""
# ruff: noqa: DTZ001

import datetime as dt
from pathlib import Path

from cal import adjust_dt, main_cal
from helper import TZ_DE, TZ_UTC


def test_adjust_dt_with_utc_datetime() -> None:
    utc_dt = dt.datetime(2024, 6, 1, 12, 34, 56, 789000, tzinfo=TZ_UTC)
    result = adjust_dt(utc_dt)
    expected = dt.datetime(2024, 6, 1, 12 + 2, 34, 0, 0, tzinfo=None)
    assert result == expected


def test_adjust_dt_with_local_tz_datetime() -> None:
    local_dt = dt.datetime(2024, 6, 1, 15, 0, 30, 123456, tzinfo=TZ_DE)
    result = adjust_dt(local_dt)
    expected = local_dt.replace(tzinfo=None, second=0, microsecond=0)
    assert result == expected


def test_adjust_dt_with_naive_datetime() -> None:
    naive_dt = dt.datetime(2024, 6, 1, 10, 20, 30, 400000)
    result = adjust_dt(naive_dt)
    expected = naive_dt.replace(second=0, microsecond=0)
    assert result == expected


def test_main_cal() -> None:
    db = main_cal(p=Path("tests/testdata/cal.ics"))
    assert db["2009-10-18"] == ["00:00 Title Full Day"]
    assert "2023-06-15" not in db  # repeating
    assert db["2025-05-31"] == ["14:00 Title 1", "14:30 Title 2"]
