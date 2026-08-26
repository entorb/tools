"""Tests for helper.py."""

from helper import append_data, sort_lines


def test_append_data_adds_to_existing_date() -> None:
    db: dict[str, list[str]] = {"2024-01-01": ["foo"]}
    append_data(db, "2024-01-01", "bar")
    assert db == {"2024-01-01": ["foo", "bar"]}


def test_append_data_creates_new_date() -> None:
    db: dict[str, list[str]] = {}
    append_data(db, "2024-06-01", "baz")
    assert db == {"2024-06-01": ["baz"]}


def test_append_data_multiple_calls() -> None:
    db: dict[str, list[str]] = {}
    append_data(db, "2024-06-01", "a")
    append_data(db, "2024-06-01", "b")
    append_data(db, "2024-06-02", "c")
    assert db == {"2024-06-01": ["a", "b"], "2024-06-02": ["c"]}


def test_append_data_with_empty_string() -> None:
    db: dict[str, list[str]] = {"2024-01-01": []}
    append_data(db, "2024-01-01", "")
    assert db == {"2024-01-01": [""]}


def test_sort_lines_all_times() -> None:
    lines = ["09:00 breakfast", "08:30 wake up", "10:15 meeting"]
    result = sort_lines(lines)
    assert result == ["08:30 wake up", "09:00 breakfast", "10:15 meeting"]


def test_sort_lines_no_times() -> None:
    lines = ["xxx", "foo", "bar"]
    result = sort_lines(lines)
    assert result == ["xxx", "foo", "bar"]


def test_sort_lines_mixed() -> None:
    lines = ["foo", "09:00 breakfast", "bar", "08:30 wake up", "baz"]
    result = sort_lines(lines)
    assert result == ["08:30 wake up", "09:00 breakfast", "foo", "bar", "baz"]


def test_sort_lines_empty_list() -> None:
    assert sort_lines([]) == []


def test_sort_lines_time_like_but_invalid() -> None:
    lines = ["9:00 breakfast", "foo", "12:3 lunch", "10:00 meeting"]
    result = sort_lines(lines)
    assert result == [
        "10:00 meeting",
        "9:00 breakfast",
        "foo",
        "12:3 lunch",
    ]  # Only "10:00 meeting" matches pattern


def test_sort_lines_preserves_order_of_non_times() -> None:
    lines = ["foo", "bar", "baz"]
    result = sort_lines(lines)
    assert result == ["foo", "bar", "baz"]


def test_sort_lines_times_and_non_times_order() -> None:
    lines = ["foo", "10:00 a", "bar", "09:00 b", "baz"]
    result = sort_lines(lines)
    assert result == ["09:00 b", "10:00 a", "foo", "bar", "baz"]
