"""Read Strava activity ics export and convert to json list."""

import datetime as dt
import re
from pathlib import Path

from helper import TZ_DE, TZ_UTC, append_data, export_json

FILE_IN = Path("data/Strava_Activity_Calendar.ics")
# example:
# see tests/testdata/strava.ics


def datestr_to_dt(datestr: str) -> dt.datetime:
    """Convert to datetime in local timezone, without seconds."""
    # 20250531T125001Z
    return (
        dt.datetime.strptime(datestr, "%Y%m%dT%H%M%SZ")
        .replace(tzinfo=TZ_UTC, second=0)
        .astimezone(tz=TZ_DE)
        .replace(tzinfo=None)
    )


def main_strava(file_in: Path) -> dict[str, list[str]]:
    """Read Strava_Activity_Calendar.ics and return dict."""
    db: dict[str, list[str]] = {}

    l_cont = file_in.read_text().split("BEGIN:VEVENT")
    l_cont.pop(0)  # remove header
    for event in l_cont:
        event_dict: dict[str, str] = {}
        for line in event.strip().splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                event_dict[key.strip()] = value.strip()
        act_type, title = event_dict["SUMMARY"].split(": ", maxsplit=1)
        if act_type == "Ride":
            act_type = "Cycling"
        elif act_type == "Run":
            act_type = "Jogging"
        elif act_type == "VirtualRide":
            act_type = "IndoorCycling"

        title = title.replace(" (Strava)", "")
        title = re.sub(r"^\d+\w?/365\s*", "", title)

        # replace initials by full names
        if Path("src/name_fix.py").exists():
            from name_fix import name_fix  # noqa: PLC0415

            title = name_fix(title)

        # DTSTART:20250531T125001Z
        dt_start = datestr_to_dt(event_dict["DTSTART"])
        date = str(dt_start.date())
        start_time = dt_start.strftime("%H:%M")
        # duration from end-start does not take breaks into account
        # hence added the time in the cal export.
        s = f"{start_time} {act_type}: {title}"
        append_data(db, date, s)

    return db


if __name__ == "__main__":
    db = main_strava(FILE_IN)
    export_json(db=db, filename="strava")
