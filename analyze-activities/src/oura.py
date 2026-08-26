"""Read the Oura ring daily-sleep file and convert to json list of start and end."""

import csv
import datetime as dt
from pathlib import Path

from helper import append_data, export_json

FILE_IN = Path("data/oura_sleep.csv")
# example:
# see tests/testdata/oura.csv


def datestr_to_dt(datestr: str) -> dt.datetime:
    """Convert to datetime in local timezone, without seconds."""
    # 2025-05-18T20:13:41.000+02:00
    my_dt = dt.datetime.fromisoformat(datestr).replace(tzinfo=None, second=0)
    return my_dt


def main_oura(file_in: Path) -> dict[str, list[str]]:
    """Read oura.csv file and return dict."""
    db: dict[str, list[str]] = {}

    with file_in.open(mode="r", encoding="utf-8") as fh:
        csv_reader = csv.DictReader(fh, delimiter=",")
        for row in csv_reader:
            for event in ["bedtime_start", "bedtime_end"]:
                my_dt = datestr_to_dt(row[event])
                date = str(my_dt.date())
                t = "Start sleep" if event == "bedtime_start" else "Wake up"
                s = f"{my_dt.strftime('%H:%M')} {t}"
                append_data(db, date, s)

    return db


if __name__ == "__main__":
    db = main_oura(FILE_IN)
    export_json(db=db, filename="oura")
