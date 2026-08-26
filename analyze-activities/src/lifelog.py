"""Read my personal journal and convert to json list."""

# TODO: A and V prefix

import re
from pathlib import Path

from helper import append_data, export_json

FILE_IN = Path("data/lifelog.md")
# example:
# Do 22.05.2025
# +T 0450 early jogging
# some text without time

# re pattern for dates like "Do 02.01.2025"
RE_DATE = re.compile(r"^[A-Z][a-z] (\d{2})\.(\d{2})\.(\d{4})\s*$")

# re pattern for times without ":" like "1200"
RE_TIME_4_DIGIT = re.compile(r"^(\d{2})(\d{2})\s*(.*)$")
RE_START_PLUS = re.compile(r"^(\+T?)[\s:]*(\d{2}):?(\d{2})\s*(.*)$")


def format_time_prefix(s: str) -> str:
    """Format line. add ':' to time, move '+T' to after time."""
    # if line starts with + or +T followed by time
    match = RE_START_PLUS.match(s)
    if match:
        prefix = ""
        if match.group(1) == "+T":
            prefix = "gut Torben"
        elif match.group(1) == "+":
            prefix = "schön"
        s = f"{match.group(2)}:{match.group(3)} {prefix}: {match.group(4)}"
    else:
        # if line starts with 4 digits -> insert ":"
        s = RE_TIME_4_DIGIT.sub(r"\1:\2 \3", s)

    return s


def main_journal(file_in: Path) -> dict[str, list[str]]:
    """Read journal.md file and return dict."""
    db: dict[str, list[str]] = {}
    with file_in.open(encoding="utf-8") as fh:
        date = "2000-01-01"
        for line in fh:
            s = line.strip()
            if s.startswith("### KW") or s == "":
                continue

            # if line is a date: "Do 02.01.2025"
            match = RE_DATE.match(s)
            if match:
                date = f"{match.group(3)}-{match.group(2)}-{match.group(1)}"
                continue

            # if line starts with + or +T
            s = format_time_prefix(s)
            if s[0:2] == "+T":
                if s[6:8] == "+T":
                    s = "super T: " + s[2:]
                elif s.startswith("+"):
                    s = "gut: " + s[1:]

            # replace initials by full names
            if Path("src/name_fix.py").exists():
                from name_fix import name_fix  # noqa: PLC0415

                s = name_fix(s)

            s = s.replace("  ", " ")
            append_data(db, date, s)

    return db


if __name__ == "__main__":
    db = main_journal(FILE_IN)
    export_json(db=db, filename=FILE_IN.stem, sort=False)
