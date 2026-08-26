"""
Read calendar appointments and convert to json list.

based on https://github.com/entorb/tools-calendar/blob/main/upcoming_events.py
"""

import datetime as dt
from pathlib import Path

import icalendar

from helper import TZ_DE, TZ_UTC, append_data, export_json

FILE_IN = Path("data/cal.ics")
TODAY = dt.datetime.now(tz=TZ_DE).date()
NOW_DT = dt.datetime.now(tz=TZ_DE).replace(tzinfo=None)


def adjust_dt(my_dt: dt.datetime) -> dt.datetime:
    """Convert to datetime in local timezone, without seconds."""
    if my_dt.tzinfo == TZ_UTC:
        my_dt = my_dt.astimezone(TZ_DE)
    return my_dt.replace(tzinfo=None, second=0, microsecond=0)


def main_cal(p: Path) -> dict[str, list[str]]:  # noqa: D103
    db: dict[str, list[str]] = {}

    with p.open(encoding="utf-8", newline="\r\n") as f:
        calendar = icalendar.Calendar.from_ical(f.read())

    for event in calendar.walk("VEVENT"):
        title = str(event.get("SUMMARY")).strip()

        # replace initials by full names
        if Path("src/name_fix.py").exists():
            from name_fix import name_fix  # noqa: PLC0415

            title = name_fix(title)

        # Skip repeating events
        if "RRULE" in event:
            # print("skipping", title)
            continue

        start = event.get("DTSTART").dt
        end = event.get("DTEND").dt

        # skip future events
        if (type(start) is dt.date and start > TODAY) or (
            type(start) is dt.datetime and start.replace(tzinfo=None) > NOW_DT
        ):
            continue

        # full-day events
        if type(start) is dt.date:
            date = str(start)
            s = f"00:00 {title}"
        else:
            assert type(start) is dt.datetime
            my_dt = adjust_dt(start)
            date = str(my_dt.date())
            time = my_dt.strftime("%H:%M")
            s = f"{time} {title}"

        append_data(db, date, s)

        # multi-day events
        if type(start) is dt.date and type(end) is dt.date and end > start:
            day = start + dt.timedelta(days=1)
            while day < end:
                append_data(db, str(day), s)
                day = day + dt.timedelta(days=1)

    return db


if __name__ == "__main__":
    db = main_cal(p=FILE_IN)
    export_json(db=db, filename="cal")
