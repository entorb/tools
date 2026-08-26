"""Helper functions."""

import json
import re
from pathlib import Path
from zoneinfo import ZoneInfo

TZ_DE = ZoneInfo("Europe/Berlin")
TZ_UTC = ZoneInfo("UTC")
RE_TIME_PATTERN = re.compile(r"^(\d{2}):(\d{2})")


def sort_lines(lst: list[str]) -> list[str]:
    """
    Sort lines in lst.

    Lines starting with a time (HH:MM) come first and are sorted.
    Others follow in original order.
    """
    l1: list[str] = []
    l2: list[str] = []
    for item in lst:
        match = RE_TIME_PATTERN.match(item)
        if match:
            l1.append(item)
        else:
            l2.append(item)
    return sorted(l1) + l2


def export_json(db: dict[str, list[str]], filename: str, *, sort: bool = True) -> None:
    """Export sorted data as json."""
    db2: dict[str, list[str]] = {}
    for key in sorted(db.keys()):
        lst = sort_lines(db[key]) if sort else db[key]
        db2[key] = lst

    # export to json
    with Path(f"output/{filename}.json").open(
        "w", encoding="utf-8", newline="\n"
    ) as fh:
        json.dump(db2, fh, ensure_ascii=False, sort_keys=False, indent=2)


def append_data(db: dict[str, list[str]], date: str, s: str) -> None:
    """Append data to date."""
    if date in db:
        db[date].append(s)
    else:
        db[date] = [s]
