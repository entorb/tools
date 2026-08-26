"""Read the git log files and convert to json list."""

import datetime as dt
import re
from pathlib import Path

from helper import append_data, export_json

MIN_CHANGES = 5
TIME_OFFSET = 30  # min

# example source data:
# 2025-01-07T21:37:10+01:00: Update .gitattributes
#  1 file changed, 1 insertion(+), 26 deletions(-)


def datestr_to_dt(datestr: str) -> dt.datetime:
    """Convert to datetime in local timezone, without seconds."""
    # 2025-04-19T21:18:55+02:00
    my_dt = dt.datetime.fromisoformat(datestr).replace(tzinfo=None, second=0)
    # guess the start time of the commit
    my_dt -= dt.timedelta(minutes=TIME_OFFSET)
    return my_dt


def extract_data_from_log_entry(element: str) -> dict[str, str | int]:
    """Extract data from commit log line."""
    stats_dict: dict[str, str | int] = {}
    header, changes = element.split("\n ")
    date_str, title = header.split(": ", maxsplit=1)
    stats_dict["title"] = title.replace("\t", " ").strip()

    my_dt = datestr_to_dt(date_str)
    stats_dict["date"] = str(my_dt.date())
    stats_dict["time"] = my_dt.strftime("%H:%M")

    stats_list = changes.split(",")
    for x in stats_list:
        x = x.strip()  # noqa: PLW2901
        if "file" in x:
            y = re.sub(r" files? changed", "", x)
            stats_dict["files"] = int(y)
        elif "insertion" in x:
            y = re.sub(r" insertions?\(\+\)", "", x)
            stats_dict["insert"] = int(y)
        elif "deletion" in x:
            y = re.sub(r" deletions?\(\-\)", "", x)
            stats_dict["del"] = int(y)

    if "files" not in stats_dict:
        msg = "no files found in", element
        raise ValueError(msg)
    if "insert" not in stats_dict:
        stats_dict["insert"] = 0
    if "del" not in stats_dict:
        stats_dict["del"] = 0

    return stats_dict


def process_file(p: Path, db: dict[str, list[str]]) -> None:
    """Process a git log file."""
    repo = p.stem
    print(repo)
    cont = p.read_text()

    seen: set[tuple[str, str, str]] = set()

    for element in cont.split("\n\n"):
        # entries are in reverse cron. order
        d = extract_data_from_log_entry(element=element)
        # skip minor changes
        assert isinstance(d["insert"], int)
        assert isinstance(d["del"], int)
        changes = d["insert"]  # + d["del"]
        if changes < MIN_CHANGES:
            continue
        assert isinstance(d["title"], str)
        if (
            "README" in d["title"]
            or "cspell-words.txt" in d["title"]
            or "History cleanup" in d["title"]
            or ".gitignore" in d["title"]
        ):
            continue
        date = d["date"]
        assert isinstance(date, str)
        assert isinstance(d["time"], str)
        assert isinstance(repo, str)
        fingerprint = (date, d["time"], repo)
        if fingerprint not in seen:
            seen.add(fingerprint)
            # print(d["date"], d["time"], d["title"], changes)
            s = f"{d['time']} Coding at {repo}: {d['title']} ({changes} changes)"
            append_data(db, date, s)


def main_git() -> dict[str, list[str]]:  # noqa: D103
    db: dict[str, list[str]] = {}
    for p in Path("data/git").glob("*.log"):
        process_file(p=p, db=db)
    return db


if __name__ == "__main__":
    db = main_git()
    export_json(db=db, filename="git")
