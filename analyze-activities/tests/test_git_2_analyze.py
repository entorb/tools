"""Tests for git."""

from pathlib import Path

import pytest

from git_2 import datestr_to_dt, extract_data_from_log_entry, process_file


def test_datestr_to_dt_basic() -> None:
    dt = datestr_to_dt("2025-04-19T21:48:55+02:00")
    assert dt.year == 2025
    assert dt.month == 4
    assert dt.day == 19
    assert dt.hour == 21
    assert dt.minute == 18
    assert dt.second == 0
    assert dt.tzinfo is None


def test_datestr_to_dt_removes_seconds_and_tz() -> None:
    dt = datestr_to_dt("2023-12-31T23:59:59+00:00")
    assert dt.year == 2023
    assert dt.month == 12
    assert dt.day == 31
    assert dt.hour == 23
    assert dt.minute == 29
    assert dt.second == 0
    assert dt.tzinfo is None


def test_datestr_to_dt_different_timezone() -> None:
    dt = datestr_to_dt("2022-01-01T00:30:00-05:00")
    assert dt.year == 2022
    assert dt.month == 1
    assert dt.day == 1
    assert dt.hour == 0
    assert dt.minute == 0
    assert dt.second == 0
    assert dt.tzinfo is None


def test_datestr_to_dt_invalid_format_raises() -> None:
    with pytest.raises(ValueError, match="not-a-date"):
        datestr_to_dt("not-a-date")


def test_extract_data_from_log_entry_1() -> None:
    element = """2025-01-07T21:37:10+01:00: Update .gitattributes
 1 file changed, 1 insertion(+), 26 deletions(-)
"""
    d = extract_data_from_log_entry(element)
    assert d["date"] == "2025-01-07", d["date"]
    assert d["time"] == "21:07", d["time"]
    assert d["title"] == "Update .gitattributes", d["title"]
    assert d["files"] == 1, d["files"]
    assert d["insert"] == 1, d["insert"]
    assert d["del"] == 26, d["del"]


def test_extract_data_from_log_entry_2() -> None:
    element = """2024-07-13T07:48:41+02:00: Fixing Ruff
 10 files changed, 140 insertions(+), 113 deletions(-)
"""
    d = extract_data_from_log_entry(element)
    assert d["date"] == "2024-07-13", d["date"]
    assert d["time"] == "07:18", d["time"]
    assert d["title"] == "Fixing Ruff", d["title"]
    assert d["files"] == 10, d["files"]
    assert d["insert"] == 140, d["insert"]
    assert d["del"] == 113, d["del"]


def test_extract_data_from_log_entry_3() -> None:
    element = """2024-07-13T03:55:16+02:00: convert json transactions to excel
 2 files changed, 87 insertions(+)
"""
    d = extract_data_from_log_entry(element)
    assert d["date"] == "2024-07-13", d["date"]
    assert d["time"] == "03:25", d["time"]
    assert d["title"] == "convert json transactions to excel", d["title"]
    assert d["files"] == 2, d["files"]
    assert d["insert"] == 87, d["insert"]
    assert d["del"] == 0, d["del"]


def test_process_file() -> None:
    db: dict[str, list[str]] = {}
    process_file(p=Path("tests/testdata/git.log"), db=db)
    # not README line included!
    assert db["2021-05-13"] == [
        "18:40 Coding at git: Initial commit (17770 changes)",
    ]
    assert db["2021-05-27"] == ["11:05 Coding at git: added disputation (1545 changes)"]
